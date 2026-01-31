import gradio as gr
from moviepy.editor import *
import os, shutil, tempfile

def create_video(image_files, audio_file):
    temp_dir = tempfile.mkdtemp()
    image_folder = os.path.join(temp_dir, "images")
    os.makedirs(image_folder, exist_ok=True)

    for img in image_files:
        shutil.copy(img.name, image_folder)

    audio = AudioFileClip(audio_file.name)
    audio_duration = audio.duration

    images = sorted(os.listdir(image_folder))
    img_duration = audio_duration / len(images)

    clips = []
    for img in images:
        clip = (
            ImageClip(os.path.join(image_folder, img))
            .set_duration(img_duration)
            .resize(height=720)
            .fadein(0.5)
            .fadeout(0.5)
        )
        clips.append(clip)

    video = concatenate_videoclips(clips, method="compose")
    final_video = video.set_audio(audio)

    output_video = os.path.join(temp_dir, "final_video.mp4")
    final_video.write_videofile(output_video, fps=24, codec="libx264", audio_codec="aac")

    return output_video

app = gr.Interface(
    fn=create_video,
    inputs=[
        gr.File(file_types=["image"], file_count="multiple"),
        gr.File(file_types=["audio"])
    ],
    outputs=gr.Video(),
    title="Image to Video Generator"
)

app.launch(share=True)
