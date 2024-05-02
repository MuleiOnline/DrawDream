from prompt import generate_text
from image import generate_image, download_and_crop_image
from video import create_video_from_images
import os
import openai
from Audio.TTS import audio_generation, get_mp3_duration, merge_audio_files
from moviepy.editor import VideoFileClip, AudioFileClip


def merge_video_audio(video_path, audio_path, output_path):
    # 读取视频文件
    video_clip = VideoFileClip(video_path)
    # 读取音频文件
    audio_clip = AudioFileClip(audio_path)

    # 将音频设置到视频中
    video_clip = video_clip.set_audio(audio_clip)

    # 写出合成后的视频文件
    video_clip.write_videofile(output_path, codec='libx264', audio_codec='aac')

    # 关闭视频和音频文件，释放资源
    video_clip.close()
    audio_clip.close()
    print(f"合成视频已保存至：{output_path}")


def main():
    base_path = r'C:\Users\Administrator\Downloads\DrawDream-main'
    user_input = input("Please describe your dream: ")
    style_choice = input("Enter the number for your preferred style (1-9): ")
    enriched_text = generate_text(user_input)

    if enriched_text:
        # Save the enriched text to a file
        text_file_path = os.path.join(base_path, 'story_plot.txt')
        with open(text_file_path, 'w') as file:
            file.write(enriched_text)

        image_url = generate_image(enriched_text, style_choice)
        if image_url:
            download_and_crop_image(image_url, base_path)
            images_folder = os.path.join(base_path, 'cropped_images')
            output_video_path = os.path.join(base_path, 'result.mp4')
            frame_rate = 0.5
            size = (1920, 1080)
            create_video_from_images(images_folder, output_video_path, frame_rate, size)

            # 生成音频
            audio_generation()
            print(get_mp3_duration())
            audio_dir = 'C:/Users/Administrator/Downloads/DrawDream-main/Audio/audio_files'
            merge_audio_files(audio_dir)

            # 合成视频
            video_path ='C:/Users/Administrator/Downloads/DrawDream-main/result.mp4'
            audio_path ='C:/Users/Administrator/Downloads/DrawDream-main/combined_audio.mp3'
            output_path = 'C:/Users/Administrator/Downloads/DrawDream-main/Final_video.mp4'

            merge_video_audio(video_path, audio_path, output_path)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("An error occurred:", str(e))

# You woke up lying on the floor, rubbing your eyes, and found yourself in a gothic style room. You feel a little scared, as if someone is watching you, when the door to the room is pushed open
#一个小女孩正坐在湖边钓鱼，突然有个奇怪的动物突然出现并吓到了小女孩，然后小女孩跳进湖里并来到一个新的世界
