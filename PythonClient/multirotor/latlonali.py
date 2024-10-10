<<<<<<< HEAD
import setup_path
import airsim
import time
import numpy as np
import os
import cv2

client = airsim.MultirotorClient()
client.confirmConnection()

client.enableApiControl(True)
client.armDisarm(True)
client.takeoffAsync().join()

gps_data = client.getGpsData()
print(f"Current GPS location: Lat: {gps_data.gnss.geo_point.latitude}, Lon: {gps_data.gnss.geo_point.longitude}, Alt: {gps_data.gnss.geo_point.altitude}")


HG001_longitude = 126.7242
HG001_latitude = 37.6682

HG002_longitude = 126.7213
HG002_latitude = 37.6634

HG003_longitude = 126.7970
HG003_latitude = 37.6177

HG004_longitude = 126.8077136
HG004_latitude = 37.5959787

HG005_longitude = 126.8045
HG005_latitude = 37.5724
target_altitude = 450


client.moveToGPSAsync(HG001_latitude, HG001_longitude, target_altitude, 30).join()
client.hoverAsync().join()
time.sleep(20)
gps_data_after = client.getGpsData()
print(f"After move GPS location: Lat: {gps_data_after.gnss.geo_point.latitude}, Lon: {gps_data_after.gnss.geo_point.longitude}, Alt: {gps_data_after.gnss.geo_point.altitude}")


client.moveToGPSAsync(HG002_latitude, HG002_longitude, target_altitude, 30).join()
client.hoverAsync().join()
time.sleep(20)
gps_data_after = client.getGpsData()
print(f"After move GPS location: Lat: {gps_data_after.gnss.geo_point.latitude}, Lon: {gps_data_after.gnss.geo_point.longitude}, Alt: {gps_data_after.gnss.geo_point.altitude}")


client.moveToGPSAsync(HG003_latitude, HG003_longitude, target_altitude, 30).join()
client.hoverAsync().join()
time.sleep(20)
gps_data_after = client.getGpsData()
print(f"After move GPS location: Lat: {gps_data_after.gnss.geo_point.latitude}, Lon: {gps_data_after.gnss.geo_point.longitude}, Alt: {gps_data_after.gnss.geo_point.altitude}")


client.moveToGPSAsync(HG004_latitude, HG004_longitude, target_altitude, 30).join()
client.hoverAsync().join()
time.sleep(20)
gps_data_after = client.getGpsData()
print(f"After move GPS location: Lat: {gps_data_after.gnss.geo_point.latitude}, Lon: {gps_data_after.gnss.geo_point.longitude}, Alt: {gps_data_after.gnss.geo_point.altitude}")


client.moveToGPSAsync(HG005_latitude, HG005_longitude, target_altitude, 30).join()
client.hoverAsync().join()
time.sleep(20)
gps_data_after = client.getGpsData()
print(f"After move GPS location: Lat: {gps_data_after.gnss.geo_point.latitude}, Lon: {gps_data_after.gnss.geo_point.longitude}, Alt: {gps_data_after.gnss.geo_point.altitude}")


client.hoverAsync().join()

client.armDisarm(False)
=======
import setup_path
import airsim
import time
import numpy as np
import os
import cv2

client = airsim.MultirotorClient()
client.confirmConnection()

client.enableApiControl(True)
client.armDisarm(True)
client.takeoffAsync().join()

gps_data = client.getGpsData()
print(f"Current GPS location: Lat: {gps_data.gnss.geo_point.latitude}, Lon: {gps_data.gnss.geo_point.longitude}, Alt: {gps_data.gnss.geo_point.altitude}")


HG001_longitude = 126.7242
HG001_latitude = 37.6682

HG002_longitude = 126.7213
HG002_latitude = 37.6634

HG003_longitude = 126.7970
HG003_latitude = 37.6177

HG004_longitude = 126.8077136
HG004_latitude = 37.5959787

HG005_longitude = 126.8045
HG005_latitude = 37.5724
target_altitude = 450


client.moveToGPSAsync(HG001_latitude, HG001_longitude, target_altitude, 30).join()
client.hoverAsync().join()
time.sleep(20)
gps_data_after = client.getGpsData()
print(f"After move GPS location: Lat: {gps_data_after.gnss.geo_point.latitude}, Lon: {gps_data_after.gnss.geo_point.longitude}, Alt: {gps_data_after.gnss.geo_point.altitude}")


client.moveToGPSAsync(HG002_latitude, HG002_longitude, target_altitude, 30).join()
client.hoverAsync().join()
time.sleep(20)
gps_data_after = client.getGpsData()
print(f"After move GPS location: Lat: {gps_data_after.gnss.geo_point.latitude}, Lon: {gps_data_after.gnss.geo_point.longitude}, Alt: {gps_data_after.gnss.geo_point.altitude}")


client.moveToGPSAsync(HG003_latitude, HG003_longitude, target_altitude, 30).join()
client.hoverAsync().join()
time.sleep(20)
gps_data_after = client.getGpsData()
print(f"After move GPS location: Lat: {gps_data_after.gnss.geo_point.latitude}, Lon: {gps_data_after.gnss.geo_point.longitude}, Alt: {gps_data_after.gnss.geo_point.altitude}")


client.moveToGPSAsync(HG004_latitude, HG004_longitude, target_altitude, 30).join()
client.hoverAsync().join()
time.sleep(20)
gps_data_after = client.getGpsData()
print(f"After move GPS location: Lat: {gps_data_after.gnss.geo_point.latitude}, Lon: {gps_data_after.gnss.geo_point.longitude}, Alt: {gps_data_after.gnss.geo_point.altitude}")


client.moveToGPSAsync(HG005_latitude, HG005_longitude, target_altitude, 30).join()
client.hoverAsync().join()
time.sleep(20)
gps_data_after = client.getGpsData()
print(f"After move GPS location: Lat: {gps_data_after.gnss.geo_point.latitude}, Lon: {gps_data_after.gnss.geo_point.longitude}, Alt: {gps_data_after.gnss.geo_point.altitude}")


client.hoverAsync().join()

client.armDisarm(False)
>>>>>>> 9af2eb4 (updates)
client.enableApiControl(False)