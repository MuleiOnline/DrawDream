import requests
import json
from environment import generate_env


url_chat = "https://gpt-api.hkust-gz.edu.cn/v1/chat/completions"
headers_chat = {
    "Content-Type": "application/json",
    "Authorization": "Bearer c330e0694fbd4f0783df93114c15bfab30afb6263743429984a9cdda6851b143"
}


def generate_text(prompt):
    # environment 中包含温度、光照和天气信息
    environment = generate_env()
    story_prompt = (f"The background temperature of the story is: {environment[0]}, the lighting condition of the story is: {environment[1]}, "
                    f"the background weather of the story is: {environment[2]}, the plot prompt of the story is: {prompt}")
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
