import airsim
import time
import numpy as np
import os
import json

def saving_data(data, file_name, folder_path, data_type='image'):
    """
    이미지 및 메타 데이터를 지정된 폴더에 파일로 저장하는 함수.
    :param data: 저장할 데이터 (이미지 또는 메타 데이터)
    :param file_name: 저장할 파일 이름
    :param folder_path: 파일을 저장할 폴더 경로
    :param data_type: 'image' 또는 'meta'로 파일 형식을 결정 ('image'는 PNG, 'meta'는 JSON 형식)
    """
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
        print(f"Created directory: {folder_path}")
        
    if data_type == 'image':
        # 이미지 저장 경로 설정
        file_path = os.path.join(folder_path, file_name + '.png')
        airsim.write_png(file_path, data)
        print(f"Data saved to {file_path}")
    elif data_type == 'meta':
        # 메타 데이터 저장 경로 설정
        file_path = os.path.join(folder_path, file_name + '.json')
        with open(file_path, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        # print(f"Meta info saved to {file_path}")

def capturing_data(client, image_type):
    """
    이미지를 캡처하여 메모리로 반환하는 함수.
    :param client: AirSim 클라이언트
    :param image_type: 요청할 이미지 유형 (Scene, Segmentation 등)
    :return: 이미지 데이터 (numpy array)
    """
    # 이미지 요청
    response = client.simGetImages([airsim.ImageRequest(3, image_type, False, False)])

    # 반환된 리스트에서 첫 번째 이미지 데이터에 접근
    if response and isinstance(response[0], airsim.ImageResponse):
        img1d = np.frombuffer(response[0].image_data_uint8, dtype=np.uint8)
        img_rgb = img1d.reshape(response[0].height, response[0].width, 3)
        img_rgb = np.flipud(img_rgb)  # 이미지가 상하 반전된 상태로 오기 때문에 다시 뒤집음
        return img_rgb
    else:
        raise ValueError("No valid image response received from AirSim.")


def setting_data(client, image_index, meta_data, save_path):
    """
    Scene 및 Segmentation 이미지를 캡처하고 저장하는 함수.
    :param client: AirSim 클라이언트
    :param image_index: 이미지 파일의 번호
    :param meta_data: 메타 데이터를 저장할 리스트
    :param save_path: 이미지 저장 경로
    """
    # Scene 이미지 저장
    scene_image_name = f"scene_{image_index:06d}"
    scene_image_data = capturing_data(client, airsim.ImageType.Scene)
    saving_data(scene_image_data, scene_image_name, os.path.join(save_path, 'scene'), data_type='image')

    # Segmentation 이미지 저장
    seg_image_name = f"seg_{image_index:06d}"
    seg_image_data = capturing_data(client, airsim.ImageType.Segmentation)
    saving_data(seg_image_data, seg_image_name, os.path.join(save_path, 'seg'), data_type='image')

    # 메타 데이터 수집
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

def starting_airsim_drone(client, waypoints, altitude, save_path='output', speed=30, interval=1000):
    """
    드론을 비행하고 각 지점에서 지정된 간격(밀리초)으로 Scene 및 Segmentation 이미지를 캡처하여 저장하는 함수.
    :param client: AirSim 클라이언트
    :param waypoints: [(latitude, longitude), ...] 형태의 위경도 리스트
    :param altitude: 드론의 비행 고도
    :param save_path: 파일 저장 경로
    :param speed: 드론의 이동 속도 (기본값 30)
    :param interval: 몇 밀리초마다 이미지를 저장할지에 대한 간격 (기본값 1000ms = 1초)
    """
    meta_data = []
    image_index = 1 # start index

    for waypoint in waypoints:
        latitude, longitude = waypoint
        print(f"Moving to waypoint {image_index}: Lat: {latitude}, Lon: {longitude}, Alt: {altitude}")
        
        # 드론을 해당 좌표로 이동시키기 시작
        next_waypoint = client.moveToGPSAsync(latitude, longitude, altitude, speed)

        # 이동 완료를 기다리는 동안 이미지 저장 (이동 중 이미지를 캡처하려면 loop 사용)
        start_time = time.time()
        while not next_waypoint.join():  # 작업 완료 여부를 기다림
                if time.time() - start_time >= interval / 1000.0:
                    setting_data(client, image_index, meta_data, save_path)
                    image_index += 1
                    start_time = time.time()  # 다음 간격으로 시간 초기화

        # 드론이 목표 지점에 도달한 후 한 번 더 이미지 저장
        setting_data(client, image_index, meta_data, save_path)
        image_index += 1

    # 수집된 메타 데이터 저장
    saving_data(meta_data, 'meta_data', save_path, data_type='meta')


if __name__ == "__main__":
    # AirSim과 연결
    client = airsim.MultirotorClient()
    client.confirmConnection()
    client.enableApiControl(True)

    # 드론 이륙
    client.takeoffAsync().join()

    # 경로 웨이포인트 설정
    waypoints = [
        (37.6682, 126.7242),  
        (37.6634, 126.7213),  
        (37.6177, 126.7970),  
        (37.5959787, 126.8077136),  
        (37.5724, 126.8045)   
    ]
    altitude = 450  # 기본 고도 설정
    interval = 1000  # 1000ms (1초) 간격으로 이미지 저장
    save_path = 'C:/Users/kj746/AirSim/PythonClient/multirotor/flight_mode_data'

    # 드론 주행 
    starting_airsim_drone(client, waypoints, altitude, save_path, interval)

    # 드론 착륙
    client.landAsync().join()

    # API 제어 비활성화
    client.enableApiControl(False)