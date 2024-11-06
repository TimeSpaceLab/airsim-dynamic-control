#AirSim 시뮬레이션에서 출력한 ppm파일을 jpg파일로 변환하는 API 코드

import os
from PIL import Image

def convert_ppm_to_jpg(ppm_folder, jpg_folder):
    if not os.path.exists(jpg_folder):
        os.makedirs(jpg_folder)

    #PPM 파일 목록 가져오기
    ppm_files = [f for f in os.listdir(ppm_folder) if f.endswith('.ppm')]
    
    for index, ppm_file in enumerate(ppm_files, start=1):
        #PPM 파일 경로
        ppm_path = os.path.join(ppm_folder, ppm_file)
        
        #이미지 열기
        with Image.open(ppm_path) as img:
            #이미지 변환 시 기존 ppm 파일 명을 이용
            jpg_file_name = os.path.splitext(ppm_file)[0] + '.jpg'
            jpg_path = os.path.join(jpg_folder, jpg_file_name)
            
            #JPG로 저장
            img.convert('RGB').save(jpg_path, 'JPEG')
            print(f"Converted {ppm_file} to {jpg_file_name}")

ppm_folder = r'C:\Users\kim\Documents\AirSim\2024-11-06-20-19-04\images'  #PPM 파일이 있는 폴더 경로
jpg_folder = r'C:\Users\kim\Documents\AirSim\사진 이름명 일치 실험'   #변환된 JPG 파일을 저장할 폴더 경로
convert_ppm_to_jpg(ppm_folder, jpg_folder)