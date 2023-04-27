import streamlit as st
import numpy as np
import cv2

from utils.utils import validate_url, uploader, get_image, FILE_TYPES
from PIL import Image

URL = "https://globalgovernanceforum.org/wp-content/uploads/2020/11/immanuel-kant.jpg"


def show_cols():
    # input of parameters for OpenCV.GaussianBlur
    c1, c2 = st.columns(2)
    with c1:
        dim = st.number_input("Kernel size:", min_value=1, max_value=99, value=5, step=2)
    with c2:
        sig = st.number_input("Sigma:", min_value=1, max_value=99, value=8, step=1)

    return c1, c2, dim, sig


def normalize(x, mu, sd):
    return 1 / (np.sqrt(2 * np.pi) * sd) * np.e ** (-np.power((x-mu) / sd,2) / 2)


def gaussian_kernel(size, sigma=1):
    kernel_1d = np.linspace(-(size // 2), size // 2, size)
    for i in range(size):
        kernel_1d[i] = normalize(kernel_1d[i], 0, sigma)
    kernel_2d = np.outer(kernel_1d.T, kernel_1d.T)

    kernel_2d *= 1.0 / kernel_2d.max()

    return kernel_2d


def convolution(image, kernel, column, average=False):
    with column:
        st.write(f"Image size:{image.shape}")
        st.write(f"Kernel size: {kernel.shape}")

        image_row, image_col = image.shape
        kernel_row, kernel_col = kernel.shape

        output = np.zeros(image.shape)

        pad_height = int((kernel_row - 1) / 2)
        pad_width = int((kernel_col - 1) / 2)

        padded_image = np.zeros((image_row + (2 * pad_height), image_col + (2 * pad_width)))

        padded_image[pad_height:padded_image.shape[0] - pad_height, pad_width:padded_image.shape[1] - pad_width] = image

        for row in range(image_row):
            for col in range(image_col):
                output[row, col] = np.sum(kernel * padded_image[row:row + kernel_row, col:col + kernel_col])
                if average:
                    output[row, col] /= kernel.shape[0] * kernel.shape[1]

        st.write(f"Size of the output image: {output.shape}")

        output_img = Image.fromarray((np.uint8(output)))

    return output_img


def gaussian_blur(image, kernel_size, sigma, col):
    kernel = gaussian_kernel(kernel_size, sigma=sigma)
    return convolution(image, kernel, col, average=True)


def main():
    st.markdown("## Laboratory work №1")
    st.markdown("### **Title**: Gaussian blur")
    st.markdown("---")

    st.markdown("""In image processing, a Gaussian blur (also known as Gaussian smoothing) is the result of blurring an
    image by a Gaussian function (named after mathematician and scientist Carl Friedrich Gauss).It is a widely used 
    effect in graphics software, typically to reduce image noise and reduce detail. The visual effect of this blurring 
    technique is a smooth blur resembling that of viewing the image through a translucent screen, distinctly different 
    from the bokeh effect produced by an out-of-focus lens or the shadow of an object under usual illumination. 
    Gaussian smoothing is also used as a pre-processing stage in computer vision algorithms in order to enhance image
    structures at different scales—see scale space representation and scale space implementation.""")
    st.markdown("---")

    user_img = uploader(st.file_uploader("Upload your image:", type=FILE_TYPES))
    user_url = validate_url(st.text_input(f"Insert url of your image {FILE_TYPES}: ", URL))

    _, gray_image = get_image(user_img, user_url)

    func = st.radio(
        "Choose your filter:", (
            "1. OpenCV GaussianBlur",
            "2. Step by step implementation",
        ),
        index=1
    )

    if func[:1] == "1":
        c1, c2,dimension, sigma = show_cols()

        res = cv2.GaussianBlur(gray_image, (dimension, dimension), sigma)

        with c2:
            st.image(res, width=300)

    elif func[:1] == "2":
        c1, c2, dimension, sigma = show_cols()
        res = gaussian_blur(gray_image, dimension, sigma, c1)

        with c2:
            st.image(res, width=300)


if __name__ == "__main__":
    main()

