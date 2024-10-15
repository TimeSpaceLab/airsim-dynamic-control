import setup_path
import airsim
import time
import numpy as np
import os
import cv2
import json
import time


client = airsim.MultirotorClient()
client.confirmConnection()

client.enableApiControl(True)
client.armDisarm(True)




client.takeoffAsync().join()




client.startRecording()

client.moveToPositionAsync(0, 0, -450, 30).join()


waypoints = [
    (37.5226, 126.9171),  
    (37.5241, 126.9288),  
    (37.5437627, 126.9046052)
    # ,  
    # (37.5959787, 126.8077136),  
    # (37.5724, 126.8045)
]
altitude = 450
speed = 5

for waypoint in waypoints:
    latitude, longitude = waypoint
    print(f"Moving to Lat: {latitude}, Lon: {longitude}")
    client.moveToGPSAsync(latitude, longitude, altitude, speed).join()

# Recording 중지
client.stopRecording()

# 드론 착륙
client.landAsync().join()

client.armDisarm(False)
client.enableApiControl(False)