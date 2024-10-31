import os
from PIL import Image

def convert_ppm_to_jpg(ppm_folder, jpg_folder):
    if not os.path.exists(jpg_folder):
        os.makedirs(jpg_folder)

    # PPM 파일 목록 가져오기
    ppm_files = [f for f in os.listdir(ppm_folder) if f.endswith('.ppm')]
    
    for index, ppm_file in enumerate(ppm_files, start=1):
        # PPM 파일 경로
        ppm_path = os.path.join(ppm_folder, ppm_file)
        
        # 이미지 열기
        with Image.open(ppm_path) as img:
            # JPG 파일 이름 설정 (6자리로 맞춤)
            jpg_file_name = f"{str(index).zfill(6)}.jpg"
            jpg_path = os.path.join(jpg_folder, jpg_file_name)
            
            # JPG로 저장
            img.convert('RGB').save(jpg_path, 'JPEG')
            print(f"Converted {ppm_file} to {jpg_file_name}")

# 사용 예시
ppm_folder = r'C:\Users\kim\Documents\AirSim\2024-10-29-18-28-03\images'  # PPM 파일이 있는 폴더 경로
jpg_folder = r'C:\Users\kim\Documents\AirSim\사진 방향'   # 변환된 JPG 파일을 저장할 폴더 경로
convert_ppm_to_jpg(ppm_folder, jpg_folder)



#시간 20.0으로 속도는 10m/s 5m/s record api 작동시킬때 자동 생성되는 txt 파일에서 위도 경도 높이 가져올 수 있는지 확인학고 있는데 airsim documentation 사이트에서 코드 추가하면 가능하다고 나와있긴함 한번 해봐야 할듯
#랜더링 이슈는 계속 지속적으로 확인해봐야할 것 같음