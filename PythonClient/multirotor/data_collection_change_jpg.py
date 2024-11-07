#AirSim 시뮬레이션에서 출력한 ppm파일을 jpg파일로 변환하는 API 코드

import os
from PIL import Image

def convert_ppm_to_jpg(ppm_folder, jpg_folder):
    if not os.path.exists(jpg_folder):
        os.makedirs(jpg_folder)

    # 확장자가 없는 파일 포함해서 목록 가져오기
    ppm_files = [f for f in os.listdir(ppm_folder) if '.' not in f]

    for ppm_file in ppm_files:
        # 확장자가 없는 PPM 파일 경로
        ppm_path = os.path.join(ppm_folder, ppm_file)
        temp_ppm_path = ppm_path + '.ppm'  # 임시로 .ppm 확장자 붙이기
        
        # 파일 이름 그대로 사용, .jpg 확장자만 붙임
        jpg_file_name = ppm_file + '.jpg'
        jpg_path = os.path.join(jpg_folder, jpg_file_name)

        try:
            # 임시로 .ppm 확장자 붙이기
            os.rename(ppm_path, temp_ppm_path)
            
            # 이미지 열기 및 JPG로 변환 저장
            with Image.open(temp_ppm_path) as img:
                img.convert('RGB').save(jpg_path, 'JPEG')
                print(f"Converted {ppm_file} to {jpg_file_name}")
                
            # 작업 후 다시 확장자 제거하여 원래대로 복구
            os.rename(temp_ppm_path, ppm_path)

        except IOError:
            print(f"파일 {ppm_file}을(를) 처리할 수 없습니다.")
            # 예외 발생 시 원래대로 복구
            if os.path.exists(temp_ppm_path):
                os.rename(temp_ppm_path, ppm_path)

ppm_folder = r'C:\Users\kj746\Documents\AirSim\2024-10-31-17-33-59\images'  # PPM 파일이 있는 폴더 경로
jpg_folder = r'C:\Users\kj746\Documents\AirSim\2024-10-31-17-33-59\jpg'  # PPM 파일이 있는 폴더 경로
convert_ppm_to_jpg(ppm_folder, jpg_folder)
