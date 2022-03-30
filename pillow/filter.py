from PIL import ImageFilter, ImageOps


def image_filter(images, index):
    """Apply selected filter to image(s)"""
    i = 0
    for image in images:
        # Apply "Blur" filter
        if index == 1:
            images[i] = image.filter(ImageFilter.BLUR)

        # Apply "Contour" filter
        if index == 2:
            images[i] = image.filter(ImageFilter.CONTOUR)

        # Apply "Detail" filter
        if index == 3:
            images[i] = image.filter(ImageFilter.DETAIL)

        # Apply "Edge Enhance" filter
        if index == 4:
            images[i] = image.filter(ImageFilter.EDGE_ENHANCE)

        # Apply "Edge Enhance More" filter
        if index == 5:
            images[i] = image.filter(ImageFilter.EDGE_ENHANCE_MORE)

        # Apply "Emboss" filter
        if index == 6:
            images[i] = image.filter(ImageFilter.EMBOSS)

        # Apply "Find Edges" filter
        if index == 7:
            images[i] = image.filter(ImageFilter.FIND_EDGES)

        # Apply "Smooth" filter
        if index == 8:
            images[i] = image.filter(ImageFilter.SMOOTH)

        # Apply "Smooth More" filter
        if index == 9:
            images[i] = image.filter(ImageFilter.SMOOTH_MORE)

        # Apply "Sharpen" filter
        if index == 10:
            images[i] = image.filter(ImageFilter.SHARPEN)

        # Apply "Invert Colors" filter
        if index == 11:
            images[i] = ImageOps.invert(image)

        # Apply "Black and White" filter
        if index == 12:
            images[i] = image.convert("L")

        # Apply "Auto Contrast" filter
        if index == 13:
            images[i] = ImageOps.autocontrast(image)

        # Apply "Mirror" filter
        if index == 14:
            images[i] = ImageOps.mirror(image)

        # Apply "Solarize" filter
        if index == 15:
            images[i] = ImageOps.solarize(image, threshold=128)

        # Apply "Remove RED Color" filter
        if index == 16:
            # Get image's parameters for quicker processing
            image_sample = image.load()
            image_size = image.size
            # Remove image's Red Channel
            for x in range(image_size[0]):
                for y in range(image_size[1]):
                    r, g, b = image_sample[x, y]
                    image_sample[x, y] = 0, g, b

        # Apply "Remove GREEN Color" filter
        if index == 17:
            # Get image's parameters for quicker processing
            image_sample = image.load()
            image_size = image.size
            # Remove image's Green Channel
            for x in range(image_size[0]):
                for y in range(image_size[1]):
                    r, g, b = image_sample[x, y]
                    image_sample[x, y] = r, 0, b

        # Apply "Remove BLUE Color" filter
        if index == 18:
            # Get image's parameters for quicker processing
            image_sample = image.load()
            image_size = image.size
            # Remove image's Blue Channel
            for x in range(image_size[0]):
                for y in range(image_size[1]):
                    r, g, b = image_sample[x, y]
                    image_sample[x, y] = r, g, 0

        i += 1

    return images
