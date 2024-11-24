import tkinter as tk
from tkinter import ttk
import os
import pygame
from yt_dlp import YoutubeDL
from moviepy.editor import VideoFileClip


class VideoClipperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("YouTube Video Clipper")

        self.url_label = tk.Label(self.root, text="Enter YouTube URL:")
        self.url_label.pack()

        self.url_entry = tk.Entry(self.root, width=40)
        self.url_entry.pack()

        self.download_button = tk.Button(self.root, text="Download Video", command=self.download_video)
        self.download_button.pack()

        self.start_time_slider = tk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL, label="Start Time (sec)")
        self.start_time_slider.pack()

        self.end_time_slider = tk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL, label="End Time (sec)")
        self.end_time_slider.pack()

        self.preview_button = tk.Button(self.root, text="Preview", command=self.preview_video)
        self.preview_button.pack()

        self.clip_button = tk.Button(self.root, text="Clip Video", command=self.create_clip)
        self.clip_button.pack()

        # Subtitle checkbox
        self.subtitle_var = tk.BooleanVar()
        self.subtitle_checkbox = tk.Checkbutton(self.root, text="Download Subtitles", variable=self.subtitle_var)
        self.subtitle_checkbox.pack()

        self.video_duration = None  # To store the video's length

        # Initialize pygame for live video preview
        pygame.init()
        self.screen = pygame.display.set_mode((640, 480))  # Set window size
        self.clock = pygame.time.Clock()

    def download_video(self):
        url = self.url_entry.get()
        ydl_opts = {
            'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
            'merge_output_format': 'mp4',
            'outtmpl': 'downloaded_video.mp4'
        }

        if self.subtitle_var.get():
            ydl_opts['subtitles'] = True
            ydl_opts['subtitleslangs'] = ['en']  # Choose desired language

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        print("Download complete.")

        # After downloading, set the video duration
        self.set_video_duration("downloaded_video.mp4")

    def set_video_duration(self, video_path):
        with VideoFileClip(video_path) as video:
            self.video_duration = video.duration  # Duration in seconds

            # Update the sliders to reflect the video length
            self.start_time_slider.config(to=self.video_duration)
            self.end_time_slider.config(to=self.video_duration)

    def show_preview(self, start_time, end_time):
        video_file = "downloaded_video.mp4"
        
        try:
            # Load video and audio clips
            video_clip = VideoFileClip(video_file).subclip(start_time, end_time)
            audio_clip = video_clip.audio

            # Prepare audio to play using pygame mixer
            audio_file = "temp_audio.wav"
            audio_clip.write_audiofile(audio_file, codec="pcm_s16le")  # Save audio to file
            pygame.mixer.init(frequency=audio_clip.fps)  # Match audio sample rate
            sound = pygame.mixer.Sound(audio_file)

            # Start playing audio and video simultaneously
            sound.play()

            # Render the video frames
            video_frames = video_clip.iter_frames(fps=24, dtype="uint8")
            for frame in video_frames:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        return

                # Resize the frame to fit within the pygame window (640x480)
                frame_resized = pygame.transform.scale(pygame.surfarray.make_surface(frame), (480, 640))
                frame_resized = pygame.transform.flip(frame_resized, False, True)


                # If the video is rotated incorrectly, you can fix it here:
                # If the frame is consistently sideways (90 or 270 degrees), rotate it to fix
                # This is just an example for 90-degree rotation
                frame_resized = pygame.transform.rotate(frame_resized, 270)  # Adjust this as needed

                # Display the frame
                self.screen.blit(frame_resized, (0, 0))
                pygame.display.update()

                self.clock.tick(24)  # Match FPS with video playback

            # Clean up the temporary audio file
            os.remove(audio_file)

        except Exception as e:
            print(f"Error during preview: {e}")

    def preview_video(self):
        start_time = self.start_time_slider.get()
        end_time = self.end_time_slider.get()
        self.show_preview(start_time, end_time)

    def create_clip(self):
        start_time = self.start_time_slider.get()
        end_time = self.end_time_slider.get()

        with VideoFileClip("downloaded_video.mp4") as video:
            clip = video.subclip(start_time, end_time)
            clip.write_videofile("output_clip.mp4", codec="libx264")
        print("Clip created successfully.")


if __name__ == "__main__":
    root = tk.Tk()
    app = VideoClipperApp(root)
    root.mainloop()
