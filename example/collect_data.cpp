/*****************************************************************
 Copyright (c) 2020, Unitree Robotics.Co.Ltd. All rights reserved.
******************************************************************/

#include "unitree_legged_sdk/unitree_legged_sdk.h"
#include <math.h>
#include <iostream>
#include <stdio.h>
#include <stdint.h>
#include <fstream>
#include <unistd.h>
#include <sys/stat.h>

using namespace std;
using namespace UNITREE_LEGGED_SDK;

class Custom
{
public:
    Custom(uint8_t level): 
        safe(LeggedType::Go1), 
        udp(level, 8090, "192.168.123.10", 8007) {
        udp.InitCmdData(cmd);
    }
    void UDPRecv();
    void UDPSend();
    void RobotData();

    Safety safe;
    UDP udp;
    LowCmd cmd = {0};
    LowState state = {0};
    int motiontime = 0;
    float dt = 0.002;     // 0.001~0.01
};

void Custom::UDPRecv()
{  
    udp.Recv();
}

void Custom::UDPSend()
{  
    udp.Send();
}

void Custom::RobotData() 
{
    motiontime++;
    udp.GetRecv(state);
    // time
    std::cout << motiontime*dt << " ";
    // q
    std::cout << state.motorState[0].q << " " << state.motorState[1].q << " " << state.motorState[2].q << " ";
    std::cout << state.motorState[3].q << " " << state.motorState[4].q << " " << state.motorState[5].q << " ";
    std::cout << state.motorState[6].q << " " << state.motorState[7].q << " " << state.motorState[8].q << " "; 
    std::cout << state.motorState[9].q << " " << state.motorState[10].q << " " << state.motorState[11].q << " ";
    // dq
    std::cout << state.motorState[0].dq << " " << state.motorState[1].dq << " " << state.motorState[2].dq << " ";
    std::cout << state.motorState[3].dq << " " << state.motorState[4].dq << " " << state.motorState[5].dq << " ";
    std::cout << state.motorState[6].dq << " " << state.motorState[7].dq << " " << state.motorState[8].dq << " ";
    std::cout << state.motorState[9].dq << " " << state.motorState[10].dq << " " << state.motorState[11].dq << " ";
    // tau
    std::cout << state.motorState[0].tauEst << " " << state.motorState[1].tauEst << " " << state.motorState[2].tauEst << " ";
    std::cout << state.motorState[3].tauEst << " " << state.motorState[4].tauEst << " " << state.motorState[5].tauEst << " ";
    std::cout << state.motorState[6].tauEst << " " << state.motorState[7].tauEst << " " << state.motorState[8].tauEst << " ";
    std::cout << state.motorState[9].tauEst << " " << state.motorState[10].tauEst << " " << state.motorState[11].tauEst << " ";
    // IMU
    std::cout << state.imu.accelerometer[0] << " " << state.imu.accelerometer[1] << " " << state.imu.accelerometer[2] << " ";
    std::cout << state.imu.gyroscope[0] << " " << state.imu.gyroscope[1] << " " << state.imu.gyroscope[2] << " ";
    // Force
    std::cout << state.footForce[0] << " " << state.footForce[1] << " " << state.footForce[2] << " " << state.footForce[3] << std::endl;

}


int main(void)
{

    // create a directory for the logs witht the current date and time
    std::string date = "date +%Y-%m-%d_%H-%M-%S";
    // do not use exec
    FILE* datepipe = popen(date.c_str(), "r");
    if (!datepipe) {
        std::cerr << "Failed to open pipe\n";
        return 1;
    }
    char date_str[100];
    fgets(date_str, 100, datepipe);
    pclose(datepipe);
    date_str[strlen(date_str)-1] = '\0'; // remove the newline character
    std::string dir = "../logs/" + std::string(date_str);
    // use mkdir
    if (mkdir(dir.c_str(), 0777) == -1) {
        std::cerr << "Failed to create directory\n";
        return 1;
    }


    std::cout << "Communication level is set to LOW-level." << std::endl
              << "WARNING: Make sure the robot is hung up." << std::endl
              << "Press Enter to continue..." << std::endl;
    std::cin.ignore();

    std::ofstream logfile(dir + "/go1.log");

    if (!logfile) {
        std::cerr << "Failed to open log file\n";
        return 1;
    }

    std::cout << "Log file opened successfully. Press Enter to start logging...\n"; 
    std::cin.ignore();

    // redirect standard output to the log file
    std::streambuf* coutbuf = std::cout.rdbuf();

    Custom custom(LOWLEVEL);
    // InitEnvironment();
    LoopFunc loop_data("data_loop", custom.dt,    boost::bind(&Custom::RobotData, &custom));
    LoopFunc loop_udpSend("udp_send",     custom.dt, 3, boost::bind(&Custom::UDPSend,      &custom));
    LoopFunc loop_udpRecv("udp_recv",     custom.dt, 3, boost::bind(&Custom::UDPRecv,      &custom));

    loop_udpSend.start();
    loop_udpRecv.start();
    loop_data.start();

    std::cout << std::endl << "Started logging...\n";

    std::cout.rdbuf(logfile.rdbuf());

    std::cout << "time q_FL_hip q_FL_thigh q_FL_calf q_FR_hip q_FR_thigh q_FR_calf q_RL_hip q_RL_thigh q_RL_calf q_RR_hip q_RR_thigh q_RR_calf dq_FL_hip dq_FL_thigh dq_FL_calf dq_FR_hip dq_FR_thigh dq_FR_calf dq_RL_hip dq_RL_thigh dq_RL_calf dq_RR_hip dq_RR_thigh dq_RR_calf tau_FL_hip tau_FL_thigh tau_FL_calf tau_FR_hip tau_FR_thigh tau_FR_calf tau_RL_hip tau_RL_thigh tau_RL_calf tau_RR_hip tau_RR_thigh tau_RR_calf IMU_acc_x IMU_acc_y IMU_acc_z IMU_gyro_x IMU_gyro_y IMU_gyro_z FL_force FR_force RL_force RR_force" << std::endl;

    while(1){
        sleep(1);
    };

    std::cout.rdbuf(coutbuf);

    return 0; 
}
