"""
Preprocessor / DIAS - Bosch Implementation

The script needs to be located in the same directory where cloudfeeder.py 
is also located.

"""

import math
import json
from datetime import datetime, timedelta
SAMPLETIME = 2

class T_SCR_Mode:
    Nonee, Bad, Intermediate, Good = range(4)

class BinInfoProvider:
    """A class that provides info to create a bin"""    
    def __init__(self):
        self.signals = {}
        self.ctr_total = 0
        self.ctr_tscr_good = 0
        self.ctr_tscr_intermediate = 0
        self.ctr_tscr_bad = 0
        self.start_sampling = "0001-01-01T00:00:00Z+0000"

        # a dashboard(Dictionary) with 1 maps initialized
        self.dashboard = {
                            "tscr_good": {},
                        }

        for key in self.dashboard:
            if key == "tscr_good":
                for x in range(1, 13):
                    self.dashboard[key][str(x)] = {}
                    self.dashboard[key][str(x)] = {
                        "cumulativeNOxDS_g": 0,
                        "cumulativeNOxDS_ppm": 0,
                        "cumulativeNOxUS_g": 0,
                        "cumulativeNOxUS_ppm": 0,
                        "cumulativePower_J": 0,
                        "cumulativePower_kWh": 0,
                        "samplingTime": 0,
                    }

def sendUpdate(binPro):
    tel_dict = {}
    timeStr = createTimestamp(binPro)
    start_sampling = datetime.strptime(binPro.start_sampling, "%Y-%m-%dT%H:%M:%SZ%z")
    if "0000-00-00T" not in timeStr and timeStr != "":
        timestamp = datetime.strptime(timeStr, "%Y-%m-%dT%H:%M:%SZ%z")
    else: #Invalid DateTime
        timestamp = datetime.strptime("0001-01-01T00:00:00Z+0000", "%Y-%m-%dT%H:%M:%SZ%z")
    
    if (timestamp - start_sampling)/timedelta(minutes=SAMPLETIME) >= 1:
        tel_dict = createTelemetry(binPro)
        deleteBinData(binPro)
        binPro.start_sampling = timeStr
    elif (timestamp - start_sampling)/timedelta(minutes=SAMPLETIME) < 0: #time setback or replay attack
        tel_dict = createTelemetry(binPro)
        deleteBinData(binPro)
        binPro.start_sampling = timeStr
    return tel_dict

def preprocessing(binPro):
    # Current Engine Output Torque
    curOutToq = 0
        
    temp_torque = binPro.signals["ActualEngPercentTorque"] - binPro.signals["NominalFrictionPercentTorque"]
    if temp_torque > 0:
        curOutToq = temp_torque * binPro.signals["EngReferenceTorque"] / 100 # divided by 100 because ActualEngPercentTorque - NominalFrictionPercentTorque is in percentage
    ## Cumulative NOx (DownStream) in g
    noxDS_gs = 0.001588 * (binPro.signals["Aftertreatment1OutletNOx"]*10000) * (binPro.signals["Aftrtratment1ExhaustGasMassFlow"]*36/10) / 3600
    ## Cumulative NOx (UpStream) in g
    noxUS_gs = 0.001588 * (binPro.signals["UpstreamNOxSecOC"]*10000) * (binPro.signals["Aftrtratment1ExhaustGasMassFlow"]*36/10) / 3600
    # RPM = Revolutions Per Minute
    # Conversion from RPM to Revolutions Per Second: EngSpeed / 60 
    power_Js = curOutToq * binPro.signals["EngSpeed"] / 60 * 2 * math.pi

    # <assumption>
    # X-Axis: is not Engine Speed. but a percentage of: (EngSpeed-EngSpeedAtIdlePoint1) / (EngSpeedAtPoint2-EngSpeedAtIdlePoint1)
    xAxisVal = getXAxisVal(binPro.signals["EngSpeed"], binPro.signals["EngSpeedAtPoint2"], binPro.signals["EngSpeedAtIdlePoint1"])
    # Y-Axis: loadBasedOnOutToq = curOutToq / maxOutToqAvailAtCurSpeed
    yAxisVal = getYAxisVal(curOutToq, binPro.signals["ActualEngPercentTorque"], binPro.signals["EngReferenceTorque"], binPro.signals["EngPercentLoadAtCurrentSpeed"])
    binPos = selectBinPos(xAxisVal, yAxisVal)

    # Get map type info, decide the position and create a telemetry dictionary
    # * Fault active part is omitted
    # * barometric (kpa): mbar = 10 x kPa
    ## A. New Concept
    ### 1 bad / 2 intermediate / 3 good
    catEvalNum = catalystEval(binPro)

    if catEvalNum == 3:
        # T-SCR (Good) - special function.
        storeTscrGoodMetrics(noxDS_gs, noxUS_gs, power_Js, "tscr_good", str(binPos), binPro)
    binPro.ctr_total += 1
    return

def getXAxisVal(speed, hsGovKickInSpeed, idleSpeed):
    numerator = speed - idleSpeed
    denominator = hsGovKickInSpeed - idleSpeed
    if denominator == 0.0:
        return 0.0
    curEngSpeed = numerator / denominator * 100 # multiply by 100 to be in percentage
    if curEngSpeed > 100:
        curEngSpeed = 100.0
    elif curEngSpeed < 0:
        # print("The current speed can not be smaller than the engine speed at idle.")
        # print("The engine speed at high speed governor kick in point can not be equal or smaller than the engine speed at idle.")
        curEngSpeed = 0.0
    return curEngSpeed
    
def getYAxisVal(curOutToq, actualEngPercentTorque, engReferenceTorque, engPercentLoadAtCurrentSpeed):
    # Maximum Engine Output Torque Available At Current Speed
    if engPercentLoadAtCurrentSpeed != 0:
        maxOutToqAvailAtCurSpeed = actualEngPercentTorque * engReferenceTorque / engPercentLoadAtCurrentSpeed
    else:
        return 0
    if maxOutToqAvailAtCurSpeed == 0:
        return 0
    # Engine Load based on Output Torque
    loadBasedOnOutToq = curOutToq / maxOutToqAvailAtCurSpeed * 100 # multiply by 100 to be in percentage
    if loadBasedOnOutToq > 100:
        loadBasedOnOutToq = 100.0
    elif loadBasedOnOutToq < 0:
        loadBasedOnOutToq = 0.0
    return loadBasedOnOutToq

def selectBinPos(xAxisVal, yAxisVal):
    # Check X-axis first and then Y-axis
    if xAxisVal < 25:
        if yAxisVal < 33:
            return 1
        elif 33 <= yAxisVal <= 66:
            return 5
        elif 66 < yAxisVal:
            return 9
    elif 25 <= xAxisVal < 50:
        if yAxisVal < 33:
            return 2
        elif 33 <= yAxisVal <= 66:
            return 6
        elif 66 < yAxisVal:
            return 10
    elif 50 <= xAxisVal < 75:
        if yAxisVal < 33:
            return 3
        elif 33 <= yAxisVal <= 66:
            return 7
        elif 66 < yAxisVal:
            return 11
    elif 75 <= xAxisVal:
        if yAxisVal < 33:
            return 4
        elif 33 <= yAxisVal <= 66:
            return 8
        elif 66 < yAxisVal:
            return 12
    return 0

def catalystEval(binPro):
    timeAfterEngStart = binPro.signals["TimeSinceEngineRunning"]
    tAmbient = binPro.signals["AmbientAirTemp"]
    pAmbient = binPro.signals["BarometricPress"] * 10
    tSCR = binPro.signals["Aftrtrtmnt1SCRCtlystIntkGasTemp"]
    isMILon = binPro.signals["MalfunctionIndicatorLampStatus"]
    if timeAfterEngStart <= 180 or tAmbient < -7 or pAmbient < 750 or isMILon != 0 or tSCR < 180:
        binPro.ctr_tscr_bad += 1
        print(f"Bad: tAmbient: {tAmbient}, Enigne start: {timeAfterEngStart}, pAmbient: {pAmbient}, MIL: {isMILon}, tSCR: {tSCR}")
        return T_SCR_Mode.Bad
    elif timeAfterEngStart > 180 and tAmbient >= -7 and pAmbient >= 750 and isMILon == 0:
        if 180 <= tSCR < 220:
            binPro.ctr_tscr_intermediate += 1
            print(f"Intermediate: tAmbient: {tAmbient}, Enigne start: {timeAfterEngStart}, pAmbient: {pAmbient}, MIL: {isMILon}, tSCR: {tSCR}")
            return T_SCR_Mode.Intermediate
        elif tSCR >= 220:
            binPro.ctr_tscr_good += 1
            print(f"Good: tAmbient: {tAmbient}, Enigne start: {timeAfterEngStart}, pAmbient: {pAmbient}, MIL: {isMILon}, tSCR: {tSCR}")
            return T_SCR_Mode.Good
    
    print(f"None: tAmbient: {tAmbient}, Enigne start: {timeAfterEngStart}, pAmbient: {pAmbient}, MIL: {isMILon}, tSCR: {tSCR}")
    return T_SCR_Mode.Nonee

def storeTscrGoodMetrics(noxDS_gs, noxUS_gs, power_Js, mapKeyword, binPos, binPro):
    # Cumulative NOx (DownStream) in g
    binPro.dashboard[mapKeyword][binPos]['cumulativeNOxDS_g'] += noxDS_gs
    # Cumulative NOx (DownStream) in ppm
    binPro.dashboard[mapKeyword][binPos]['cumulativeNOxDS_ppm'] += binPro.signals["Aftertreatment1OutletNOx"] * 10000
    # Cumulative NOx (UpStream) in g
    binPro.dashboard[mapKeyword][binPos]['cumulativeNOxUS_g'] += noxUS_gs
    # Cumulative NOx (UpStream) in ppm
    binPro.dashboard[mapKeyword][binPos]['cumulativeNOxUS_ppm'] += binPro.signals["UpstreamNOxSecOC"] * 10000
    # Cumulative Work in J
    binPro.dashboard[mapKeyword][binPos]['cumulativePower_J'] += power_Js
    # Cumulative Work in kWh
    binPro.dashboard[mapKeyword][binPos]['cumulativePower_kWh'] += convertJoulesToKWh(power_Js)
    # Cumulative Sampling Time
    binPro.dashboard[mapKeyword][binPos]['samplingTime'] += 1

def deleteBinData(binPro):    
    for x in range(1, 13):
        binPro.dashboard["tscr_good"][str(x)] = {}
        binPro.dashboard["tscr_good"][str(x)] = {
            "cumulativeNOxDS_g": 0,
            "cumulativeNOxDS_ppm": 0,
            "cumulativeNOxUS_g": 0,
            "cumulativeNOxUS_ppm": 0,
            "cumulativePower_J": 0,
            "cumulativePower_kWh": 0,
            "samplingTime": 0,
        }

def convertJoulesToKWh(joules):
    # 1 kW = 1000 J, 1 kWh = 1000 J * 3600
    # 1 kWh = 3600000 J, 1 J = 1 / 3600000 kWh
    denominator = 3600000
    return joules / denominator
    
def createTimestamp(binPro):
    year = "{:>04d}".format(binPro.signals["TimeYear"])
    month = "{:>02d}".format(binPro.signals["TimeMonth"])
    day = "{:>02d}".format(binPro.signals["TimeDay"])
    hour = "{:>02d}".format(binPro.signals["TimeHour"])
    min = "{:>02d}".format(binPro.signals["TimeMin"])
    sec = "{:>02d}".format(binPro.signals["TimeSec"])
    hourOff = "{:>02d}".format(binPro.signals["LocalHourOffset"])
    minOff = "{:>02d}".format(binPro.signals["LocalMinuteOffset"])
    if '-' in hourOff:
        sign = ""
    else:
        sign = "+"
    return "" + year + "-" + month + "-" + day + "T" + hour + ":" + min + ":" + sec + "Z" + sign + hourOff + minOff
    
    

def createTelemetry(binPro):
    tel_dict = {}
    tel_dict["metadata"] = {}
    tel_dict["metadata"]["timestamp"] = createTimestamp(binPro)
    tel_dict["metadata"]["total_sampling"] = binPro.ctr_total
    tel_dict["metadata"]["tSCR_good"] = binPro.ctr_tscr_good
    tel_dict["metadata"]["tSCR_intermediate"] = binPro.ctr_tscr_intermediate
    tel_dict["metadata"]["tSCR_bad"] = binPro.ctr_tscr_bad

    tel_dict["metadata"]["total_Distance_ECM"] = binPro.signals["TotalDistanceECM"]
    tel_dict["metadata"]["time_Since_ECU_DTC_Erase"] = binPro.signals["TimeSinceECUDTCErase"]
    tel_dict["metadata"]["distance_Since_ECU_DTC_Erase"] = binPro.signals["DistanceSinceECUDTCErase"]
    tel_dict["metadata"]["ECU_CVN"] = binPro.signals["ECUCVN"]
    tel_dict["metadata"]["ECU_Tampering_Probability"] = binPro.signals["ECUTamperingProbability"]
    tel_dict["metadata"]["ECU_Tampering_Probability_Authentication"] = binPro.signals["ECUTamperingProbabilityAuthentication"]
    tel_dict["metadata"]["upstreamNOx_SecOC_Authentication"] = binPro.signals["UpstreamNOxSecOCAuthentication"]
    tel_dict["metadata"]["DTC_List"] = binPro.signals["DTCList"]

    
    tel_dict["tscr_good"] = {}
    for x in range(1,13):
        if binPro.dashboard["tscr_good"][str(x)]["samplingTime"] != 0:
            tel_dict["tscr_good"][str(x)] = binPro.dashboard["tscr_good"][str(x)]
            tel_dict["tscr_good"][str(x)]["cumulativeNOxDS_ppm"] = tel_dict["tscr_good"][str(x)]["cumulativeNOxDS_ppm"]/binPro.dashboard["tscr_good"][str(x)]["samplingTime"]
            tel_dict["tscr_good"][str(x)]["cumulativeNOxUS_ppm"] = tel_dict["tscr_good"][str(x)]["cumulativeNOxUS_ppm"]/binPro.dashboard["tscr_good"][str(x)]["samplingTime"]
         
    return tel_dict

def printSignalValues(binPro):
    print("######################## Signals ########################")
    for signal, value in binPro.signals.items():
        print(signal, ": ", str(value))

def printTelemetry(telemetry):
    print("####################### Telemetry #######################")
    print(json.dumps(telemetry, indent=2))
