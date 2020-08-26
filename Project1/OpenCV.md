# OpenCV

- version : 4.2.0

## 참고

- [참고1](https://m.blog.naver.com/samsjang/220498694383)
- [참고2, 이거보고 설치함](https://webnautes.tistory.com/1186)



## Basic

- 실시간 비전을 목적으로 한 프로그래밍 라이브러리
- 실시간 이미지 프로세싱에 중점을 둔 라이브러리
- 조금이라도 영상처리가 들어간다면 필수적으로 사용하게 되는 라이브러리



## 설치방법

### 1. 설치된 OpenCV 제거

- 버전 확인

```bash
$ pkg-config --modversion opencv
```



- 여기서 버전 확인되면 설치되어있는것, 아니면 다음 단계로 넘어가도 된다
- 다음 명령으로 OpenCV 라이브러리 설정 파일을 포함해서 기존에 설치된 OpenCV 패키지를 삭제하고 진행한다

```bash
$ sudo apt-get purge libopencv* python-opencv
$ sudo apt-get autoremove
```



- 다음 명령으로 기존 설치된 openvc 라이브러리를 삭제(`-i` 제거하면 전부 삭제)

```bash
$  sudo find /usr/local/ -name "*opencv*" -exec rm -i {} \;
```





### 2. 기존 설치된 패키지 업그레이드

```bash
$ sudo apt-get update
$ sudo apt-get upgrade
```



### 3. OpenCV 컴파일 전 필요한 패키지 설치

- **build-essential** 패키지에는 C/C++ 컴파일러와 관련 라이브러리, make 같은 도구들이 포함되어 있습니다.
- **cmake**는 컴파일 옵션이나 빌드된 라이브러리에 포함시킬 OpenCV 모듈 설정등을 위해 필요합니다. 

```bash
$ sudo apt-get install build-essential cmake
```



- **pkg-config**는 프로그램 컴파일 및 링크시 필요한 라이브러리에 대한 정보를 메타파일(확장자가 .pc 인 파일)로부터 가져오는데 사용됩니다. 
- 터미널에서 특정 라이브러리를 사용한 소스코드를 컴파일시 필요한 컴파일러 및 링커 플래그를 추가하는데 도움이 됩니다. 

```bash
$ sudo apt-get install pkg-config
```



- 특정 포맷의 이미지 파일을 불러오거나 기록하기 위해 필요한 패키지들입니다.

```bash
$ sudo apt-get install libjpeg-dev libtiff5-dev libpng-dev
```



- 특정 코덱의 비디오 파일을 읽어오거나 기록하기 위해 필요한 패키지들입니다.

```bash
$ sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libxvidcore-dev libx264-dev libxine2-dev
```



- Video4Linux 패키지는 리눅스에서 실시간 비디오 캡처를 지원하기 위한 디바이스 드라이버와 API를 포함하고 있습니다. 

```bash
$ sudo apt-get install libv4l-dev v4l-utils
```



- GStreamer는 비디오 스트리밍을 위한 라이브러리입니다. 

```bash
$ sudo apt-get install libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev 
```



- OpenCV에서는 highgui 모듈을 사용하여 자체적으로 윈도우 생성하여 이미지나 비디오를 보여줄 수 있습니다. 
- 윈도우 생성 등의 GUI를 위해 gtk 또는 qt를 선택해서 사용가능합니다. 여기서는 gtk2를 지정해주었습니다. (그외 : libgtk-3-dev  /  libqt4-dev  /  libqt5-dev)

```bash
$ sudo apt-get install libgtk2.0-dev
```



- OpenGL 지원하기 위해 필요한 라이브러리입니다.

```bash
$ sudo apt-get install mesa-utils libgl1-mesa-dri libgtkgl2.0-dev libgtkglext1-dev 
```



- OpenCV 최적화를 위해 사용되는 라이브러리들입니다.

```bash
$ sudo apt-get install libatlas-base-dev gfortran libeigen3-dev
```



- python2.7-dev와 python3-dev 패키지는 OpenCV-Python 바인딩을 위해 필요한 패키지들입니다. 
- Numpy는 매트릭스 연산등을 빠르게 처리할 수 있어서 OpenCV에서 사용됩니다. 

```bash
$ sudo apt-get install python2.7-dev python3-dev python-numpy python3-numpy
```





### 4. OpenCV 설정과 컴파일 및 설치

- 소스코드 저장할 디렉토리 생성

```bash
$ mkdir opencv 
$ cd opencv 
~/opencv$ 
```



- OpenCV 4.2.0 소스코드를 다운로드 받아 압축을 풀어줍니다.

```bash
$ wget -O opencv.zip https://github.com/opencv/opencv/archive/4.2.0.zip 
$ unzip opencv.zip
```



- opencv_contrib(extra modules) 소스코드를 다운로드 받아 압축을 풀어줍니다. (SIFT, SURF 등을 사용하기 위해 필요합니다.)

```bash
$ wget -O opencv_contrib.zip https://github.com/opencv/opencv_contrib/archive/4.2.0.zip 
$ unzip opencv_contrib.zip
```



- 다음처럼 두 개의 디렉토리가 생성됩니다. 

```bash
$ ls -d */ opencv-4.2.0/ opencv_contrib-4.2.0/
```



- opencv-4.2.0 디렉토리로 이동하여 build 디렉토리를 생성하고 build 디렉토리로 이동합니다.
- 컴파일은 build 디렉토리에서 이루어집니다.

```bash
$ cd opencv-4.2.0/
$ mkdir build 
$ cd build
~build$
```



- cmake를 사용하여 OpenCV 컴파일 설정을 해줍니다. 
  - **OpenCV 4에서 pkg-config를 디폴트로 지원하지 않는 것으로 바뀌었습니다.** **그래서 OPENCV_GENERATE_PKGCONFIG=ON 옵션을 추가해야합니다.**( 참고** [**https://github.com/opencv/opencv/issues/13154**](https://github.com/opencv/opencv/issues/13154) **)** 
  - **Non free 모듈을 사용하려면 다음 옵션을 추가하세요.**
  - **-D OPENCV_ENABLE_NONFREE=ON** 

```bash
cmake -D CMAKE_BUILD_TYPE=RELEASE \ 
-D CMAKE_INSTALL_PREFIX=/usr/local \
-D WITH_TBB=OFF \
-D WITH_IPP=OFF \
-D WITH_1394=OFF \
-D BUILD_WITH_DEBUG_INFO=OFF \
-D BUILD_DOCS=OFF \
-D INSTALL_C_EXAMPLES=ON \ 
-D INSTALL_PYTHON_EXAMPLES=ON \
-D BUILD_EXAMPLES=OFF \
-D BUILD_TESTS=OFF \
-D BUILD_PERF_TESTS=OFF \
-D WITH_QT=OFF \
-D WITH_GTK=ON \
-D WITH_OPENGL=ON \
-D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib-4.2.0/modules \
-D WITH_V4L=ON \
-D WITH_FFMPEG=ON \
-D WITH_XINE=ON \
-D BUILD_NEW_PYTHON_SUPPORT=ON \
-D OPENCV_GENERATE_PKGCONFIG=ON ../

# or 에러가 나는 경우 한줄로 바꾼 다음 명령을 사용하세요. 
cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D WITH_TBB=OFF -D WITH_IPP=OFF -D WITH_1394=OFF -D BUILD_WITH_DEBUG_INFO=OFF -D BUILD_DOCS=OFF -D INSTALL_C_EXAMPLES=ON -D INSTALL_PYTHON_EXAMPLES=ON -D BUILD_EXAMPLES=OFF -D BUILD_TESTS=OFF -D BUILD_PERF_TESTS=OFF -D WITH_QT=OFF -D WITH_GTK=ON -D WITH_OPENGL=ON -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib-4.2.0/modules -D WITH_V4L=ON -D WITH_FFMPEG=ON -D WITH_XINE=ON -D BUILD_NEW_PYTHON_SUPPORT=ON -D OPENCV_GENERATE_PKGCONFIG=ON ../
```



- 다음과 같은 메시지가 보이면 정상적으로 된 것입니다.

```bash
-- Configuring done
-- Generating done
-- Build files have been written to: /home/webnautes/opencv/opencv-4.2.0/build
```



cmake를 사용하여 진행한 OpenCV 컴파일 관련 설정 결과입니다.

```bash
-- General configuration for OpenCV 4.2.0 =====================================
-- Version control: unknown
-- Extra modules:
-- Location (extra): /home/keti0/opencv/opencv_contrib-4.2.0/modules
-- Version control (extra): unknown
-- Platform:
-- Timestamp: 2020-08-26T06:23:16Z
-- Host: Linux 5.4.0-42-generic x86_64
-- CMake: 3.10.2
-- CMake generator: Unix Makefiles
-- CMake build tool: /usr/bin/make
-- Configuration: RELEASE
-- CPU/HW features:
-- Baseline: SSE SSE2 SSE3
-- requested: SSE3
-- Dispatched code generation: SSE4_1 SSE4_2 FP16 AVX AVX2 AVX512_SKX
-- requested: SSE4_1 SSE4_2 AVX FP16 AVX2 AVX512_SKX
-- SSE4_1 (14 files): + SSSE3 SSE4_1
-- SSE4_2 (1 files): + SSSE3 SSE4_1 POPCNT SSE4_2
-- FP16 (0 files): + SSSE3 SSE4_1 POPCNT SSE4_2 FP16 AVX
-- AVX (4 files): + SSSE3 SSE4_1 POPCNT SSE4_2 AVX
-- AVX2 (27 files): + SSSE3 SSE4_1 POPCNT SSE4_2 FP16 FMA3 AVX AVX2
-- AVX512_SKX (3 files): + SSSE3 SSE4_1 POPCNT SSE4_2 FP16 FMA3 AVX AVX2 AVX_512F AVX512_COMMON AVX512_SKX
-- C/C++:
-- Built as dynamic libs?: YES
-- C++ Compiler: /usr/bin/c++ (ver 7.5.0)
-- C++ flags (Release): -fsigned-char -W -Wall -Werror=return-type -Werror=non-virtual-dtor -Werror=address -Werror=sequence-point -Wformat -Werror=format-security -Wmissing-declarations -Wundef -Winit-self -Wpointer-arith -Wshadow -Wsign-promo -Wuninitialized -Winit-self -Wsuggest-override -Wno-delete-non-virtual-dtor -Wno-comment -Wimplicit-fallthrough=3 -Wno-strict-overflow -fdiagnostics-show-option -Wno-long-long -pthread -fomit-frame-pointer -ffunction-sections -fdata-sections -msse -msse2 -msse3 -fvisibility=hidden -fvisibility-inlines-hidden -O3 -DNDEBUG -DNDEBUG
-- C++ flags (Debug): -fsigned-char -W -Wall -Werror=return-type -Werror=non-virtual-dtor -Werror=address -Werror=sequence-point -Wformat -Werror=format-security -Wmissing-declarations -Wundef -Winit-self -Wpointer-arith -Wshadow -Wsign-promo -Wuninitialized -Winit-self -Wsuggest-override -Wno-delete-non-virtual-dtor -Wno-comment -Wimplicit-fallthrough=3 -Wno-strict-overflow -fdiagnostics-show-option -Wno-long-long -pthread -fomit-frame-pointer -ffunction-sections -fdata-sections -msse -msse2 -msse3 -fvisibility=hidden -fvisibility-inlines-hidden -g -O0 -DDEBUG -D_DEBUG
-- C Compiler: /usr/bin/cc
-- C flags (Release): -fsigned-char -W -Wall -Werror=return-type -Werror=non-virtual-dtor -Werror=address -Werror=sequence-point -Wformat -Werror=format-security -Wmissing-declarations -Wmissing-prototypes -Wstrict-prototypes -Wundef -Winit-self -Wpointer-arith -Wshadow -Wuninitialized -Winit-self -Wno-comment -Wimplicit-fallthrough=3 -Wno-strict-overflow -fdiagnostics-show-option -Wno-long-long -pthread -fomit-frame-pointer -ffunction-sections -fdata-sections -msse -msse2 -msse3 -fvisibility=hidden -O3 -DNDEBUG -DNDEBUG
-- C flags (Debug): -fsigned-char -W -Wall -Werror=return-type -Werror=non-virtual-dtor -Werror=address -Werror=sequence-point -Wformat -Werror=format-security -Wmissing-declarations -Wmissing-prototypes -Wstrict-prototypes -Wundef -Winit-self -Wpointer-arith -Wshadow -Wuninitialized -Winit-self -Wno-comment -Wimplicit-fallthrough=3 -Wno-strict-overflow -fdiagnostics-show-option -Wno-long-long -pthread -fomit-frame-pointer -ffunction-sections -fdata-sections -msse -msse2 -msse3 -fvisibility=hidden -g -O0 -DDEBUG -D_DEBUG
-- Linker flags (Release): -Wl,--gc-sections
-- Linker flags (Debug): -Wl,--gc-sections
-- ccache: NO
-- Precompiled headers: NO
-- Extra dependencies: dl m pthread rt /usr/lib/x86_64-linux-gnu/libGL.so /usr/lib/x86_64-linux-gnu/libGLU.so
-- 3rdparty dependencies:
-- OpenCV modules:
-- To be built: aruco bgsegm bioinspired calib3d ccalib core datasets dnn dnn_objdetect dnn_superres dpm face features2d flann freetype fuzzy gapi hfs highgui img_hash imgcodecs imgproc line_descriptor ml objdetect optflow phase_unwrapping photo plot python2 python3 quality reg rgbd saliency shape stereo stitching structured_light superres surface_matching text tracking video videoio videostab xfeatures2d ximgproc xobjdetect xphoto
-- Disabled: world
-- Disabled by dependency: -
-- Unavailable: cnn_3dobj cudaarithm cudabgsegm cudacodec cudafeatures2d cudafilters cudaimgproc cudalegacy cudaobjdetect cudaoptflow cudastereo cudawarping cudev cvv hdf java js matlab ovis sfm ts viz
-- Applications: apps
-- Documentation: NO
-- Non-free algorithms: NO
-- GUI:
-- GTK+: YES (ver 2.24.32)
-- GThread : YES (ver 2.56.4)
-- GtkGlExt: YES (ver 1.2.0)
-- OpenGL support: YES (/usr/lib/x86_64-linux-gnu/libGL.so /usr/lib/x86_64-linux-gnu/libGLU.so)
-- VTK support: NO
-- Media I/O:
-- ZLib: /usr/lib/x86_64-linux-gnu/libz.so (ver 1.2.11)
-- JPEG: /usr/lib/x86_64-linux-gnu/libjpeg.so (ver 80)
-- WEBP: build (ver encoder: 0x020e)
-- PNG: /usr/lib/x86_64-linux-gnu/libpng.so (ver 1.6.34)
-- TIFF: /usr/lib/x86_64-linux-gnu/libtiff.so (ver 42 / 4.0.9)
-- JPEG 2000: build (ver 1.900.1)
-- OpenEXR: build (ver 2.3.0)
-- HDR: YES
-- SUNRASTER: YES
-- PXM: YES
-- PFM: YES
-- Video I/O:
-- FFMPEG: YES
-- avcodec: YES (57.107.100)
-- avformat: YES (57.83.100)
-- avutil: YES (55.78.100)
-- swscale: YES (4.8.100)
-- avresample: NO
-- GStreamer: YES (1.14.5)
-- v4l/v4l2: YES (linux/videodev2.h)
-- Xine: YES (ver 1.2.8)
-- Parallel framework: pthreads
-- Trace: YES (with Intel ITT)
-- Other third-party libraries:
-- Lapack: NO
-- Eigen: YES (ver 3.3.4)
-- Custom HAL: NO
-- Protobuf: build (3.5.1)
-- OpenCL: YES (no extra features)
-- Include path: /home/keti0/opencv/opencv-4.2.0/3rdparty/include/opencl/1.2
-- Link libraries: Dynamic load
-- Python 2:
-- Interpreter: /usr/bin/python2.7 (ver 2.7.17)
-- Libraries: /usr/lib/x86_64-linux-gnu/libpython2.7.so (ver 2.7.17)
-- numpy: /usr/lib/python2.7/dist-packages/numpy/core/include (ver 1.13.3)
-- install path: lib/python2.7/dist-packages/cv2/python-2.7
-- Python 3:
-- Interpreter: /usr/bin/python3 (ver 3.6.9)
-- Libraries: /usr/lib/x86_64-linux-gnu/libpython3.6m.so (ver 3.6.9)
-- numpy: /usr/lib/python3/dist-packages/numpy/core/include (ver 1.13.3)
-- install path: lib/python3.6/dist-packages/cv2/python-3.6
-- Python (for build): /usr/bin/python2.7
-- Java:
-- ant: NO
-- JNI: NO
-- Java wrappers: NO
-- Java tests: NO
-- Install to: /usr/local

--
-- Configuring done
-- Generating done
-- Build files have been written to: /home/keti0/opencv/opencv-4.2.0/build
```



- 다음처럼 Python 2 또는 Python 3 라이브러리 항목이 보이지 않는 경우에는  

```bash
-- Python 2:
-- Interpreter: /usr/bin/python2.7 (ver 2.7.17)
-- Libraries: /usr/lib/x86_64-linux-gnu/libpython2.7.so (ver 2.7.17)
-- numpy: /usr/lib/python2.7/dist-packages/numpy/core/include (ver 1.13.3)
-- install path: lib/python2.7/dist-packages/cv2/python-2.7
-- Python 3:
-- Interpreter: /usr/bin/python3 (ver 3.6.9)
-- Libraries: /usr/lib/x86_64-linux-gnu/libpython3.6m.so (ver 3.6.9)
-- numpy: /usr/lib/python3/dist-packages/numpy/core/include (ver 1.13.3)
-- install path: lib/python3.6/dist-packages/cv2/python-3.6
```

- 붉은색 줄처럼 해당 경로들을 직접 적어줘야 합니다.  포스팅에서 사용한 옵션과 차이가 있을 수 있습니다. 

```bash
cmake -D CMAKE_BUILD_TYPE=RELEASE \
-D CMAKE_INSTALL_PREFIX=/usr/local \
-D WITH_TBB=OFF \
-D WITH_IPP=OFF \
-D WITH_1394=OFF \
-D BUILD_WITH_DEBUG_INFO=OFF \
-D BUILD_DOCS=OFF \
-D INSTALL_C_EXAMPLES=ON \
-D INSTALL_PYTHON_EXAMPLES=ON \
-D BUILD_EXAMPLES=OFF \
-D BUILD_TESTS=OFF \
-D BUILD_PERF_TESTS=OFF \
-D WITH_QT=OFF \
-D WITH_GTK=ON \
-D WITH_OPENGL=ON \
-D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib-4.2.0/modules \
-D WITH_V4L=ON  \
-D WITH_FFMPEG=ON \
-D WITH_XINE=ON \
-D BUILD_NEW_PYTHON_SUPPORT=ON \
-D OPENCV_GENERATE_PKGCONFIG=ON \

## 아래부분
-D PYTHON2_INCLUDE_DIR=/usr/include/python2.7 \
-D PYTHON2_NUMPY_INCLUDE_DIRS=/usr/lib/python2.7/dist-packages/numpy/core/include/ \
-D PYTHON2_PACKAGES_PATH=/usr/lib/python2.7/dist-packages \
-D PYTHON2_LIBRARY=/usr/lib/x86_64-linux-gnu/libpython2.7.so \
-D PYTHON3_INCLUDE_DIR=/usr/include/python3.6m \
-D PYTHON3_NUMPY_INCLUDE_DIRS=/usr/lib/python3/dist-packages/numpy/core/include/  \
-D PYTHON3_PACKAGES_PATH=/usr/lib/python3/dist-packages \
-D PYTHON3_LIBRARY=/usr/lib/x86_64-linux-gnu/libpython3.6m.so \
```



- 컴파일을 시작하기 전에 사용 중인 컴퓨터의 CPU 코어수를 확인합니다.

```bash
$ cat /proc/cpuinfo | grep processor | wc -l 4
```



- make 명령을 사용하여 컴파일을 시작합니다. **-j** 다음에 위에서 확인한 숫자를 붙여서 실행해줍니다. 앞에 time을 붙여서 실행하면 컴파일 완료 후 걸린 시간을 알려줍니다.

```bash
$ time make -j4
```



- 컴파일 성공하면 다음과 같은 메시지를 볼 수 있습니다.

```bash
[100%] Building CXX object modules/python3/CMakeFiles/opencv_python3.dir/__/src2/cv2.cpp.o [100%] Building CXX object modules/python2/CMakeFiles/opencv_python2.dir/__/src2/cv2.cpp.o [100%] Linking CXX shared module ../../lib/python3/cv2.cpython-36m-x86_64-linux-gnu.so 
[100%] Linking CXX shared module ../../lib/cv2.so 
[100%] Built target opencv_python3 
[100%] Built target opencv_python2  

real	17m15.631s 
user	55m47.050s 
sys	2m39.468s
```

- 참고로 i5, SSD, 16G 메모리를 장착한 노트북에서 컴파일한데 걸린 시간은 위 결과에서 user + sys를 더한 약 57분입니다. 



- 이제 컴파일 결과물을 설치합니다. 

```bash
$ sudo make install
```



- /etc/ld.so.conf.d/ 디렉토리에 **/usr/local/lib**를 포함하는 설정파일이 있는지 확인합니다.



```bash
$ cat /etc/ld.so.conf.d/*
/usr/lib/x86_64-linux-gnu/libfakeroot
# libc default configuration
/usr/local/lib
# Multiarch support
/usr/local/lib/x86_64-linux-gnu
/lib/x86_64-linux-gnu
/usr/lib/x86_64-linux-gnu
```



- **/usr/local/lib**이 출력되지 않았다면 다음 명령을 추가로 실행해야합니다.

```bash
$ sudo sh -c 'echo '/usr/local/lib' > /etc/ld.so.conf.d/opencv.conf'
```



- /usr/local/lib을 찾은 경우나 못찾아서 추가한 작업을 한 경우 모두 컴파일시 opencv 라이브러리를 찾을 수 있도록 다음 명령을 실행합니다.

```bash
$ sudo ldconfig
```





### 5. OpenCV 설치 결과 확인

OpenCV 3과 달리 opencv대신에 opencv4를 옵션으로 사용하여 pkg-config를 실행해야 컴파일할 수 있습니다. 

$ g++ -o facedetect /usr/local/share/opencv4/samples/cpp/facedetect.cpp $(pkg-config opencv4 --libs --cflags)





실행시켜보면 얼굴 인식이 됩니다. 

$ ./facedetect --cascade="/usr/local/share/opencv4/haarcascades/haarcascade_frontalface_alt.xml" --nested-cascade="/usr/local/share/opencv4/haarcascades/haarcascade_eye_tree_eyeglasses.xml" --scale=1.3





다음 포스팅도 참고하세요. 



 Visual Studio Code에서 CMake 사용하여 OpenCV 코드 컴파일 하기https://webnautes.tistory.com/933  





## 5.2. Python

\1. python 2.x와 python 3x에서 opencv 라이브러리를 사용가능한지는 다음처럼 확인합니다.

각각 OpenCV 버전이 출력되어야 합니다. 



webnautes@webnautes-pc:~/opencv/opencv-4.2.0/build$ python Python 2.7.17 (default, Nov 7 2019, 10:07:09) [GCC 7.4.0] on linux2Type "help", "copyright", "credits" or "license" for more information.>>> import cv2>>> cv2.__version__'4.2.0'>>> 





webnautes@webnautes-pc:~/opencv/opencv-4.2.0/build$ python3 Python 3.6.9 (default, Nov 7 2019, 10:44:02) [GCC 8.3.0] on linuxType "help", "copyright", "credits" or "license" for more information.>>> import cv2>>> cv2.__version__'4.2.0'>>> 





혹시 다른 버전이 나온다면 다음 위치에 있는 cv2 디렉토리를 삭제하고 다시 해보세요.



sudo rm -rf ~ /.local/lib/python3.6/site-packages/cv2





\2. 기존 OpenCV 3를 삭제 후 진행했다면 다음과 같은 에러가 날 수 있습니다.



webnautes@webnautes-pc:~/opencv/opencv-4.2.0/build$ python Python 2.7.17 (default, Nov 7 2019, 10:07:09) [GCC 7.4.0] on linux2 Type "help", "copyright", "credits" or "license" for more information. >>> import cv2 Traceback (most recent call last):  File "<stdin>", line 1, in <module> ImportError: libopencv_reg.so.3.4: cannot open shared object file: No such file or directory





다음 처럼 cv2.so를 복사해줘야 합니다.



webnautes@webnautes-pc:~/opencv/opencv-4.2.0/build$ sudo cp /usr/local/python/cv2/python-2.7/cv2.so /usr/local/lib/python2.7/dist-packages/  webnautes@webnautes-pc:~/opencv/opencv-4.2.0/build$ sudo cp /usr/local/python/cv2/python-2.7/cv2.so /usr/lib/python2.7/dist-packages/  webnautes@webnautes-pc:~/opencv/opencv-4.2.0/build$ sudo cp /usr/local/python/cv2/python-3.6/cv2.cpython-36m-x86_64-linux-gnu.so /usr/lib/python3/dist-packages  webnautes@webnautes-pc:~/opencv/opencv-4.2.0/build$ sudo cp /usr/local/python/cv2/python-3.6/cv2.cpython-36m-x86_64-linux-gnu.so /usr/local/lib/python3.6/dist-packages





\3. 예제 코드를 실행해봅니다.



$ python /usr/local/share/opencv4/samples/python/facedetect.py --cascade "/usr/local/share/opencv4/haarcascades/haarcascade_frontalface_alt.xml" --nested-cascade "/usr/local/share/opencv4/haarcascades/haarcascade_eye_tree_eyeglasses.xml" /dev/video0





$  python3 /usr/local/share/opencv4/samples/python/facedetect.py --cascade "/usr/local/share/opencv4/haarcascades/haarcascade_frontalface_alt.xml" --nested-cascade "/usr/local/share/opencv4/haarcascades/haarcascade_eye_tree_eyeglasses.xml" /dev/video0





다음처럼 터미널에 표시되면서 카메라 영상에 얼굴이 검출된 결과를 얻을 수 있습니다.



python2



webnautes@webnautes-pc:~/opencv/opencv-4.2.0/build$ python /usr/local/share/opencv4/samples/python/facedetect.py --cascade "/usr/local/share/opencv4/haarcascades/haarcascade_frontalface_alt.xml" --nested-cascade "/usr/local/share/opencv4/haarcascades/haarcascade_eye_tree_eyeglasses.xml" /dev/video0 face detection using haar cascades USAGE:  facedetect.py [--cascade <cascade_fn>] [--nested-cascade <cascade_fn>] [<video_source>] [ INFO:0] Initialize OpenCL runtime...





python3



webnautes@webnautes-pc:~/opencv/opencv-4.2.0/build$  python3 /usr/local/share/opencv4/samples/python/facedetect.py --cascade "/usr/local/share/opencv4/haarcascades/haarcascade_frontalface_alt.xml" --nested-cascade "/usr/local/share/opencv4/haarcascades/haarcascade_eye_tree_eyeglasses.xml" /dev/video0 face detection using haar cascades USAGE:  facedetect.py [--cascade <cascade_fn>] [--nested-cascade <cascade_fn>] [<video_source>] [ INFO:0] Initialize OpenCL runtime...





\4. 이제 필요 없어진 컴파일에 사용했던 opencv 소스코드 디렉토리를 삭제합니다.



webnautes@webnautes-pc:~/opencv/opencv-4.2.0/build$ cd webnautes@webnautes-pc:~$ rm -rf opencv