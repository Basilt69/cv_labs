import plotly.express as px
import streamlit as st
import numpy as np
import cv2

from utils.utils import FILE_TYPES, uploader, validate_url, get_image

URL = "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTWe0RVcWbYG_kkoc-Bsz8t8gVW_eX_8bSV3h23C209nTGtrl3vNC3yA7zYwio_d0FGsPA&usqp=CAU"


def description():
    task = """
        1. Otsu method (OpenCV)
        2. Otsu method(handmade)
        3. Bradley method(32UC1) 
    """

    st.markdown("### Laboratory work №2")
    st.markdown("**Title:** Binarisation")

    if st.checkbox("Show task:"):
        st.write(task)
    st.markdown("---")


def show_cols(c1, c2):
    with c1:
        threshold = st.number_input("Threshold", min_value=1, max_value=999, value=15, step=1)
    with c2:
        max_value = st.number_input("Max:", min_value=1, max_value=999, value=255, step=1)

    return threshold, max_value


def otsu_binary(img):
    pixel_number = img.shape[0] * img.shape[1]
    mean_weight = 1.0 / pixel_number
    hist, bins = np.histogram(img, np.array(range(0, 256)))

    fig = px.histogram(hist, nbins=len(bins))
    st.plotly_chart(fig, use_container_width=True)

    final_thresh = -1
    final_value = -1
    for t in bins[1:-1]:
        wb = np.sum(hist[:t]) * mean_weight
        wf = np.sum(hist[t:]) * mean_weight

        mub = np.mean(hist[:t])
        muf = np.mean(hist[t:])

        value = wb * wf * (mub - muf) ** 2

        if value > final_value:
            final_thresh = t
            final_value = value
    final_img = img.copy()
    st.write(f"Threshold: {final_thresh}")
    final_img[img > final_thresh] = 255
    final_img[img < final_thresh] = 0
    return final_img


def bradley_binary(img, t):
    # default window size is round(cols/8)
    s = np.round(img.shape[1] / 8)

    # compute integral image
    int_img = np.cumsum(np.cumsum(img, axis=1), axis=0)

    # define grid of points
    (rows, cols) = img.shape[:2]
    (X, Y) = np.meshgrid(np.arange(cols), np.arange(rows))

    # make into 1D grid of coordinates for easier access
    X = X.ravel()
    Y = Y.ravel()

    # ensure s is even so that are able to index into the image properly
    s = s + np.mod(s, 2)

    # access the four corners of each neighbourhood
    x1 = X - s / 2
    x2 = X + s / 2
    y1 = Y - s / 2
    y2 = Y + s / 2

    # ensures no coordinates are out of bounds
    x1[x1 < 0] = 0
    x2[x2 >= cols] = cols - 1
    y1[y1 < 0] = 0
    y2[y2 >= rows] = rows - 1

    # ensures coordinates are integer
    x1 = x1.astype(int)
    x2 = x2.astype(int)
    y1 = y1.astype(int)
    y2 = y2.astype(int)

    # count how many pixels are in each neighbourhood
    count = (x2 - x1) * (y2 - y1)

    # compute the row and column coordinates to access each corner of the neighbourhood for the integral image
    f1_x = x2
    f1_y = y2
    f2_x = x2
    f2_y = y1 - 1
    f2_y[f2_y < 0] = 0
    f3_x = x1
    f3_x[f3_x < 0] = 0
    f3_y = y2
    f4_x = f3_x
    f4_y = f2_y

    # compute areas of each window
    sums = int_img[f1_y, f1_x] - int_img[f2_y, f2_x] - int_img[f3_y, f3_x] + int_img[f4_y, f4_x]

    # compute thresholded image and reshape into a 2D grid
    out = np.ones(rows * cols, dtype=bool)
    out[img.ravel() * count <= sums * (100.0 - t) / 100.0] = False

    # also convert back to uint8
    out = 255 * np.reshape(out, (rows, cols)).astype(np.uint8)

    return out


def main():
    description()

    user_img = uploader(st.file_uploader("Upload image:", type=FILE_TYPES))
    user_url = validate_url(st.text_input(f"Insert image URL {FILE_TYPES}: ", URL))

    _, gray_image = get_image(user_img, user_url)

    method = st.radio(
        "Choose method:", {
            "1. OpenCV THRESH_OTSU",
            "2. Otsu method(handmade)",
            "3. Bradley method",
        },
        index=0
    )

    c1, c2 = st.columns(2)

    if method[:1] == "1":
        thresh, max_val = show_cols(c1, c2)
        final_thresh, final_img = cv2.threshold(src=gray_image, thresh=thresh, maxval=max_val, type=cv2.THRESH_OTSU)
        st.write(f"Threshold: {final_thresh}")

        with c2:
            st.image(final_img, width=300)

    if method[:1] == "2":
        res = otsu_binary(gray_image)

        with c2:
            st.image(res, width=300)

    if method[:1] == "3":
        thresh, _ = show_cols(c1, c2)
        res = bradley_binary(gray_image, thresh)
        with c2:
            st.image(res, width=300)


if __name__ == "__main__":
    main()