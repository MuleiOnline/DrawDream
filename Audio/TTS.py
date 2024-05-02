import os
from openai import OpenAI
from mutagen.mp3 import MP3
from pydub import AudioSegment
import os

def get_mp3_duration():
    """ 获取MP3文件的播放时长（以秒为单位）"""
    audio1 = MP3("C:/Users/Administrator/Downloads/DrawDream-main/Audio/audio_files/line_1.mp3")
    audio2 = MP3("C:/Users/Administrator/Downloads/DrawDream-main/Audio/audio_files/line_2.mp3")
    audio3 = MP3("C:/Users/Administrator/Downloads/DrawDream-main/Audio/audio_files/line_3.mp3")
    audio4 = MP3("C:/Users/Administrator/Downloads/DrawDream-main/Audio/audio_files/line_4.mp3")
    audio5 = MP3("C:/Users/Administrator/Downloads/DrawDream-main/Audio/audio_files/line_5.mp3")
    audio6 = MP3("C:/Users/Administrator/Downloads/DrawDream-main/Audio/audio_files/line_6.mp3")

    duration = []
    duration.append(audio1.info.length)
    duration.append(audio2.info.length)
    duration.append(audio3.info.length)
    duration.append(audio4.info.length)
    duration.append(audio5.info.length)
    duration.append(audio6.info.length)

    return duration


def audio_generation():

    OpenAI.api_key = 'xxxxxxxxxx'


    # 创建OpenAI客户端
    client = OpenAI()

    # 获取当前文件所在目录的上一级目录，并设置输入文件和输出文件夹的路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(current_dir)  # 上一级目录
    input_file_path = os.path.join(parent_dir, "story_plot.txt")
    output_folder = os.path.join(current_dir, "audio_files")

    # 创建输出文件夹（如果不存在）
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # 读取输入文件的每行文本并生成音频
    with open(input_file_path, "r", encoding="utf-8") as file:
        for i, line in enumerate(file):
            # 清理每行文本，去除多余的空格和换行符
            clean_line = line.strip()

            # 如果行为空，则跳过
            if not clean_line:
                continue

            # 指定输出音频文件的路径
            speech_file_path = os.path.join(output_folder, f"line_{i + 1}.mp3")

            # 调用OpenAI的语音模型生成音频
            response = client.audio.speech.create(
                model="tts-1",
                voice="alloy",
                input=clean_line
            )

            # 将生成的音频流保存到文件
            response.stream_to_file(speech_file_path)

    print("音频文件生成完毕。")
    print("Input file path:", input_file_path)
    return


def merge_audio_files(audio_dir):
    # 创建一个空的音频段
    combined = AudioSegment.empty()

    # 遍历子目录中的所有文件
    for file_name in os.listdir(audio_dir):
        if file_name.endswith('.mp3'):
            # 加载MP3文件
            audio_path = os.path.join(audio_dir, file_name)
            audio_segment = AudioSegment.from_mp3(audio_path)
            # 将当前音频添加到组合音频中
            combined += audio_segment

    # 导出合并后的音频文件
    output_path = 'combined_audio.mp3'
    combined.export(output_path, format='mp3')
    print(f'合并后的音频已经保存到：{output_path}')


# 使用示例
  # 音频文件所在的子目录
# output_file = 'combined_audio.mp3'  # 合并后的音频文件名
# merge_audio_files(audio_dir)
# print("Audio files have been merged successfully!")
#
# # 使用示例
# duration = get_mp3_duration()
# print(duration)
