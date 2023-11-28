# extract_modules.py

import shutil
import os
import importlib.util

def extract_and_save_module(module_name, output_directory):
    try:
        # 모듈을 찾아서 저장
        spec = importlib.util.find_spec(module_name)
        if spec:
            module_path = spec.origin
            if module_path and not module_path.startswith('built-in'):
                # 내장 모듈이 아닌 경우에만 복사
                shutil.copy(module_path, os.path.join(output_directory, module_name + '.py'))
            else:
                print(f"Module '{module_name}' is built-in and will not be copied.")
        else:
            print(f"Module '{module_name}' not found.")
    except Exception as e:
        print(f"Error while processing module '{module_name}': {e}")

def main():
    # 프로그램에 사용된 모듈 목록
    used_modules = ['PyQt5.QtWidgets', 'PyQt5.QtCore', 'subprocess', 'os', 'psutil', 'ctypes', 'requests', 'traceback', 'json', 'serial', 'serial.tools.list_ports', 'sqlite3']

    # 모듈을 저장할 디렉토리 생성
    output_directory = 'modules'
    os.makedirs(output_directory, exist_ok=True)

    # 각 모듈을 추출하고 저장
    for module_name in used_modules:
        extract_and_save_module(module_name, output_directory)

    print("Modules extracted successfully.")

if __name__ == "__main__":
    main()