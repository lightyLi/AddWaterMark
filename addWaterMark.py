import os
import argparse
from PIL import Image, UnidentifiedImageError

def change_transparency(img, value):
    img=img.convert('RGBA') 
    alpha = img.split()[3]
    new_alpha = alpha.point(lambda i: int(i * value)) # Value is the transparency of images
    img.putalpha(new_alpha) # Merge the RGB channels with the new alpha channel
    return img

def merge_logo(img, logo, position, padding, scale):
    # Get the mask of the logo
    logo_mask = logo.split()[3]

    imageWidth, imageHeight = img.size

    shorter_side = min(imageWidth, imageHeight)
    new_logo_width = int(shorter_side * scale/100)
    logo_aspect_ratio = logo.width / logo.height
    new_logo_height = int(new_logo_width / logo_aspect_ratio)

    # Resize the logo and its mask
    logo = logo.resize((new_logo_width, new_logo_height))
    logo_mask = logo_mask.resize((new_logo_width, new_logo_height))

    paste_x, paste_y = 0, 0
    if position == 'topleft':
        paste_x, paste_y = padding, padding
    elif position == 'topright':
        paste_x, paste_y = imageWidth - new_logo_width - padding, padding
    elif position == 'bottomleft':
        paste_x, paste_y = padding, imageHeight - new_logo_height - padding
    elif position == 'bottomright':
        paste_x, paste_y = imageWidth - new_logo_width - padding, imageHeight - new_logo_height - padding
    elif position == 'center':
        paste_x, paste_y = (imageWidth - new_logo_width) // 2, (imageHeight - new_logo_height) // 2

    try:
        img.paste(logo, (paste_x, paste_y), logo_mask)  # log_mask is the shape of pasted image
    except Exception as e:
        print(f"An error occurred: {e}")
        return
    return img

def add_watermark(directory, logo_path, position, new_directory, padding, transparency, scale, is_store_original_info):
    """
    Add a watermark to images in the specified directory and it's subdirectory.
    
    Args:
    - directory (str): The directory containing images to be watermarked.
    - logo_path (str): Path to the watermark logo.
    - position (str): Position of the watermark on the image.
    - new_directory (str): Directory to save watermarked images.
    - padding (int): Padding around the logo in pixels.
    - transparency (float): Set the transparency of the logo image.
    - scale (int): Change the scale of the logo image
    """
    EXTS = ('.jpg', '.jpeg', '.png')

    try:
        original_logo = Image.open(logo_path) # import watermark pic data
    except UnidentifiedImageError:
        print(f"Failed to read logo from {logo_path}. Ensure it's a valid image format.")
        return
    except Exception as e:
        print(f"An error occurred: {e}")
        return

    # Change the logo transparency
    original_logo = change_transparency(original_logo, transparency)


    # Using os.walk() to make folder image search recursive
    for dirpath, dirnames, filenames in os.walk(directory):
        for filename in filenames:
            if filename.lower().endswith(EXTS) and filename != os.path.basename(logo_path):
                full_path = os.path.join(dirpath, filename)
                try:
                    image = Image.open(full_path)
                except UnidentifiedImageError:
                    print(f"Skipped {filename}. Unsupported image format.")
                    continue
                except Exception as e:
                    print(f"An error occurred while processing {filename}: {e}")
                    continue
                
                image_path = os.path.join(dirpath, filename)
                image = Image.open(image_path)  # Load image data
                
                # Merge the logo and image
                new_image = merge_logo(image, original_logo, position, padding, scale)
               
                # Generate the relative path
                relative_path = os.path.relpath(dirpath, directory)
                save_directory = new_directory if new_directory else directory
                final_save_directory = os.path.join(save_directory, relative_path)
                # Ensure the new directory exists
                if not os.path.exists(final_save_directory):
                    os.makedirs(final_save_directory)
                image_store_path = os.path.join(final_save_directory, filename)

                # Check if the image mode is 'RGBA' and convert it to 'RGB'
                if new_image.mode == 'RGBA':
                    new_image = new_image.convert('RGB')
                if is_store_original_info:
                    original_info = image.info
                else:
                    original_info = []

                image.save(image_store_path, quality= 'keep', **original_info)  # Using "keeep" parampter to store the image in original quality.
                print('Added watermark to ' + image_store_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="A script to add watermarks to images. Given a directory, this will traverse through all its images and apply the specified watermark. The resulting watermarked images can be saved in the same directory or a new specified directory, maintaining the original directory structure.")

    parser.add_argument('dir', 
                        help="Directory containing the images you want to watermark. The script will search recursively within this directory.",
                        metavar='SourceDirectory')

    parser.add_argument('logo', 
                        help="Path to the logo image that will be used as the watermark.",
                        metavar='WatermarkLogoPath')

    parser.add_argument('--pos', 
                        choices=['topleft', 'topright', 'bottomleft', 'bottomright', 'center'], 
                        default='center',
                        help="Specifies the position of the watermark on the image. Default is 'center'.")

    parser.add_argument('--new_dir',
                        default=None, 
                        help="An optional directory where the watermarked images will be saved. If not provided, watermarked images will overwrite originals in the source directory. The original directory structure will be maintained.",
                        metavar='DestinationDirectory')

    parser.add_argument('--padding', 
                        type=int, 
                        default=0,
                        help="Specifies the padding (in pixels) around the watermark, useful when watermark is positioned at the corners. Default is 0, meaning no padding.")
    
    parser.add_argument('--transparency',
                        type=float, 
                        default=1,
                        help="Set the watermark transparency, the value must be between 0~1")

    parser.add_argument('--scale',
                        type=float, 
                        default=20,
                        help="Resize the watermark based on a percentage of the image's width. E.g., for 10% of the image's width, provide 10.")
    
    parser.add_argument('--keep_info',
                        type=bool, 
                        default=True,
                        help="Set True to keep the original info of image")

    args = parser.parse_args()

    add_watermark(args.dir, args.logo, args.pos, args.new_dir, args.padding, args.transparency, args.scale, args.keep_info)
