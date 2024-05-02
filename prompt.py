import requests
import json
from environment import generate_env
import re







url_chat = "https://gpt-api.hkust-gz.edu.cn/v1/chat/completions"
headers_chat = {
    "Content-Type": "application/json",
    "Authorization": "Bearer c330e0694fbd4f0783df93114c15bfab30afb6263743429984a9cdda6851b143"
}

def extract_weather_info(sentence):
    # 扩展天气相关的词汇列表，包括中文和英文
    weather_keywords = [
        '晴', '阴', '多云', '小雨', '中雨', '大雨', '暴雨', '雷阵雨', '小雪', '中雪', '大雪', '暴雪',
        '冰雹', '雾', '霾', '风', '台风', '沙尘暴', '雷电', '刮风', '凉爽', '热', '冷',
        'sunny', 'cloudy', 'overcast', 'light rain', 'moderate rain', 'heavy rain', 'storm',
        'thunderstorm', 'light snow', 'moderate snow', 'heavy snow', 'blizzard', 'hail',
        'fog', 'haze', 'windy', 'typhoon', 'sandstorm', 'thunder', 'breezy', 'cool', 'hot', 'cold'
    ]
    # 创建正则表达式，匹配包含上述关键词的句子
    pattern = '|'.join(weather_keywords)
    # 搜索句子中的天气信息
    matches = re.findall(pattern, sentence, re.IGNORECASE)

    if matches:
        return ', '.join(matches)
    else:
        return None

def generate_text(prompt):
    # environment 中包含温度、光照和天气信息
    environment = generate_env()
    # 检查用户是否输入天气信息
    weather_from_user = extract_weather_info(prompt)
    if weather_from_user:
        story_prompt = (
            f"The background temperature of the story is: {environment[0]}, the lighting condition of the story is: {environment[1]}, "
            f"the background weather of the story is: {weather_from_user}, the plot prompt of the story is: {prompt}")
        print(story_prompt)
    else:
        story_prompt = (
            f"The background temperature of the story is: {environment[0]}, the lighting condition of the story is: {environment[1]}, "
            f"the background weather of the story is: {environment[2]['description']}, the plot prompt of the story is: {prompt}")
        print(story_prompt)


    data = {
        "model": "gpt-4",
        "messages": [
            {"role": "system",
             "content": "You are an assistant. Your task is to expand the following dream description into a complete story. Divide the whole story roughly into 6 simple sentences and number-sort them in order."},
            {"role": "user", "content": story_prompt}
        ],
        "temperature": 0.7
    }
    response = requests.post(url_chat, headers=headers_chat, data=json.dumps(data))
    if response.status_code == 200:
        response_data = response.json()
        scenes = response_data['choices'][0]['message']['content'].split('\n\n')
        return ' '.join(scenes)
    else:
        print("Failed to fetch data. Status code:", response.status_code)
        return None

# # 测试句子
# test_sentences = [
#     "明天北京将会有小雨，记得带伞。",
#     "It will be sunny in New York tomorrow.",
#     "今天天气晴朗，适合外出。",
#     "预计后天会下大雪。",
#     "Tomorrow there will be a blizzard in Chicago.",
#     "下周一到周五气温适中，没有降水。",
#     "I plan to go hiking this weekend."
# ]
#
# for sentence in test_sentences:
#     print(extract_weather_info(sentence))
