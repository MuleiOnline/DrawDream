import requests  # 导入requests库，用于发起HTTP请求
import json  # 导入json库，用于处理JSON数据
from PIL import Image  # 从PIL库导入Image类，用于处理图像
from io import BytesIO  # 从io库导入BytesIO，用于处理字节流
import os  # 导入os库，用于处理文件和目录
import cv2

# 设置API请求的公共变量和头信息
url_chat = "https://gpt-api.hkust-gz.edu.cn/v1/chat/completions"  # 设置文本生成API的URL
url_image = "https://api.xiaoai.plus/v1/images/generations"  # 设置图像生成API的URL

headers_chat = {
    "Content-Type": "application/json",  # 设置请求内容类型为JSON
    "Authorization": "Bearer c330e0694fbd4f0783df93114c15bfab30afb6263743429984a9cdda6851b143"  # 设置请求的认证信息，替换为实际的令牌
}

headers_image = {
    "Content-Type": "application/json",  # 同上
    "Authorization": "Bearer sk-cEwCRbpTRcknuqzI77EfFbC4B4874e5f94162b7cFf981dDc"  # 设置图像API的认证信息，替换为实际的令牌
}


# 文本生成函数
def generate_text(prompt):
    """根据输入的提示文本生成完整的故事文本。"""
    data = {
        "model": "gpt-4",  # 指定使用的模型为GPT-4
        "messages": [
            {"role": "system",
             "content": "You are an assistant. Your task is to expand the following dream description into a complete story. Divide the whole story roughly into 6 simple sentences and number-sort them in order."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7  # 设置生成的随机性
    }
    response = requests.post(url_chat, headers=headers_chat, data=json.dumps(data))  # 发起POST请求
    if response.status_code == 200:  # 检查响应状态码是否为200
        response_data = response.json()
        scenes = response_data['choices'][0]['message']['content'].split('\n\n')
        return ' '.join(scenes)  # 将生成的文本拼接并返回
    else:
        print("Failed to fetch data. Status code:", response.status_code)
        return None


# 图像生成函数
def generate_image(text, style):
    """根据文本和风格生成图像。"""
    style_descriptions = {
        "1": "Flat style illustration",
        "2": "Textured style illustration",
        "3": "Gradient style illustration",
        "4": "Hand-drawn style",
        "5": "Graffiti style illustration",
        "6": "Watercolor style illustration",
        "7": "Picture book style illustration",
        "8": "Modern Chinese style illustration",
        "9": "Japanese style illustration"
    }
    chosen_style = style_descriptions.get(style, "Flat style illustration")  # 获取指定风格描述
    prompt = f"Based on the following plot, please generate the constant six small images in the same image once in the {chosen_style}: {text}"
    data = {
        "model": "dall-e-3",
        "prompt": prompt,
        "size": "1024x1024",
        "quality": "standard",
        "n": 1
    }
    response = requests.post(url_image, headers=headers_image, json=data)
    if response.status_code == 200:
        response_json = response.json()
        if 'data' in response_json:
            return response_json['data'][0]['url']
        else:
            error_message = response_json.get('error', {}).get('message', 'Unknown error.')
            print("Error in response:", error_message)
            return None
    elif response.status_code == 500:
        print("Server error occurred. Please try again later.")
    else:
        print("Failed to fetch image. Status code:", response.status_code)
        print("Error data:", response.text)
    return None

# video generation( undone)
def create_video_from_images(images_folder, output_video_path, frame_rate, size):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter(output_video_path, fourcc, frame_rate, size)

    file_lst = [
        '1_top_left.jpg', '2_top_middle.jpg', '3_top_right.jpg',
        '6_bottom_left.jpg', '5_bottom_middle.jpg', '4_bottom_right.jpg'
    ]

    for filename in file_lst:
        img_path = os.path.join(images_folder, filename)
        if os.path.exists(img_path):
            img = cv2.imread(img_path)
            img = cv2.resize(img, size)
            video.write(img)
        else:
            print(f"File does not exist: {img_path}")

    video.release()
    print("Video created at", output_video_path)

# 图像裁剪函数
def download_and_crop_image(url, base_path):
    """下载图像并将其裁剪成六个部分。"""
    if url:
        response = requests.get(url)
        if response.status_code == 200:
            full_image_path = os.path.join(base_path, 'full_image.jpg')
            with open(full_image_path, 'wb') as f:
                f.write(response.content)  # 将图像内容写入文件
            print("Image downloaded and saved to", full_image_path)

            img = Image.open(BytesIO(response.content))  # 打开图像
            size_x, size_y = img.size  # 获取图像尺寸
            columns, rows = 3, 2
            w, h = size_x // columns, size_y // rows

            image_order = ['1_top_left.jpg', '2_top_middle.jpg', '3_top_right.jpg', '6_bottom_left.jpg',
                           '5_bottom_middle.jpg', '4_bottom_right.jpg']

            cropped_dir = os.path.join(base_path, 'cropped_images')
            os.makedirs(cropped_dir, exist_ok=True)

            for i, order in enumerate(image_order):
                col = i % columns
                row = i // columns
                left, upper = col * w, row * h
                right, lower = left + w, upper + h
                region = img.crop((left, upper, right, lower))  # 裁剪图像
                region.save(os.path.join(cropped_dir, order))  # 保存裁剪后的图像
            print("Cropping completed and saved in", cropped_dir)
        else:
            print("Failed to fetch image. Status code:", response.status_code)

# 主函数
def main():
    base_path = r'C:\Users\Administrator\Downloads\Draw Dream'  # 设置基本路径
    user_input = input("Please describe your dream: ")  # 获取用户输入的梦境描述
    style_choice = input("Enter the number for your preferred style (1-9): ")  # 获取用户选择的图像风格
    enriched_text = generate_text(user_input)  # 生成文本

    if enriched_text:
        image_url = generate_image(enriched_text, style_choice)  # 生成图像
        if image_url:
            download_and_crop_image(image_url, base_path)  # 下载并裁剪图像

            images_folder = os.path.join(base_path, 'cropped_images')
            output_video_path = os.path.join(base_path, 'result.mp4')

            frame_rate = 0.5  # 每帧2秒
            size = (1920, 1080)  # 视频尺寸
            create_video_from_images(images_folder, output_video_path, frame_rate, size)  # 创建视频


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("An error occurred:", str(e))
