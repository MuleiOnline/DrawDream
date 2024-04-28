import requests

url_tts = "https://api.xiaoai.plus/v1/tts/generations"  # 假设的TTS API URL
headers_tts = {
    "Content-Type": "application/json",
    "Authorization": "Bearer xxxxxxxx"  # 请使用实际的token替换这里
}

def generate_speech(text):
    data = {
        "model": "whisper",  # 假设的模型名字，根据实际情况修改
        "prompt": text,
        "language": "en-US"  # 根据需要选择适当的语言
    }
    response = requests.post(url_tts, headers=headers_tts, json=data)
    if response.status_code == 200:
        response_json = response.json()
        audio_url = response_json['data'][0]['url']  # 假设音频文件的URL是这样返回的

        audio_response = requests.get(audio_url)
        if audio_response.status_code == 200:
            with open("output_audio.mp3", "wb") as f:  # 保存音频文件到本地
                f.write(audio_response.content)
            print("Audio has been saved successfully.")
        else:
            print("Failed to download the audio file.")
    else:
        print("Failed to generate speech. Status code:", response.status_code)
        print("Error data:", response.text)

# 生成随机一段文字进行测试
import random
import string

def generate_random_text(length=100):
    letters = string.ascii_letters + " "
    return ''.join(random.choice(letters) for i in range(length))

# 测试文本转语音
test_text = generate_random_text()
generate_speech(test_text)
