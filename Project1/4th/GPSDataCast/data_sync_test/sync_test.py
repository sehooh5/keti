import subprocess
import shlex
import time

def start_video_streaming(username, num):
    while True:
        command = f'cvlc /home/{username}/blackbox_osan/blackbox_0{num}.avi --sout "#rtp{{dst=192.168.0.14,port=500{num},mux=ts}}" --no-sout-all --play-and-exit'
        try:
            subprocess.run(shlex.split(command), check=True)
            print(f"Video stream {num} completed.")
        except subprocess.CalledProcessError as e:
            print(f"Error occurred: {e}")
        except KeyboardInterrupt:
            break

if __name__ == "__main__":
    username = "worker"
    stream_num = 8  # Adjust this value based on your requirements

    try:
        start_video_streaming(username, stream_num)
    except KeyboardInterrupt:
        print("Streaming stopped.")