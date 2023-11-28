# extract_modules.py

import shutil
import os
import importlib.util

def extract_and_save_module(module_name, output_directory):
    # 모듈을 찾아서 저장
    spec = importlib.util.find_spec(module_name)
    if spec:
        module_path = spec.origin
        shutil.copy(module_path, os.path.join(output_directory, module_name + '.py'))
    else:
        print(f"Module '{module_name}' not found.")

def main():
    # 프로그램에 사용된 모듈 목록
    used_modules = ['PyQt5.QtWidgets', 'PyQt5.QtCore', 'subprocess', 'os', 'sys', 'psutil']

    # 모듈을 저장할 디렉토리 생성
    output_directory = 'extracted_modules'
    os.makedirs(output_directory, exist_ok=True)

    # 각 모듈을 추출하고 저장
    for module_name in used_modules:
        extract_and_save_module(module_name, output_directory)

    print("Modules extracted successfully.")

if __name__ == "__main__":
    main()