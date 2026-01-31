from moviepy.editor import *
import os

image_folder = "img"
audio_path = r"C:\Users\danis\Desktop\fast_api\orchestral-joy-30-sec-423312.mp3"
output_video = "final_video.mp4"

# Load audio
audio = AudioFileClip(audio_path)
audio_duration = audio.duration

# Load images
images = sorted(os.listdir(image_folder))
num_images = len(images)

# Duration per image
img_duration = audio_duration / num_images

clips = []

for img in images:
    img_path = os.path.join(image_folder, img)

    clip = (
        ImageClip(img_path)
        .set_duration(img_duration)
        .resize(height=720)        # resize for video
        .fadein(0.5)               # fade in
        .fadeout(0.5)              # fade out
    )

    clips.append(clip)

# Combine image clips
video = concatenate_videoclips(clips, method="compose")

# Add audio
final_video = video.set_audio(audio)

# Export
final_video.write_videofile(
    output_video,
    fps=24,
    codec="libx264",
    audio_codec="aac"
)
