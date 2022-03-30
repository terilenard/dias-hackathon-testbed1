"""

This script is to authenticate CAN messages on the base of Autosar SecOC module

        hexSecKey = "D251E60F5CDFC443A3DADD6968E871CB"
        secret= bytearray.fromhex(hexSecKey)
        cobj = CMAC.new(secret, ciphermod=AES)
        hexMes = "aabbccdd010000000000000000000000"
        byteMes= bytearray.fromhex(hexMes)
        cobj.update(byteMes)

        print (cobj.hexdigest())

"""

# Create command to execute the script

from Crypto.Hash import CMAC
from Crypto.Cipher import AES
from get_start_freshness import *

# alternative to check "from cryptography.fernet import Fernet"

class SecocVerification:
	def __init__(self, raw_can_frame):
		self.secret_key = "00000000000000000" # Kex for encryption
		self.raw_can = raw_can_frame[2:] # Strip off 0x prefix e.g. "db7cffff19d4de01"
		self.freshness_counter = 0x00000000
		self.message = '' # Message to be encrypted
		try: 
			with open ("/etc/dbcfeeder/counter.txt", 'r') as f:
				self.freshness_counter = int(f.read().strip(), 16)
		except Exception:
			print("Error in j1939reader.py whilst trying to read from file 'counter.txt'. Creating file...")
			synchronize_counter(self.raw_can[:8], self.raw_can[8:10], self.raw_can[-6:])
			#comment above line and uncomment below two lines for diasbaling FV synchronization
			#with open("/etc/dbcfeeder/counter.txt", "w") as f: # Write complete counter value into persistant memory to load after power off
				#f.write(str('{:08x}'.format(self.freshness_counter)) + "\n") # Format complete counter value as 4 byte hex number
	
	def authentication_status(self):
		transmitted_data = self.raw_can[:8] # first 4 bytes
		transmitted_fv = self.raw_can[8:10] # 5th byte
		transmitted_mac_val = self.raw_can[-6:] # last 3 bytes

		calculated_mac_val = self.calculate_mac(transmitted_data, transmitted_fv)

		#Compare transmitted and calculated MAC values
		if transmitted_mac_val == calculated_mac_val:
			with open("/etc/dbcfeeder/counter.txt", "w") as f: # Write complete counter value into persistant memory to load after power off
				f.write(str('{:08x}'.format(self.freshness_counter)) + "\n") # Format complete counter value as 4 byte hex number
			return 1  
		return 0

	def calculate_mac(self, transmitted_data, transmitted_fv):
		self.message = self.assign_cipher(transmitted_data, transmitted_fv)
		if ''.__eq__(self.secret_key) or ''.__eq__(self.message):
			print('Key or message cannot be empty!')
			return -1
		if len(self.secret_key) < 32:
			print(f"Key-length: {len(self.secret_key)}")
			print('Key-length is less than 16 byte')
			return -1
		
		secret= bytearray.fromhex(self.secret_key)
		cobj = CMAC.new(secret, ciphermod=AES)
		byteMes= bytearray.fromhex(self.message)
		cobj.update(byteMes)
		calculated_mac = cobj.hexdigest()
		trunc_calculated_mac = calculated_mac[0:6] # Truncated mac to compare in authentication_status()
		return trunc_calculated_mac        

	def assign_cipher(self, transmitted_data, transmitted_fv):
		complete_counter_val = self.calculate_complete_freshness(transmitted_fv)[2:]
		self.message = '00C8' + transmitted_data + complete_counter_val # Data Identifier 0x00C8 needs to be put as 2 byte hex number at the beginning of the message
		return self.message  

	def calculate_complete_freshness(self, transmitted_fv):
		transmitted_fv = int(transmitted_fv, 16)
		pi_counter_lsb = (self.freshness_counter&(0xFF<<(8*0)))>>(8*0) # Gets LSB of complete reference counter
		pi_counter_3msb = hex((self.freshness_counter&(0xFFFFFF<<(8*1)))>>(8*1))[2:] # Gets the 3 MSBs of complete reference counter

		if transmitted_fv > pi_counter_lsb: #maybe >=?
			transmitted_fv = str('{:02x}'.format(transmitted_fv)) # Hex representation of transmitted_fv without 0x prefix
			complete_freshness = "0x" + pi_counter_3msb + transmitted_fv
		else: # transmitted_fv < pi_counter_lsb
			transmitted_fv = str('{:02x}'.format(transmitted_fv)) # Hex representation of transmitted_fv without 0x prefix
			new_pi_counter_3msb = int(pi_counter_3msb,16) + 0x01
			new_pi_counter_3msb = hex(new_pi_counter_3msb) # Convert to hex
			complete_freshness =  "0x" + new_pi_counter_3msb[2:] + transmitted_fv
			
		self.freshness_counter = int(complete_freshness,16)
		complete_counter_hex = "{0:#0{1}x}".format(self.freshness_counter,10) # Convert to hex for MAC generation
		return complete_counter_hex
