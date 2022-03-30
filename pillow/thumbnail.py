import os
from pathlib import Path
from PIL import Image


def thumbnails(images, image_name, store_path, index, size):
    """Change image's size if selected and save all files in selected directory."""
    i = 0
    for image in images:
        # Resize image keeping it's original aspect ratio
        if index == 1:
            image.thumbnail(size)

        # Resize image into selected aspect ratio
        if index == 2:
            width, height = size
            # Make sure selected width is not bigger than image's width
            if width > image.size[0]:
                width = image.size[0]

            # Make sure selected height is not bigger than image's height
            if height > image.size[1]:
                height = image.size[1]
            image = image.resize([width, height], Image.ANTIALIAS)

        # Prepare edited filename for saving
        filename = os.path.basename(image_name[i])
        filename = os.path.splitext(filename)[0]
        filename += "_edited"
        filename = Path(store_path + "/" + filename + ".jpeg")
        # Save image(s)
        image.save(filename, "JPEG")
        i += 1
