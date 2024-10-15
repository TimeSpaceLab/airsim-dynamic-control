import setup_path
import airsim
import time
import numpy as np
import os
import cv2
import json

client = airsim.MultirotorClient()
client.confirmConnection()

client.enableApiControl(True)
client.armDisarm(True)
client.takeoffAsync().join()


def saving_data(data, file_name, folder_path, data_type='image'):
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Created directory: {folder_path}")
        
    if data_type == 'image':
        file_path = os.path.join(folder_path, file_name + '.png')
        airsim.write_png(file_path, data)
        print(f"Data saved to {file_path}")
    elif data_type == 'meta':
        file_path = os.path.join(folder_path, file_name + '.json')
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)

def capturing_data(client, image_type):
    response = client.simGetImages([airsim.ImageRequest(3, image_type, False, False)])
    if response and isinstance(response[0], airsim.ImageResponse):
        img1d = np.frombuffer(response[0].image_data_uint8, dtype=np.uint8)
        img_rgb = img1d.reshape(response[0].height, response[0].width, 3)
        img_rgb = np.flipud(img_rgb)
        return img_rgb
    else:
        raise ValueError("No valid image response received from AirSim.")

def setting_data(client, image_index, meta_data, save_path):
    scene_image_name = f"scene_{image_index:06d}"
    scene_image_data = capturing_data(client, airsim.ImageType.Scene)
    saving_data(scene_image_data, scene_image_name, os.path.join(save_path, 'scene'), data_type='image')

    seg_image_name = f"seg_{image_index:06d}"
    seg_image_data = capturing_data(client, airsim.ImageType.Segmentation)
    saving_data(seg_image_data, seg_image_name, os.path.join(save_path, 'seg'), data_type='image')

    gps_data = client.getGpsData()
    imu_data = client.getImuData()
    meta_data.append({
        "index": image_index,
        "scene_image_name": scene_image_name,
        "seg_image_name": seg_image_name,
        "roll": airsim.to_eularian_angles(imu_data.orientation)[0],
        "pitch": airsim.to_eularian_angles(imu_data.orientation)[1],
        "yaw": airsim.to_eularian_angles(imu_data.orientation)[2],
        "latitude": gps_data.gnss.geo_point.latitude,
        "longitude": gps_data.gnss.geo_point.longitude,
        "altitude": gps_data.gnss.geo_point.altitude
    })

def starting_airsim_drone(client, waypoints, altitude, save_path='output', speed=10, interval=1000):
    client.moveToPositionAsync(0, 0, altitude, 30).join()
    meta_data = []
    image_index = 1

    for waypoint in waypoints:
        latitude, longitude = waypoint
        print(f"Moving to waypoint {image_index}: Lat: {latitude}, Lon: {longitude}, Alt: {altitude}")
        
        # 비동기적으로 이동을 시작
        next_waypoint = client.moveToGPSAsync(latitude, longitude, altitude, speed)

        start_time = time.time()
        while True:
            # 이동이 완료되었는지 확인 (is_done() 메서드를 이용)
            if next_waypoint.done():
                break

            # 지정된 시간 간격이 지났을 때 이미지 저장
            if time.time() - start_time >= interval / 1000.0:
                setting_data(client, image_index, meta_data, save_path)
                image_index += 1
                start_time = time.time()  # 다음 캡처 타이밍으로 시간 초기화

        # 도착 후 한 번 더 이미지를 저장
        setting_data(client, image_index, meta_data, save_path)
        image_index += 1

    # 메타 데이터 저장
    saving_data(meta_data, 'meta_data', save_path, data_type='meta')

if __name__ == "__main__":
    client.takeoffAsync().join()

    waypoints = [
        (37.6682, 126.7242),  
        (37.6634, 126.7213),  
        (37.6177, 126.7970),  
        (37.5959787, 126.8077136),  
        (37.5724, 126.8045)
    ]
    altitude = -450
    interval = 1000
    save_path = r'C:\Users\kim\AirSim\PythonClient\multirotor\test'

    starting_airsim_drone(client, waypoints, altitude, save_path, interval)

    client.landAsync().join()
    client.enableApiControl(False)