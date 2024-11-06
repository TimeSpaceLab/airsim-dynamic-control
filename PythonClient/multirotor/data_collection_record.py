import setup_path
import airsim
import time
import numpy as np
import os
import cv2
import json
import time

#Airsim 연결
client = airsim.MultirotorClient()
client.confirmConnection()

client.enableApiControl(True)
client.armDisarm(True)



#드론 이륙 
client.takeoffAsync().join()



#AirSim Recording API 시작
client.startRecording()

#목표한 고도까지 30m/s의 속도로 상승
client.moveToPositionAsync(0, 0, -200, 30).join()

#드론이 이동할 현실세계 위도, 경도
waypoints = [
    (37.5226, 126.9171),  
    (37.5241, 126.9288),  
    (37.5437627, 126.9046052)
    # ,  
    # (37.5959787, 126.8077136),  
    # (37.5724, 126.8045)
]

#목표하는 고도
#28줄의 client.moveToPositionAsync(0, 0, -200, 30).join()에서는 z축 좌표가 음수로 되어있는 것은 moveToPositionAsync함수는 Unreal Engine의 좌표계를 기준으로 작동하는 API이기 때문에 
# Unreal Engine의 좌표계의 맞춰 z축 좌표를 음수로 만든 것
#moveToGPSAsync에 이용할 altitude 변수는 음수로 만들면 현실세계 좌표계에 따라서 상승하는 것이 아닌 하강하므로 양수로 지정할 것
altitude = 200

#드론의 이동속도
speed = 5

#드론의 좌표간 이동
for waypoint in waypoints:
    latitude, longitude = waypoint
    
    #드론 이동 시 이동하는 위도와 경도를 출력
    print(f"Moving to Lat: {latitude}, Lon: {longitude}")

    #진행방향과 드론의 front 방향이 일치하도록 하는 코드
    client.moveToGPSAsync(latitude, longitude, altitude, speed, 3e+38, airsim.DrivetrainType.ForwardOnly, airsim.YawMode(False,0)).join() 

    #드론이 정북방향으로 이동하도록 하는 코드
    #client.moveToGPSAsync(latitude, longitude, altitude, speed).join()


# Recording 중지
client.stopRecording()

# 드론 착륙
client.landAsync().join()

#AirSim 연결 해제
client.armDisarm(False)
client.enableApiControl(False)