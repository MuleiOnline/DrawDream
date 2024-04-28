import cv2
import os

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

