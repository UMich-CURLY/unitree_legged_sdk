#!/usr/bin/python

import sys
import time
import math
import numpy as np
import logging
from datetime import datetime
import os

sys.path.append('../lib/python/amd64')
import robot_interface as sdk

now = datetime.now()

# create a folder for the log file if it does not exist with the date and time
log_path = os.path.join('../logs', now.strftime("%Y-%m-%d_%H-%M-%S"))
os.makedirs(log_path, exist_ok=True)

logging.basicConfig(filename=os.path.join(log_path, 'go1.log'), level=logging.DEBUG,format='%(message)s')

def jointLinearInterpolation(initPos, targetPos, rate):

    rate = np.fmin(np.fmax(rate, 0.0), 1.0)
    p = initPos*(1-rate) + targetPos*rate
    return p


if __name__ == '__main__':

    d = {'FR_0':0, 'FR_1':1, 'FR_2':2,
         'FL_0':3, 'FL_1':4, 'FL_2':5, 
         'RR_0':6, 'RR_1':7, 'RR_2':8, 
         'RL_0':9, 'RL_1':10, 'RL_2':11 }
    PosStopF  = math.pow(10,9)
    VelStopF  = 16000.0
    HIGHLEVEL = 0xee
    LOWLEVEL  = 0xff
    sin_mid_q = [0.0, 1.2, -2.0]
    dt = 0.002
    qInit = [0, 0, 0]
    qDes = [0, 0, 0]
    sin_count = 0
    rate_count = 0
    Kp = [0, 0, 0]
    Kd = [0, 0, 0]

    udp = sdk.UDP(LOWLEVEL, 8080, "192.168.123.10", 8007)
    safe = sdk.Safety(sdk.LeggedType.Go1)
    
    cmd = sdk.LowCmd()
    state = sdk.LowState()
    udp.InitCmdData(cmd)

    feet_order = ['FR', 'FL', 'RR', 'RL']

    motiontime = 0

    logging.info('time ' + feet_order[0] + ' ' + feet_order[1] + ' ' + feet_order[2] + ' ' + feet_order[3])

    while True:
        time.sleep(0.002)
        motiontime += 1
        udp.Recv()
        udp.GetRecv(state)
        values = str(round(motiontime, 3)) + ' '
        for i in range(4):
            values += str(round(state.footForce[i])) + ' '
        logging.info(values)

        # print("Foot Forces: FR", state.footForce[0], "FL", state.footForce[1], "RR", state.footForce[2], "RL", state.footForce[3])
        udp.Send()
