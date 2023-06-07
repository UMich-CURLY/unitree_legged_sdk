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
    
    udp = sdk.UDP(LOWLEVEL, 8090, "192.168.123.10", 8007)
    safe = sdk.Safety(sdk.LeggedType.Go1)
    
    cmd = sdk.LowCmd()
    state = sdk.LowState()

    # udp = sdk.UDP(HIGHLEVEL, 8080, "192.168.123.161", 8082)

    # cmd = sdk.HighCmd()
    # state = sdk.HighState()



    udp.InitCmdData(cmd)

    feet_order = ['FR', 'FL', 'RR', 'RL']

    motiontime = 0

    logging.info('time ' + ' ' +
                    ############ q ##################
                    'q_FL_hip' + ' ' + 'q_FL_thigh' + ' ' + 'q_FL_calf' + ' ' + 
                    'q_FR_hip' + ' ' + 'q_FR_thigh' + ' ' + 'q_FR_calf' + ' ' +
                    'q_RL_hip' + ' ' + 'q_RL_thigh' + ' ' + 'q_RL_calf' + ' ' +
                    'q_RR_hip' + ' ' + 'q_RR_thigh' + ' ' + 'q_RR_calf' + ' ' +
                    ############## dq ###############
                    'dq_FL_hip' + ' ' + 'dq_FL_thigh' + ' ' + 'dq_FL_calf' + ' ' +
                    'dq_FR_hip' + ' ' + 'dq_FR_thigh' + ' ' + 'dq_FR_calf' + ' ' +
                    'dq_RL_hip' + ' ' + 'dq_RL_thigh' + ' ' + 'dq_RL_calf' + ' ' +
                    'dq_RR_hip' + ' ' + 'dq_RR_thigh' + ' ' + 'dq_RR_calf' + ' ' +
                    ############## tau ##############
                    'tau_FL_hip' + ' ' + 'tau_FL_thigh' + ' ' + 'tau_FL_calf' + ' ' +
                    'tau_FR_hip' + ' ' + 'tau_FR_thigh' + ' ' + 'tau_FR_calf' + ' ' +
                    'tau_RL_hip' + ' ' + 'tau_RL_thigh' + ' ' + 'tau_RL_calf' + ' ' +
                    'tau_RR_hip' + ' ' + 'tau_RR_thigh' + ' ' + 'tau_RR_calf' + ' ' +
                    ############## IMU ##############
                    'imu.acc_x' + ' ' + 'imu.acc_y' + ' ' + 'imu.acc_z' + ' ' +
                    'imu.gyro_x' + ' ' + 'imu.gyro_y' + ' ' + 'imu.gyro_z' + ' ' +
                    ############## foot force ##############
                    'footForce_FL' + ' ' + 'footForce_FR' + ' ' + 'footForce_RL' + ' ' + 'footForce_RR' + ' ' + ' ')
                    ############## feet height ##############
                    # 'feet_pos_x_FL' + ' ' + 'feet_pos_x_FR' + ' ' + 'feet_pos_x_RL' + ' ' + 'feet_pos_x_RR' + ' ' +
                    # 'feet_pos_y_FL' + ' ' + 'feet_pos_y_FR' + ' ' + 'feet_pos_y_RL' + ' ' + 'feet_pos_y_RR' + ' ' +
                    # 'feet_pos_z_FL' + ' ' + 'feet_pos_z_FR' + ' ' + 'feet_pos_z_RL' + ' ' + 'feet_pos_z_RR' + ' ' +
                    ############## feet velocity ##############
                    # 'feet_vel_x_FL' + ' ' + 'feet_vel_x_FR' + ' ' + 'feet_vel_x_RL' + ' ' + 'feet_vel_x_RR' + ' ' +
                    # 'feet_vel_y_FL' + ' ' + 'feet_vel_y_FR' + ' ' + 'feet_vel_y_RL' + ' ' + 'feet_vel_y_RR' + ' ' +
                    # 'feet_vel_z_FL' + ' ' + 'feet_vel_z_FR' + ' ' + 'feet_vel_z_RL' + ' ' + 'feet_vel_z_RR' + ' ')
                    # ############## contact state ##############
                    # 'contact_FL' + ' ' + 'contact_FR' + ' ' + 'contact_RL' + ' ' + 'contact_RR' + ' ')


    dt = 0.001
    while True:
        time.sleep(dt)
        motiontime += 1
        udp.Recv()
        udp.GetRecv(state)
        values = str(round(motiontime*dt, 3)) + ' '
        ############ q ##################
        # for i in range(12):
        #     values += str(round(state.motorState[i].q, 3)) + ' '
        # # ############## dq ###############
        # for i in range(12):
        #     values += str(round(state.motorState[i].dq, 3)) + ' '
        # ############## tau ##############
        # for i in range(12):
        #     values += str(round(state.motorState[i].tauEst, 3)) + ' '
        # # ############## IMU ##############
        # for i in range(3):
        #     values += str(round(state.imu.accelerometer[i], 3)) + ' '
        # for i in range(3):
        #     values += str(round(state.imu.gyroscope[i], 3)) + ' '
        # ############## foot force ##############
        # for i in range(4):
        #     values += str(round(state.footForce[i], 3)) + ' '
        # now do them at the same time in one line
        values += ' '.join([str(round(state.motorState[i].q, 3)) for i in range(12)]) + ' ' + \
                    ' '.join([str(round(state.motorState[i].dq, 3)) for i in range(12)]) + ' ' + \
                    ' '.join([str(round(state.motorState[i].tauEst, 3)) for i in range(12)]) + ' ' + \
                    ' '.join([str(round(state.imu.accelerometer[i], 3)) for i in range(3)]) + ' ' + \
                    ' '.join([str(round(state.imu.gyroscope[i], 3)) for i in range(3)]) + ' ' + \
                    ' '.join([str(round(state.footForce[i], 3)) for i in range(4)]) + ' '
        




        ############## feet height ##############
        # for i in range(4):
        #     values += str(round(state.footPosition2Body[i].x, 3)) + ' '
        # for i in range(4):
        #     values += str(round(state.footPosition2Body[i].y, 3)) + ' '
        # for i in range(4):
        #     values += str(round(state.footPosition2Body[i].z, 3)) + ' '
        ############## feet velocity ##############
        # for i in range(4):
        #     values += str(round(state.footSpeed2Body[i].x, 3)) + ' '
        # for i in range(4):
        #     values += str(round(state.footSpeed2Body[i].y, 3)) + ' '
        # for i in range(4):
        #     values += str(round(state.footSpeed2Body[i].z, 3)) + ' '
            
        logging.info(values) 

        udp.Send()
