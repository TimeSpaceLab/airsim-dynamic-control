import setup_path
import airsim
import time
import numpy as np
import os
import cv2

height = 1040
width = 1980


client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)


client.takeoffAsync().join()
CAM_NAME = 3
print(f"Camera: {CAM_NAME}")
cam_info = client.simGetCameraInfo(CAM_NAME)
client.simSetCameraFov(CAM_NAME, 50)
print(cam_info)



def capture_bottom_image(client, position, image_name):
    client.moveToPositionAsync(position[0], position[1], position[2], 5).join()
    hovering(client)


    responses = client.simGetImages([
        airsim.ImageRequest(CAM_NAME, airsim.ImageType.Scene, False, False)
    ])

    response = responses[0]
    img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8)


    img_rgb = img1d.reshape(response.height, response.width, 3)

    img_resized = cv2.resize(img_rgb, (width, height))


    img_resized = np.flipud(img_resized)
    img_rgb = np.flipud(img_rgb)


    airsim.write_png(os.path.normpath(image_name + '.png'), img_rgb)
    print(f"Image saved to {image_name}.png")
    client.hoverAsync().join()

def capture_segmentation_image(client, position, image_name):
    client.moveToPositionAsync(position[0], position[1], position[2], 5).join()
    hovering(client)


    responses = client.simGetImages([
        airsim.ImageRequest(CAM_NAME, airsim.ImageType.Segmentation, False, False)
    ])

    response = responses[0]
    img1d = np.fromstring(response.image_data_uint8, dtype=np.uint8)

 
    img_rgb = img1d.reshape(response.height, response.width, 3)


    img_rgb = np.flipud(img_rgb)


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
altitude = -200  # 고도 (음수 값이 위로 올라가는 방향)

side_length = 200  # 사각형 한 변의 길이
step_size = 200     # 각 경로 간 이동 간격/
num_squares = 10   # 여러 겹의 사각형 생성

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

client.hoverAsync().join()