import sys
import os
from threading import Thread
from PIL import Image, ImageDraw, ImageFont

# TODO: Create a progress bar.


def watermark(path, filename, save_path, text='Camis Photography'):
    """
    This method actually adds the watermark text to the image.
    :param path: Path to the image
    :param filename: image name
    :param save_path: The path to the destination folder for the new file
    :param text: The text to add. Default is Camis Photography
    :return:
    """
    image = Image.open(os.path.join(path, filename)).convert('RGBA')
    image_watermark = Image.new('RGBA', image.size, (255, 255, 255, 0))

    draw = ImageDraw.Draw(image_watermark)

    width, height = image.size
    font = ImageFont.truetype('arial.ttf', int(height/15))
    text_width, text_height = draw.textsize('arial.ttf', font)
    x = width / 2 - text_width * 1.5
    y = height

    draw.text((x, y / 6), text, fill=(0, 0, 0, 95), font=font)
    draw.text((x, y * 3 / 6), text, fill=(0, 0, 0, 95), font=font)
    draw.text((x, y * 5 / 6), text, fill=(0, 0, 0, 95), font=font)
    derp = Image.alpha_composite(image, image_watermark)
    filename = os.path.splitext(filename)[0]
    derp.save(os.path.join(save_path, filename + '.png'))


def make_marked_folder(folder_path):
    """
    This creates a folder for the new watermarked images
    :param folder_path: The path to the current folder
    :return: the new folder
    """
    new_folder = folder_path + 'WaterMarked'
    os.makedirs(new_folder)
    print("Folder Created: " + new_folder)
    return new_folder


def mark_images(target_folder, save_folder):
    """
    TODO: Recycle a pool of threads instead of creating one for each image.
    This method cycles through the images and starts a thread for each image.
    :param target_folder: The folder containing the images
    :param save_folder: the folder that all teh images should be saved in
    :return:
    """
    for filename in os.listdir(target_folder):
        if filename.endswith('.jpg') or filename.endswith('.jpeg') or filename.endswith('.png'):
            image = Thread(target=watermark, args=(target_folder, filename, save_folder,))
            image.start()
            image.join()


if __name__ == "__main__":
    folder = sys.argv[1]
    marked_folder = make_marked_folder(folder)
    mark_images(folder, marked_folder)



