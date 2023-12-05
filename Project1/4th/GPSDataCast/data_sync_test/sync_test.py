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


import vlc

def send_rtp(video_file, destination_address, destination_port):
    # Create VLC instance
    vlc_instance = vlc.Instance("--no-xlib")

    # Create media player
    media_player = vlc_instance.media_player_new()

    # Create media object
    media = vlc_instance.media_new(video_file)

    # Set RTP options
    options = f'#rtp{{mux=ts,dst={destination_address},port={destination_port}}}'
    media.add_option(options)

    # Set media to media player
    media_player.set_media(media)

    # Start playing
    media_player.play()

    try:
        # Wait for the user to interrupt the streaming (Ctrl+C)
        input("Press Enter to stop streaming...\n")

    except KeyboardInterrupt:
        pass

    finally:
        # Stop and release the media player and instance
        media_player.stop()
        vlc_instance.release()

if __name__ == "__main__":
    video_file_path = "/home/edge-worker-01/blackbox_osan/blackbox_08.mp4"  # Replace with your MP4 file path
    destination_ip = "192.168.0.14"
    destination_port = 5008

    send_rtp(video_file_path, destination_ip, destination_port)