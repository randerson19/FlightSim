# -*- coding: utf-8 -*-
"""
Created on Mon Jun 17 09:43:44 2019

@author: Riley
"""


import requests
import xml.etree.ElementTree as ET
import time
import re
import numpy as np

headers = {'soapaction': 'InjectUAVControllerInterface',
               'content-type': "text/xml;charset='UTF-8'",
               'Connection': 'Keep-Alive'}


class FlightAxis():
    # TODO xml strings as class variables
    controller_reset = """<?xml version='1.0'encoding='UTF-8'?>
    <soap:Envelope
        xmlns:soap='http://schemas.xmlsoap.org/soap/envelope/'
        xmlns:xsd='http://www.w3.org/2001/XMLSchema'
        xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance'>
        <soap:Body>
            <RestoreOriginalControllerDevice>
                <a>1</a>
                <b>2</b>
            </RestoreOriginalControllerDevice>
        </soap:Body>
    </soap:Envelope>"""

    controller_connect = """<?xml version='1.0'encoding='UTF-8'?>
    <soap:Envelope
        xmlns:soap='http://schemas.xmlsoap.org/soap/envelope/'
        xmlns:xsd='http://www.w3.org/2001/XMLSchema'
        xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance'>
        <soap:Body>
            <InjectUAVControllerInterface>
                <a>1</a>
                <b>2</b>
            </InjectUAVControllerInterface>
        </soap:Body>
    </soap:Envelope>"""
    
    def __init__(self):
        self._state = {}

    def connect(self):
        # TODO: connect post request
        requests.post('http://127.0.0.1:18083', \
                      data = self.controller_connect, headers = headers)
        
    def disconnect(self):
        # TODO disconnect post request
        requests.post('http://127.0.0.1:18083', \
                      data = self.controller_reset, headers = headers)

    def setControls(self, controls):
        assert len(controls) == 12

        # TODO: build the post request string
        flight_setup = """<?xml version='1.0' encoding='UTF-8'?>
                <soap:Envelope
                    xmlns:soap='http://schemas.xmlsoap.org/soap/envelope/'
                    xmlns:xsd='http://www.w3.org/2001/XMLSchema'
                    xmlns:xsi='http://www.w3.org/2001/XMLSchema-instance'>
                    <soap:Body>
                        <ExchangeData>
                            <pControlInputs>
                                <m-selectedChannels>4095</m-selectedChannels>
                                <m-channelValues-0to1>
                                    <item>%.4f</item>
                                    <item>%.4f</item>
                                    <item>%.4f</item>
                                    <item>%.4f</item>
                                    <item>%.4f</item>
                                    <item>%.4f</item>
                                    <item>%.4f</item>
                                    <item>%.4f</item>
                                    <item>%.4f</item>
                                    <item>%.4f</item>
                                    <item>%.4f</item>
                                    <item>%.4f</item>
                                </m-channelValues-0to1>
                            </pControlInputs>
                        </ExchangeData>
                    </soap:Body>
                </soap:Envelope>""" % \
                (controls[0],controls[1],controls[2],controls[3],controls[4],\
                 controls[5],controls[6],controls[7],controls[8],controls[9],\
                 controls[10],controls[11])
        # send it and get the response
        vals_post = requests.post('http://127.0.0.1:18083', \
                                    data = flight_setup, headers = headers)
        # parse the response and update self._state
        root = ET.fromstring(vals_post.text)
        for elem in root.iter():
            if elem.tag == 'm-airspeed-MPS':
                m_airspeed_MPS = elem.text
                self._state['m-airspeed-MP'] = m_airspeed_MPS
            elif elem.tag == 'm-altitudeASL-MTR':
                m_altitudeASL_MTR = elem.text
                self._state['m-altitudeASL-MTR'] = m_altitudeASL_MTR
            elif elem.tag == 'm-altitudeAGL-MT':
                m_altitudeAGL_MTR = elem.text
                self._state['m-altitudeAGL-MTR'] = m_altitudeAGL_MTR
            elif elem.tag == 'm-groundspeed-MPS':
                m_groundspeed_MPS = elem.text
                self._state['m-groundspeed-MPS'] = m_groundspeed_MPS
            elif elem.tag == 'm-pitchRate-DEGpSEC':
                m_pitchRate_DEGpSEC = elem.text
                self._state['m-pitchRate-DEGpSEC'] = m_pitchRate_DEGpSEC
            elif elem.tag == 'm-rollRate-DEGpSEC':
                m_rollRate_DEGpSEC = elem.text
                self._state['m-rollRate-DEGpSEC'] = m_rollRate_DEGpSEC
            elif elem.tag == 'm-yawRate-DEGpSEC':
                m_yawRate_DEGpSEC = elem.text
                self._state['"m-yawRate-DEGpSEC'] = m_yawRate_DEGpSEC
            elif elem.tag == 'm-azimuth-DEG':
                m_azimuth_DEG = elem.text
                self._state['m-azimuth-DEG'] = m_azimuth_DEG
            elif elem.tag == 'm-inclination-DEG':
               m_inclination_DEG = elem.text
               self._state['m-inclination-DEG'] = m_inclination_DEG
            elif elem.tag == 'm-roll-DEG':
               m_roll_DEG = elem.text
               self._state['m-roll-DEG'] = m_roll_DEG
            elif elem.tag == 'm-aircraftPositionX-MTR':
                m_aircraftPositionX_MTR = elem.text
                self._state['m-aircraftPositionX-MTR'] = m_aircraftPositionX_MTR
            elif elem.tag == 'm-aircraftPositionY-MTR':
               m_aircraftPositionY_MTR = elem.text
               self._state['m-aircraftPositionY-MTR'] = m_aircraftPositionY_MTR
            elif elem.tag == 'm-velocityWorldU-MPS':
                m_velocityWorldU_MPS = elem.text
                self._state['m-velocityWorldU-MPS'] = m_velocityWorldU_MPS
            elif elem.tag == 'm-velocityWorldV-MPS':
               m_velocityWorldV_MPS = elem.text
               self._state['m-velocityWorldV-MPS'] = m_velocityWorldV_MPS
            elif elem.tag == 'm-velocityWorldW-MPS':
               m_velocityWorldW_MPS = elem.text
               self._state['m-velocityWorldW-MPS'] = m_velocityWorldW_MPS
            elif elem.tag == 'm-velocityBodyU-MPS':
                m_velocityBodyU_MPS = elem.text
                self._state['m-velocityBodyU-MPS'] = m_velocityBodyU_MPS
            elif elem.tag == 'm-velocityBodyV-MPS':
                m_velocityBodyV_MPS = elem.text
                self._state['m-velocityBodyV-MPS'] = m_velocityBodyV_MPS
            elif elem.tag == 'm-velocityBodyW-MPS':
               m_velocityBodyW_MPS = elem.text
               self._state['m-velocityBodyW-MPS'] = m_velocityBodyW_MPS
            elif elem.tag == 'm-accelerationWorldAX-MPS2':
               m_accelerationWorldAX_MPS2 = elem.text
               self._state['m-accelerationWorldAX-MPS2'] = \
               m_accelerationWorldAX_MPS2
            elif elem.tag == 'm-accelerationWorldAY-MPS2':
               m_accelerationWorldAY_MPS2 = elem.text
               self._state['m-accelerationWorldAY-MPS2'] = \
               m_accelerationWorldAY_MPS2
            elif elem.tag == 'm-accelerationWorldAZ-MPS2':
               m_accelerationWorldAZ_MPS2 = elem.text
               self._state['m-accelerationWorldAY-MPS2'] = \
               m_accelerationWorldAZ_MPS2
            elif elem.tag == 'm-accelerationBodyAX-MPS2':
                m_accelerationBodyAX_MPS2 = elem.text
                self._state['m-accelerationBodyAX-MPS2'] = \
                m_accelerationBodyAX_MPS2
            elif elem.tag == 'm-accelerationBodyAY-MPS2':
                m_accelerationBodyAY_MPS2 = elem.text
                self._state['m-accelerationBodyAY-MPS2'] = \
                m_accelerationBodyAY_MPS2
            elif elem.tag == 'm-accelerationBodyAZ-MPS2':
                m_accelerationBodyAZ_MPS2 = elem.text
                self._state['m-accelerationBodyAZ-MPS'] = m_accelerationBodyAZ_MPS2
            elif elem.tag == 'm-windX-MPS':
                m_windX_MPS = elem.text
                self._state['m-windX-MPS'] = m_windX_MPS
            elif elem.tag == 'm-windY-MPS':
               m_windY_MPS = elem.text
               self._state['m-windY-MPS'] = m_windY_MPS
            elif elem.tag == 'm-windZ-MPS':
               m_windZ_MPS = elem.text
               self._state['m-windZ-MPS'] = m_windZ_MPS
            elif elem.tag == 'm-propRPM':
                m_propRPM = elem.text
                self._state['m-propRPM'] = m_propRPM
            elif elem.tag == 'm-heliMainRotorRPM':
               m_heliMainRotorRPM = elem.text
               self._state['m-heliMainRotorRPM'] = m_heliMainRotorRPM
            elif elem.tag == 'm-batteryVoltage-VOLTS':
                m_batteryVoltage_VOLTS = elem.text
                self._state['m-batteryVoltage-VOLTS'] = m_batteryVoltage_VOLTS
            elif elem.tag == 'm-batteryCurrentDraw-AMPS':
                m_batteryCurrentDraw_AMPS = elem.text
                self._state['m-batteryCurrentDraw-AMPS'] = \
                m_batteryCurrentDraw_AMPS
            elif elem.tag == 'm-batteryRemainingCapacity-MAH':
               m_batteryRemainingCapacity_MAH = elem.text
               self._state['m-batteryRemainingCapacity-MAH'] = \
               m_batteryRemainingCapacity_MAH
            elif elem.tag == 'm-fuelRemaining-OZ':
                m_fuelRemaining_OZ = elem.text
                self._state['m-fuelRemaining-OZ'] = m_fuelRemaining_OZ
            elif elem.tag == 'm-isLocked':
                m_isLocked = elem.text
                self._state['m-isLocked'] = m_isLocked
            elif elem.tag == 'm-hasLostComponents':
               m_hasLostComponents = elem.text
               self._state['m-hasLostComponents'] = m_hasLostComponents
            elif elem.tag == 'm-anEngineIsRunning':
                m_anEngineIsRunning = elem.text
                self._state['m-anEngineIsRunning'] = m_anEngineIsRunning
            elif elem.tag == 'm-isTouchingGround':
                m_isTouchingGround = elem.text
                self._state['m-isTouchingGround'] = m_isTouchingGround
            elif elem.tag == 'm-currentAircraftStatus':
                m_currentAircraftStatus = elem.text
                self._state['m-currentAircraftStatus'] = m_currentAircraftStatus
            elif elem.tag == 'm-currentPhysicsTime-SEC':
                m_currentPhysicsTime_SEC = elem.text
                self._state['m-currentPhysicsTime-SEC'] = m_currentPhysicsTime_SEC
            elif elem.tag == 'm-currentPhysicsSpeedMultiplier':
               m_currentPhysicsSpeedMultiplier = elem.text
               self._state['m-currentPhysicsSpeedMultiplier'] = \
               m_currentPhysicsSpeedMultiplier
            elif elem.tag == 'm-orientationQuaternion-X':
                m_orientationQuaternion_X = elem.text
                self._state['m-orientationQuaternion-X'] = \
                m_orientationQuaternion_X
            elif elem.tag == 'm-orientationQuaternion-Y':
                m_orientationQuaternion_Y = elem.text
                self._state['m-orientationQuaternion-Y'] = \
                m_orientationQuaternion_Y
            elif elem.tag == 'm-orientationQuaternion-Z':
               m_orientationQuaternion_Z = elem.text
               self._state['m-orientationQuaternion-Z'] = m_orientationQuaternion_Z
            elif elem.tag == 'm-orientationQuaternion-W':
               m_orientationQuaternion_W = elem.text
               self._state['m-orientationQuaternion-W'] = m_orientationQuaternion_W
            elif elem.tag == 'm-flightAxisControllerIsActive':
                m_flightAxisControllerIsActive = elem.text
                self._state['m-flightAxisControllerIsActive'] = \
                m_flightAxisControllerIsActive
            elif elem.tag == 'm-resetButtonHasBeenPressed':
                m_resetButtonHasBeenPressed = elem.text
                self._state['m-resetButtonHasBeenPressed'] = \
                m_resetButtonHasBeenPressed

    def getStateItem(self, key):
        return self._state[key]

def constrain(x):
    # commanded alt - current. ** 0.02. if its larger than 1. throttle = 1
    if (x > 1):
        x = 1
    if (x  < -1):
        x = -1
    return x
        

class PID():
    def __init__(self, ct, kp = 0, ki = 0, kd = 0):
        self.e = 0
        self.t = ct
        self.cmd = 0
        self.int_e = 0
        self.diff_e = 0
        self.kp = kp
        self.ki = ki
        self.kd = kd
        
    def set_gains(self, kp = 0, ki = 0, kd = 0):
        pass

    def set_command(self, cmd):
        self.cmd = cmd
        
    
    def update(self, t, val, diff_e = None):
        # Store the previous e and t
        self.ep = self.e
        self.tp = self.t

        self.e = self.cmd - val
        self.t = t
        
        # TODO calculate self.int_e and self.diff_e
        self.int_e = self.int_e + (((self.e + self.ep)/2) * (self.t - self.tp))
        if diff_e is None:
            diff_e = (self.e - self.ep)/(self.t - self.tp)
        self.diff_e = diff_e
        
    def get_control(self):
        return self.kp*self.e + self.ki*self.int_e - self.kd*self.diff_e
    
    def getVars(self):
        # all the variables in the PID class
        return str((self.kp, self.ki, self.kd, self.e, self.ep, self.t,\
                    self.tp, self.cmd, self.int_e, self.diff_e))

def main():
    fa = FlightAxis()
    fa.disconnect()
    fa.connect()
    # Set every control to zero (except throttle, which goes to min)
    controls = [0]*12
    controls[2] = -1
    # Send the controls so we get our inititial state variables
    fa.setControls(controls)
    cT = float(fa.getStateItem('m-currentPhysicsTime-SEC'))
    throttle_ctrl = PID(cT, .17 , .11, .17) 
    throttle_ctrl.set_command(50)
    
    
    t = .75
    r = .1
    p = .0
    y = .0
    cmd_val = np.array([[t], [r], [p], [y]])
    mixer = np.array([[1, -1, 1, -1], [1, 1, -1, -1], [1, 1, 1, 1],\
                              [1, -1, -1, 1]])
    m_vals = np.matmul(mixer, cmd_val)
    controls[0] = m_vals[0]
    controls[1] = m_vals[1]
    controls[2] = m_vals[2]
    controls[3] = m_vals[3]
    fa.setControls(controls)
 
# =============================================================================
#     file = open("PIDVariables.csv", "w")
#     timeout = time.time() + 60
#     
#     while(True):
#         if time.time() >= timeout:
#             print(time.time())
#             file.close()
#             break
#         alt = float(fa.getStateItem('m-altitudeASL-MTR'))
#         vertical_velocity = -float(fa.getStateItem("m-velocityWorldW-MPS"))
#         t = float(fa.getStateItem('m-currentPhysicsTime-SEC'))
#         
#         throttle_ctrl.update(t, alt, vertical_velocity)
#         throttle = constrain(throttle_ctrl.get_control())
#         
#         controls[2] = throttle
#         fa.setControls(controls)
#         
#         PID_vars = re.sub('[(){}<>]', '', throttle_ctrl.getVars())
#         file.write(PID_vars + '\n')
#         print('int_e: {:>5.2f}    diff_e: {:>5.2f}     alt: {:>5.2f}'.format(
#                throttle_ctrl.int_e, throttle_ctrl.diff_e, alt), end='\n')
# =============================================================================
main()
