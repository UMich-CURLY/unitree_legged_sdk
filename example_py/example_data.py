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

    udp = sdk.UDP(LOWLEVEL, 8090, "192.168.123.10", 8007)
    safe = sdk.Safety(sdk.LeggedType.Go1)
    
    cmd = sdk.LowCmd()
    state = sdk.LowState()
    udp.InitCmdData(cmd)

    feet_order = ['FR', 'FL', 'RR', 'RL']

    motiontime = 0

    logging.info('time ' + feet_order[0] + ' ' + feet_order[1] + ' ' + feet_order[2] + ' ' + feet_order[3] + ' ')

    # logging.info('time' + ' ' + 'acc_x' + ' ' + 'acc_y' + ' ' + 'acc_z' + 'q_FR_0' + ' ' + 'q_FR_1' + ' ' + 'q_FR_2' + 'q_FL_0' + ' ' + 'q_FL_1' + ' ' + 'q_FL_2' + 'q_RR_0' + ' ' + 'q_RR_1' + ' ' + 'q_RR_2' + 'q_RL_0' + ' ' + 'q_RL_1' + ' ' + 'q_RL_2')
    # logging.info('time' + ' ' + 'imu.acc_x' + ' ' + 'imu.acc_y' + ' ' + 'imu.acc_z' + ' ')
    while True:
        time.sleep(0.002)
        motiontime += 1
        udp.Recv()
        udp.GetRecv(state)
        values = ''
        values = str(round(motiontime*0.002, 3)) + ' '
        # for i in range(4):
            # values += str(round(state.footForce[i])) + ' '
        values += str(round(1/3.01*(state.footForce[0]-27.39))) + ' ' + str(round(1/9.65*(state.footForce[1]+81.23))) + ' ' + str(round(1/8.16*(state.footForce[2]-26.28))) + ' ' + str(round(1/9.32*(state.footForce[3]-44.25))) + ' '
            # values += str(round(state.imu.accelerometer[i], 3)) + ' '
        # for i in range(12):
        #     values += str(round(state.motorState[i].q, 3)) + ' '
        logging.info(values)

        print(values)
        
        # print the q vector from 1 to 12 on a single line
        # print("Joint Angles: ", state.motorState[0].q, state.motorState[1].q, state.motorState[2].q, state.motorState[3].q, state.motorState[4].q, state.motorState[5].q, state.motorState[6].q, state.motorState[7].q, state.motorState[8].q, state.motorState[9].q, state.motorState[10].q, state.motorState[11].q)
        # logging.info(str(round(motiontime, 3)) + ' ' + str(round(state.imu.accelerometer[0], 4)) + ' ' + str(round(state.imu.accelerometer[1], 4)) + ' ' + str(round(state.imu.accelerometer[2], 4)))
        # print("IMU data: ", state.imu.accelerometer[0], state.imu.accelerometer[1], state.imu.accelerometer[2])

        # print("Foot Forces: FR", state.footForce[0], "FL", state.footForce[1], "RR", state.footForce[2], "RL", state.footForce[3])
        #         
        udp.Send()
