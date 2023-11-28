# extract_modules.py

import shutil
import os

# 프로그램에 사용된 모듈 목록
used_modules = ['PyQt5.QtWidgets', 'PyQt5.QtCore', 'subprocess', 'os', 'sys', 'psutil']

# 모듈을 저장할 디렉토리 생성
output_directory = 'modules'
os.makedirs(output_directory, exist_ok=True)

# 모듈 파일을 복사하여 저장
for module_name in used_modules:
    module_path = shutil.which(module_name + '.py')
    if module_path:
        shutil.copy(module_path, os.path.join(output_directory, module_name + '.py'))
    else:
        print(f"Module '{module_name}' not found.")

print("Modules extracted successfully.")