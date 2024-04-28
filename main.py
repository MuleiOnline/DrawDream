from prompt import generate_text
from image import generate_image, download_and_crop_image
from video import create_video_from_images
import os

def main():
    base_path = r'C:\Users\Administrator\Downloads\Draw Dream'
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

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print("An error occurred:", str(e))

# You woke up lying on the floor, rubbing your eyes, and found yourself in a gothic style room. You feel a little scared, as if someone is watching you, when the door to the room is pushed open

