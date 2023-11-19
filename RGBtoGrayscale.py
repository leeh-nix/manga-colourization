import cv2
import os

# Path to the directory containing the colorized images
colorized_images_dir = "./dataset/colored"

# Path to the directory where grayscale images will be saved
grayscale_images_dir = "./dataset/grayscale"

if not os.path.exists(grayscale_images_dir):
    os.makedirs(grayscale_images_dir)

# Iterate through colorized images and convert them to grayscale
for filename in os.listdir(colorized_images_dir):
    if (
        filename.endswith(".jpg")
        or filename.endswith(".png")
        or filename.endswith(".jpeg")
    ):
        color_image = cv2.imread(os.path.join(colorized_images_dir, filename))

        # Converting RGB image to grayscale
        grayscale_image = cv2.cvtColor(color_image, cv2.COLOR_RGB2GRAY)

        # Save the image
        cv2.imwrite(os.path.join(grayscale_images_dir, filename), grayscale_image)
