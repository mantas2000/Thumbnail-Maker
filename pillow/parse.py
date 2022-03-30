from PIL import Image


def parse_photo(file_path):
    """Open image(s), remove Alpha Channel if image has it and store image(s)."""
    images = []
    for file_name in file_path:
        try:
            # Open file
            img = Image.open(file_name)
            # If image has Alpha Channel, remove it
            if img.mode == "RGBA":
                img = rgb_fix(img)
            # Store image
            images.append(img)

        # Check if file is supported
        except IOError:
            return None

    return images


def rgb_fix(image):
    """Remove Alpha Channel from image."""
    color = (255, 255, 255)
    # Convert all transparent pixels into white pixels
    rgb_image = Image.new('RGB', image.size, color)
    rgb_image.paste(image, mask=image.split()[3])
    # Return converted image
    return rgb_image
