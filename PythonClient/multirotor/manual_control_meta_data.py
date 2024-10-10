import setup_path
import airsim
import time
import numpy as np
import os
import cv2
import json


# Airsim과 연결
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)

# 드론 이륙
client.takeoffAsync().join()

json_file = "meta_data.json"

meta_data = []

def meta_json(data, file_path):
    with open(file_path, 'w') as json_file:
        json.dump(data, json_file, indent=4)

def capture_image_and_save_data(image_name):
    gps_data = client.getGpsData()
    imu_data = client.getImuData()
    
    orientation = imu_data.orientation
    roll = airsim.to_eularian_angles(orientation)[0]
    pitch = airsim.to_eularian_angles(orientation)[1]
    yaw = airsim.to_eularian_angles(orientation)[2]
    
    latitude = gps_data.gnss.geo_point.latitude
    longitude = gps_data.gnss.geo_point.longitude
    altitude = gps_data.gnss.geo_point.altitude

    data_point = {
        "index": "kintex",
        "image_name": image_name,
        "yaw": yaw,
        "pitch": pitch,
        "roll": roll,
        "latitude": latitude,
        "longitude": longitude,
        "altitude": altitude

    }
    
    meta_data.append(data_point)

def capture_bottom_image(client, position, image_name):
    client.moveToPositionAsync(position[0], position[1], position[2], 5).join()
    hovering(client)
    capture_image_and_save_data(image_name)
    # 카메라 이미지 요청
    responses = client.simGetImages([
        airsim.ImageRequest(3, airsim.ImageType.Scene, False, False)
    ])

    response = responses[0]
    img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8)

    # reshape array to 3 channel image array H X W X 3
    img_rgb = img1d.reshape(response.height, response.width, 3)

    # original image is flipped vertically
    img_rgb = np.flipud(img_rgb)

    # write to png
    airsim.write_png(os.path.normpath(image_name + '.png'), img_rgb)
    print(f"Image saved to {image_name}.png")
    client.hoverAsync().join()

def capture_segmentation_image(client, position, image_name):
    client.moveToPositionAsync(position[0], position[1], position[2], 5).join()
    hovering(client)
    capture_image_and_save_data(image_name)

    # 세그멘테이션 이미지 요청
    responses = client.simGetImages([
        airsim.ImageRequest(3, airsim.ImageType.Segmentation, False, False)
    ])

    response = responses[0]
    img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8)

    # reshape array to 3 channel image array H X W X 3
    img_rgb = img1d.reshape(response.height, response.width, 3)

    # original image is flipped vertically
    img_rgb = np.flipud(img_rgb)

    # write to png
    airsim.write_png(os.path.normpath(image_name + '_segmentation.png'), img_rgb)
    print(f"Segmentation image saved to {image_name}_segmentation.png")
    client.hoverAsync().join()

def hovering(client):
    client.hoverAsync().join()
    time.sleep(40)

def go_front(center, front_length, altitude, step_size):
    x, y = center
    front = []
    for i in range(0, front_length, step_size):
        front.append((x + front_length, y, altitude))
        x = x + front_length
    center = x, y
    return front

def go_side(center, side_length, altitude, step_size):
    x, y = center
    side = []
    side.append((x, y - side_length, altitude))
    y = y - side_length
    center = x, y
    return side

def go_back(center, back_length, altitude, step_size):
    x, y = center
    back = []
    for i in range(0, back_length, step_size):
        back.append((x - back_length, y, altitude))
        x = x - back_length
    center = x, y
    return back

# 중심 좌표
center = (0, 0)
altitude = -450  # 고도 (음수 값이 위로 올라가는 방향)

side_length = 450  # 사각형 한 변의 길이
step_size = 450    # 각 경로 간 이동 간격/
num_squares = 1   # 여러 겹의 사각형 생성

client.moveToPositionAsync(0, 0, altitude, 10).join()

for n in range(1, num_squares + 1):
    for _ in range(num_squares + 1):
        front = go_front(center, side_length, altitude, step_size)
        for i, position in enumerate(front):
            image_name = f"front_{n}_{i+1}_{position[0]}_{position[1]}_{position[2]}"
            capture_bottom_image(client, position, image_name)  # Scene 이미지 촬영
            capture_segmentation_image(client, position, image_name)  # Segmentation 이미지 촬영
        center = front[-1][0:2]

    side = go_side(center, side_length, altitude, step_size)
    for i, position in enumerate(side):
        image_name = f"side_{n}_{i+1}_{position[0]}_{position[1]}_{position[2]}"
        capture_bottom_image(client, position, image_name)  # Scene 이미지 촬영
        capture_segmentation_image(client, position, image_name)  # Segmentation 이미지 촬영
        center = side[-1][0:2]

    for _ in range(num_squares + 1):
        back = go_back(center, side_length, altitude, step_size)
        for i, position in enumerate(back):
            image_name = f"back_{n}_{i+1}_{position[0]}_{position[1]}_{position[2]}"
            capture_bottom_image(client, position, image_name)  # Scene 이미지 촬영
            capture_segmentation_image(client, position, image_name)  # Segmentation 이미지 촬영
        center = back[-1][0:2]

meta_json(meta_data, json_file)

client.hoverAsync().join()