"""
This script is to collect the required data from the in-vehicle server, `kuksa-val-server`, 
pre-process them, and transmit the result to the DIAS-KUKSA cloud.

The script needs to be located in the same directory where testclient.py 
is also located: ~/kuksa.val/vss-testclient/

Prior to running this script, the following lines should be added to 
testclient.py:
# At the end of - 'def do_getValue(self, args)'
datastore = json.loads(resp)
return datastore

python3 cloudfeeder.py -p 1883 -t telemtry

"""

import argparse
import json
import socket
import subprocess
import time
import preprocessor_bosch
import kuksa_viss_client

def getConfig():
    parser = argparse.ArgumentParser()
    parser.add_argument("-j", "--jwt", help="JWT security token file", type=str)
    parser.add_argument("--host", metavar='\b', help="Host URL", type=str) # "mqtt.bosch-iot-hub.com"
    parser.add_argument("-p", "--port", metavar='\b', help="Protocol Port Number", type=str) # "8883"
    parser.add_argument("-u", "--username", metavar='\b', help="Credential Authorization Username (e.g., {username}@{tenant-id} ) / Configured in \"Bosch IoT Hub Management API\"", type=str) # "pc01@t20babfe7fb2840119f69e692f184127d"
    parser.add_argument("-P", "--password", metavar='\b', help="Credential Authorization Password / Configured in \"Bosch IoT Hub Management API\"", type=str) # "junhyungki@123"
    parser.add_argument("-t", "--type", metavar='\b', help="Transmission Type (e.g., telemetry or event)", type=str) # "telemetry"
    parser.add_argument("-r", "--resume", action='store_true', help="Resume the application with the accumulated data when restarting", default=False)
    args = parser.parse_args()
    return args

def getVISSConnectedClient(jwt):

    config = getKuksaValConfig()
    
    # 1. Create a VISS client instance
    client = kuksa_viss_client.KuksaClientThread(config)

    # 2. Connect to the running viss server insecurely
    client.start()
    # client.do_connect("--insecure")

    # 3. Authorize the connection
    # client.do_authorize(jwt)
    client.authorize(jwt)
    # client.authorize('eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiJrdWtzYS52YWwiLCJpc3MiOiJFY2xpcHNlIEtVS1NBIERldiIsImFkbWluIjp0cnVlLCJpYXQiOjE1MTYyMzkwMjIsImV4cCI6MTc2NzIyNTU5OSwia3Vrc2EtdnNzIjp7IioiOiJydyJ9fQ.QQcVR0RuRJIoasPXYsMGZhdvhLjUalk4GcRaxhh3-0_j3CtVSZ0lTbv_Z3As5BfIYzaMlwUzFGvCVOq2MXVjRK81XOAZ6wIsyKOxva16zjbZryr2V_m3yZ4twI3CPEzJch11_qnhInirHltej-tGg6ySfLaTYeAkw4xYGwENMBBhN5t9odANpScZP_xx5bNfwdW1so6FkV1WhpKlCywoxk_vYZxo187d89bbiu-xOZUa5D-ycFkd1-1rjPXLGE_g5bc4jcQBvNBc-5FDbvt4aJlTQqjpdeppxhxn_gjkPGIAacYDI7szOLC-WYajTStbksUju1iQCyli11kPx0E66me_ZVwOX07f1lRF6D2brWm1LcMAHM3bQUK0LuyVwWPxld64uSAEsvSKsRyJERc7nZUgLf7COnUrrkxgIUNjukbdT2JVN_I-3l3b4YXg6JVD7Y5g0QYBKgXEFpZrDbBVhzo7PXPAhJD6-c3DcUQyRZExbrnFV56RwWuExphw8lYnbMvxPWImiVmB9nRVgFKD0TYaw1sidPSSlZt8Uw34VZzHWIZQAQY0BMjR33fefg42XQ1YzIwPmDx4GYXLl7HNIIVbsRsibKaJnf49mz2qnLC1K272zXSPljO11Ke1MNnsnKyUH7mcwEs9nhTsnMgEOx_TyMLRYo-VEHBDLuEOiBo')

    return client
def getKuksaValConfig():
    try:
        with open("/etc/cloudfeeder/kuksa_val_config.json", "r") as f:
            return json.load(f)
    except FileNotFoundError as e:
        print(e)


def checkPath(client, path):
    # val = client.do_getValue(path)['value']
    val = json.loads(client.getValue(path))

    if val["data"]["dp"]["value"] == "---":
        return "0"
    else:
        return val["data"]["dp"]["value"]

def socket_connection_on(s, host, port):
    try:
        s.connect((host, int(port))) # host and port
        print("# Socket Connected :)")
        return True
    except socket.timeout:
        print("# Socket Timeout :(")
        return False
    except socket.gaierror:
        print("# Temporary failure in name resolution :(")
        return False
    except:
        return False

def send_telemetry(host, port, comb, telemetry_queue):
    # Create a socket instance
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(0.1)
    if socket_connection_on(s, host, port):
        if len(telemetry_queue) != 0:
            for i in range(0, len(telemetry_queue)):
                tel = telemetry_queue.pop(0)
                p = subprocess.Popen(tel)
                print("# Popped telemetry being sent... Queue Length: " + str(len(telemetry_queue)))
                try:
                    p.wait(1)
                except subprocess.TimeoutExpired:
                    p.kill()
                    telemetry_queue.insert(0, tel)
                    print("\n# Timeout, the popped telemetry collected. Queue Length: " + str(len(telemetry_queue)))
                    telemetry_queue.append(comb)
                    print("# The current telemetry also collected. Queue Length: " + str(len(telemetry_queue)))
                    return
                except socket.gaierror:
                    s.close()
                    telemetry_queue.insert(0, tel)
                    print("\n# Temporary failure in name resolution, the popped telemetry collected. Queue Length: " + str(len(telemetry_queue)))
                    telemetry_queue.append(comb)
                    print("# The current telemetry also collected. Queue Length: " + str(len(telemetry_queue)))
                    return
                print("# Successfully done!\n")
        p = subprocess.Popen(comb)
        print("# Current telemetry being sent...")
        try:
            p.wait(1)
        except subprocess.TimeoutExpired:
            p.kill()
            telemetry_queue.append(comb)
            print("\n# Timeout, the current telemetry collected. Queue Length: " + str(len(telemetry_queue)))
            return
        except socket.gaierror:
            s.close()
            telemetry_queue.append(comb)
            print("\n# Temporary failure in name resolution, the current telemetry collected. Queue Length: " + str(len(telemetry_queue)))
            return
        print("# Successfully done!\n")
    else:
        telemetry_queue.append(comb)
        print("# The current telemetry collected, Queue Length: " + str(len(telemetry_queue)))

def load_data(binPro, queue):
    try:
        f = open("saved_dict.json", "r")
        binPro.dashboard = json.load(f)
        print("Saved dictionary file successfully loaded :)")
    except FileNotFoundError:
        print("Saved dictionary file not found :(")
    except IOError:
        print("Saved dictionary file not found :(")
    try:
        f = open("saved_samp.json", "r")
        samp = json.load(f)
        binPro.ctr_total = samp["ctr_total"]
        binPro.ctr_tscr_good = samp["ctr_tscr_good"]
        binPro.ctr_tscr_intermediate = samp["ctr_tscr_intermediate"]
        binPro.ctr_tscr_bad = samp["ctr_tscr_bad"]
        binPro.start_sampling = samp["start_sampling"]
        print("Saved sampling time file successfully loaded :)")
    except FileNotFoundError:
        print("Saved sampling time file not found :(")
    except IOError:
        print("Saved sampling time file not found :(")
    try:
        print("h")
        f = open("saved_queue.json", "r")
        queue = json.load(f)
        print("Saved telemetry queue file successfully loaded :)")
    except FileNotFoundError:
        print("Saved telemetry queue file not found :(")
        print("Starting from scratch.")
    except IOError:
        print("Saved telemetry queue file not found :(")
        print("Starting from scratch.")
    return queue


def save_data(binPro, queue):
    saved_dict = json.dumps(binPro.dashboard)
    f = open("saved_dict.json", "w")
    f.write(saved_dict)
    f.close()
    # Saving sampling times
    saved_samp = {
        "ctr_total": binPro.ctr_total,
        "ctr_tscr_good": binPro.ctr_tscr_good,
        "ctr_tscr_intermediate": binPro.ctr_tscr_intermediate,
        "ctr_tscr_bad": binPro.ctr_tscr_bad,
        "start_sampling": binPro.start_sampling
    }
    saved_samp = json.dumps(saved_samp)
    f = open("saved_samp.json", "w")
    f.write(saved_samp)
    f.close()
    saved_queue = json.dumps(queue)
    f = open("saved_queue.json", "w")
    f.write(saved_queue)
    f.close()

print("kuksa.val cloud example feeder")

# Get the pre-fix command for publishing data
args = getConfig()

# Get a VISS-server-connected client
client = getVISSConnectedClient(args.jwt)

# Create a BinInfoProvider instance
binPro = preprocessor_bosch.BinInfoProvider()

# buffer for mqtt messages in case of connection loss or timeout
telemetry_queue = []

if args.resume:
    print("Resuming accumulated data....")
    telemetry_queue = load_data(binPro, telemetry_queue)
    print("Queue Length: " + str(len(telemetry_queue)))

while True:
    # 1. Time delay
    time.sleep(0.8)

    # 2. Store signals' values from the target path to the dictionary keys
    binPro.signals["Aftrtrtmnt1SCRCtlystIntkGasTemp"] = float(checkPath(client, "Vehicle.AfterTreatment.Aftrtrtmnt1SCRCtlystIntkGasTemp"))
    binPro.signals["Aftertreatment1IntakeNOx"] = float(checkPath(client, "Vehicle.AfterTreatment.NOxLevel.Aftertreatment1IntakeNOx"))
    binPro.signals["Aftertreatment1OutletNOx"] = float(checkPath(client, "Vehicle.AfterTreatment.NOxLevel.Aftertreatment1OutletNOx"))
    binPro.signals["Aftrtratment1ExhaustGasMassFlow"] = float(checkPath(client, "Vehicle.AfterTreatment.Aftrtratment1ExhaustGasMassFlow"))
    binPro.signals["NominalFrictionPercentTorque"] = float(checkPath(client, "Vehicle.Drivetrain.InternalCombustionEngine.Engine.NominalFrictionPercentTorque"))
    binPro.signals["AmbientAirTemp"] = float(checkPath(client, "Vehicle.AmbientAirTemp"))
    binPro.signals["BarometricPress"] = float(checkPath(client, "Vehicle.OBD.BarometricPress"))
    binPro.signals["EngCoolantTemp"] = checkPath(client, "Vehicle.OBD.EngCoolantTemp")
    binPro.signals["EngPercentLoadAtCurrentSpeed"] = float(checkPath(client, "Vehicle.OBD.EngPercentLoadAtCurrentSpeed"))
    binPro.signals["EngReferenceTorque"] = float(checkPath(client, "Vehicle.Drivetrain.InternalCombustionEngine.Engine.EngReferenceTorque"))
    binPro.signals["EngSpeedAtPoint2"] = float(checkPath(client, "Vehicle.Drivetrain.InternalCombustionEngine.Engine.EngSpeedAtPoint2"))
    binPro.signals["EngSpeedAtIdlePoint1"] = float(checkPath(client, "Vehicle.Drivetrain.InternalCombustionEngine.Engine.EngSpeedAtIdlePoint1"))
    binPro.signals["EngSpeed"] = float(checkPath(client, "Vehicle.Drivetrain.InternalCombustionEngine.Engine.EngSpeed"))
    binPro.signals["ActualEngPercentTorque"] = float(checkPath(client, "Vehicle.Drivetrain.InternalCombustionEngine.Engine.ActualEngPercentTorque"))
    binPro.signals["TimeSinceEngineRunning"] = float(checkPath(client, "Vehicle.Drivetrain.FuelSystem.TimeSinceEngineRunning"))
    binPro.signals["TotalDistanceECM"] = checkPath(client, "Vehicle.TotalVehicleDistance")
    binPro.signals["TimeSinceECUDTCErase"] = checkPath(client, "Vehicle.OBD.TimeSinceECUDTCErase")
    binPro.signals["DistanceSinceECUDTCErase"] = checkPath(client, "Vehicle.OBD.DistanceSinceECUDTCErase")
    binPro.signals["ECUCVN"] = checkPath(client, "Vehicle.OBD.ECUCVN")
    binPro.signals["ECUTamperingProbability"] = checkPath(client, "Vehicle.OBD.ECUTamperingProbability")
    binPro.signals["ECUTamperingProbabilityAuthentication"] = checkPath(client, "Vehicle.Authentication.ECUTamperingProbabilityAuthentication")
    binPro.signals["UpstreamNOxSecOC"] = float(checkPath(client, "Vehicle.AfterTreatment.NOxLevel.UpstreamNOxSecOC"))
    binPro.signals["UpstreamNOxSecOCAuthentication"] = checkPath(client, "Vehicle.Authentication.UpstreamNOxSecOCAuthentication")
    
    #DM1_ECM
    binPro.signals["MalfunctionIndicatorLampStatus"] = float(checkPath(client, "Vehicle.OBD.FaultDetectionSystem.MalfunctionIndicatorLampStatus"))
    #binPro.signals["AmberWarningLampStatus"] = checkPath(client, "Vehicle.OBD.FaultDetectionSystem.AmberWarningLampStatus")
    #binPro.signals["RedStopLampState"] = checkPath(client, "Vehicle.OBD.FaultDetectionSystem.RedStopLampState")
    #binPro.signals["ProtectLampStatus"] = checkPath(client, "Vehicle.OBD.FaultDetectionSystem.ProtectLampStatus")
    #binPro.signals["FlashMalfuncIndicatorLamp"] = checkPath(client, "Vehicle.OBD.FaultDetectionSystem.FlashMalfuncIndicatorLamp")
    #binPro.signals["FlashAmberWarningLamp"] = checkPath(client, "Vehicle.OBD.FaultDetectionSystem.FlashAmberWarningLamp")
    #binPro.signals["FlashRedStopLamp"] = checkPath(client, "Vehicle.OBD.FaultDetectionSystem.FlashRedStopLamp")
    #binPro.signals["FlashProtectLamp"] = checkPath(client, "Vehicle.OBD.FaultDetectionSystem.FlashProtectLamp")
    binPro.signals["DTCList"] = checkPath(client, "Vehicle.OBD.FaultDetectionSystem.DTCList")
    
    #TimeStamp
    binPro.signals["TimeYear"] = int(float(checkPath(client, "Vehicle.OBD.DateTime.Year")))
    binPro.signals["TimeMonth"] = int(float(checkPath(client, "Vehicle.OBD.DateTime.Month")))
    binPro.signals["TimeDay"] = int(float(checkPath(client, "Vehicle.OBD.DateTime.Day")))
    binPro.signals["TimeHour"] = int(float(checkPath(client, "Vehicle.OBD.DateTime.Hours")))
    binPro.signals["TimeMin"] = int(float(checkPath(client, "Vehicle.OBD.DateTime.Minutes")))
    binPro.signals["TimeSec"] = int(float(checkPath(client, "Vehicle.OBD.DateTime.Seconds")))
    binPro.signals["LocalHourOffset"] = int(float(checkPath(client, "Vehicle.OBD.DateTime.LocalHourOffset")))
    binPro.signals["LocalMinuteOffset"] = int(float(checkPath(client, "Vehicle.OBD.DateTime.LocalMinuteOffset")))

    # 3. In cases of getting negative values, set to zero
    if binPro.signals["UpstreamNOxSecOC"] < 0:
        binPro.signals["UpstreamNOxSecOC"] = 0
    if binPro.signals["Aftertreatment1OutletNOx"] < 0:
        binPro.signals["Aftertreatment1OutletNOx"] = 0

    
    #print("\n\n\n")
    # 4. Show collected signal values
#    preprocessor_bosch.printSignalValues(binPro)

    # Only sample data when ActualEngPercentTorque is bigger than NominalFrictionPercentTorque
    if binPro.signals["ActualEngPercentTorque"] > binPro.signals["NominalFrictionPercentTorque"]:

        # A. Proceed to sample data if the aftertreatment system is ready
        if binPro.signals["UpstreamNOxSecOC"] != 0.300000 and binPro.signals["Aftertreatment1OutletNOx"] != 0.301275:
            # 5. Preprocess the data set
            preprocessor_bosch.preprocessing(binPro)
            
        # B. Do not sample data if the aftertreatment system is not ready
        else:
            print("No sampling [Aftertreatment system]")
            #print("\n# One or both NOx sensors is(are) not ready (default value: 3012.75 ppm or 3000.00 ppm).\n# No bin sampling.")
    else:
        print("No sampling [Torque]")
        #print("\n# ActualEngPercentTorque must be higher than NominalFrictionPercentTorque")

    #send Updates
    tel_dict = preprocessor_bosch.sendUpdate(binPro)

    if tel_dict:
        preprocessor_bosch.printTelemetry(tel_dict)
        print("")

        # 6. Format telemetry
        tel_json = json.dumps(tel_dict)
        # Sending device data via Mosquitto_pub (MQTT - Device to Cloud)
        # comb =['mosquitto_pub', '-d', '-h', args.host, '-p', args.port, '-t', args.type, '-m', tel_json]
        # comb =['mosquitto_pub', '-d', '-h', args.host, '-p', args.port, '-u', args.username, '-P', args.password, '--cafile', args.cafile, '-t', args.type, '-m', tel_json]
        comb =['mosquitto_pub', '-d', '-h', args.host, '-p', args.port, '-u', args.username, '-P', args.password, '-t', args.type, '-m', tel_json]

        # 7. MQTT: Send telemetry to the cloud. (in a JSON format)
        send_telemetry(args.host, args.port, comb, telemetry_queue)
        # 8. Saving telemetry dictionary
    save_data(binPro, telemetry_queue)
