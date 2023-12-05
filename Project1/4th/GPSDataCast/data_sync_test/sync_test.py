import subprocess
import shlex
import time

def start_video_streaming(username, num):
    while True:
        command = f'cvlc /home/edge-worker-01/blackbox_osan/blackbox_08.avi --sout "#rtp{{dst=192.168.0.14,port=5008,mux=ts}}" --no-sout-all'
        try:
            subprocess.run(shlex.split(command), check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error occurred: {e}")
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    username = "your_username"
    stream_num = 1  # Adjust this value based on your requirements

    try:
        start_video_streaming(username, stream_num)
    except KeyboardInterrupt:
        print("Streaming stopped.")