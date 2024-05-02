import requests
from PIL import Image
from io import BytesIO
import os

api_key = 'xxxxxxxxxxxx'


def generate_image(text, style):
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
    chosen_style = style_descriptions.get(style, "Flat style illustration")
    prompt = f"Based on the following plot, please generate six small images(with same size and full content) in the same image once in the {chosen_style}: {text}"

    # Define the API URL
    url_image = 'https://api.openai.com/v1/images/generations'

    data = {
        "model": "dall-e-3",
        "prompt": prompt,
        "size": "1024x1024",
        "quality": "standard",
        "n": 1
    }
    headers_image = {
        'Authorization': f'Bearer {api_key}',
        'Content-Type': 'application/json'
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
    else:
        print("Failed to fetch image. Status code:", response.status_code)
        print("Error data:", response.text)
    return None


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