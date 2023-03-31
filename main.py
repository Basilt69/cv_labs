import streamlit as st

from lab_01 import gauss_blur



st.sidebar.image('logo.png', width=300)


def header():
    author = """
        made by [Basil Tkachenko](https://github.com/Basilt69)
        for **Introduction to Computer vision labs**
        in [BMSTU](https://bmstu.ru) 
    """

    st.header("BMSTU, University department: Informatics and software development - 7")
    st.markdown("**Course title:**Introduction to computer vision")
    st.markdown("**University lecturer**: Kivva K.A.")
    st.markdown("**Student:** Tkachenko B.M.")
    st.sidebar.markdown(author)

def main():
    header()
    lab = st.sidebar.radio(
        "Select your lab:", (
            "1. Gaussian blur",
        ),
        index=0
    )

    if lab[:1] == "1":
        gauss_blur.main()



if __name__ == "__main__":
    main()
