<<<<<<< HEAD
import setup_path
import airsim
import time
import numpy as np
import os
import cv2

# Airsim과 연결
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)

# 드론 이륙
client.takeoffAsync().join()

def capture_bottom_image(client, position, image_name):
    client.moveToPositionAsync(position[0], position[1], position[2], 5).join()
    hovering(client)

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
    time.sleep(20)

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

def go_up(center, up_length, altitude, step_size):
    x, y = center
    z = altitude
    up = []
    for i in range(0, up_length, step_size ):
        up.append((x, y, z + (-50)))
        z = z +(-side_length)
    center = x, y
    altitude = z
    return up
up = [(0,0,-50),(0,0,-100),(0,0,-150),(0,0,-200),(0,0,-250),(0,0,-300),(0,0,-350),(0,0,-400),(0,0,-450),(0,0,-500),(0,0,-550),(0,0,-600),(0,0,-650),(0,0,-700),(0,0,-750),(0,0,-800),
      (0,0,-850),(0,0,-900),(0,0,-950),(0,0,-1000)]

center = (0, 0)
altitude = (-100)  

side_length = 50  
step_size = 50   
num_squares = 10   

client.moveToPositionAsync(0, 0, altitude, 10).join()

for n in range(1, num_squares + 1):
    for _ in range(num_squares + 1):
        for i, position in enumerate(up):
            image_name = f"up_{n}_{i+1}_{position[0]}_{position[1]}_{position[2]}"
            capture_bottom_image(client, position, image_name)  # Scene 이미지 촬영
            capture_segmentation_image(client, position, image_name)  # Segmentation 이미지 촬영
        center = 0, 0

=======
import setup_path
import airsim
import time
import numpy as np
import os
import cv2

# Airsim과 연결
client = airsim.MultirotorClient()
client.confirmConnection()
client.enableApiControl(True)

# 드론 이륙
client.takeoffAsync().join()

def capture_bottom_image(client, position, image_name):
    client.moveToPositionAsync(position[0], position[1], position[2], 5).join()
    hovering(client)

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
    time.sleep(20)

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

def go_up(center, up_length, altitude, step_size):
    x, y = center
    z = altitude
    up = []
    for i in range(0, up_length, step_size ):
        up.append((x, y, z + (-50)))
        z = z +(-side_length)
    center = x, y
    altitude = z
    return up
up = [(0,0,-50),(0,0,-100),(0,0,-150),(0,0,-200),(0,0,-250),(0,0,-300),(0,0,-350),(0,0,-400),(0,0,-450),(0,0,-500),(0,0,-550),(0,0,-600),(0,0,-650),(0,0,-700),(0,0,-750),(0,0,-800),
      (0,0,-850),(0,0,-900),(0,0,-950),(0,0,-1000)]

center = (0, 0)
altitude = (-100)  

side_length = 50  
step_size = 50   
num_squares = 10   

client.moveToPositionAsync(0, 0, altitude, 10).join()

for n in range(1, num_squares + 1):
    for _ in range(num_squares + 1):
        for i, position in enumerate(up):
            image_name = f"up_{n}_{i+1}_{position[0]}_{position[1]}_{position[2]}"
            capture_bottom_image(client, position, image_name)  # Scene 이미지 촬영
            capture_segmentation_image(client, position, image_name)  # Segmentation 이미지 촬영
        center = 0, 0

>>>>>>> 9af2eb4 (updates)
client.hoverAsync().join()