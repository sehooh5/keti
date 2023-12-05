# import subprocess
# import shlex
# import time
#
# def start_video_streaming(username, num):
#     while True:
#         command = f'cvlc /home/{username}/blackbox_osan/blackbox_0{num}.mp4 --sout "#rtp{{dst=192.168.0.14,port=500{num},mux=ts}}" --no-sout-all --play-and-exit'
#         try:
#             subprocess.run(shlex.split(command), check=True)
#             print(f"Video stream {num} completed.")
#         except subprocess.CalledProcessError as e:
#             print(f"Error occurred: {e}")
#         except KeyboardInterrupt:
#             break
#
# if __name__ == "__main__":
#     username = "edge-worker-01"
#     stream_num = 8  # Adjust this value based on your requirements
#
#     try:
#         start_video_streaming(username, stream_num)
#     except KeyboardInterrupt:
#         print("Streaming stopped.")

###################################

# import vlc
#
# def send_rtp(video_file, destination_address, destination_port):
#     # Create VLC instance
#     vlc_instance = vlc.Instance("--no-xlib")
#
#     # Create media player
#     media_player = vlc_instance.media_player_new()
#
#     # Create media object
#     media = vlc_instance.media_new(video_file)
#
#     # Set RTP options
#     options = f'#rtp{{mux=ts,dst={destination_address},port={destination_port}}}'
#     media.add_option(options)
#
#     # Set media to media player
#     media_player.set_media(media)
#
#     # Start playing
#     media_player.play()
#
#     try:
#         # Wait for the user to interrupt the streaming (Ctrl+C)
#         input("Press Enter to stop streaming...\n")
#
#     except KeyboardInterrupt:
#         pass
#
#     finally:
#         # Stop and release the media player and instance
#         media_player.stop()
#         vlc_instance.release()
#
# if __name__ == "__main__":
#     video_file_path = "/home/edge-worker-01/blackbox_osan/blackbox_08.mp4"  # Replace with your MP4 file path
#     destination_ip = "192.168.0.14"
#     destination_port = 5008
#
#     send_rtp(video_file_path, destination_ip, destination_port)
#


#############################################################

import cv2
import imageio_ffmpeg

def send_rtp(video_file, destination_address, destination_port):
    # Open video file
    cap = cv2.VideoCapture(video_file)

    # Get video properties
    width = int(cap.get(3))
    height = int(cap.get(4))
    fps = int(cap.get(5))

    # Create RTP stream
    rtp_url = f'rtp://{destination_address}:{destination_port}?encoding-name=H264&media-type=video&clock-rate={fps}'
    writer = imageio_ffmpeg.get_writer(rtp_url, fps=fps, codec='libx264', pixelformat='yuv420p', bitrate='500k')

    try:
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # Send frame to RTP stream
            writer.append_data(frame)

        print("Streaming complete.")

    finally:
        cap.release()
        writer.close()

if __name__ == "__main__":
    video_file_path = "/home/edge-worker-01/blackbox_osan/blackbox_08.mp4"  # Replace with your MP4 file path
    destination_ip = "192.168.0.14"
    destination_port = 5008

    send_rtp(video_file_path, destination_ip, destination_port)