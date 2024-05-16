import streamlit as st
from PIL import Image, ImageOps
import io
import zipfile


st.markdown("# Panorama converter. Cylindrical to spherical")
st.markdown("Actually, just adds black stripes to the image")
st.image("demonstration.png")
uploaded_files = st.file_uploader("Upload images", type=['jpg', 'jpeg', 'png'], accept_multiple_files=True)
bordered_images = []
stripes_width = st.slider('Stripes width in % of image', min_value=0.0, max_value=200.0, value=100.0, step=1.0) / 100

if uploaded_files is not None:
    st.markdown("Scroll down for the dowload button") 
    for uploaded_file in uploaded_files:
        image_data = uploaded_file.read()
        img = Image.open(io.BytesIO(image_data))

        stripes = int(img.size[1] * stripes_width)
        bord = ImageOps.expand(img, border=(0, stripes, 0, stripes), fill="black")
        bordered_images.append((uploaded_file.name, bord))
        st.image(bord)
    
    zip_buffer = io.BytesIO()
    with st.spinner('Please wait...'):
        with zipfile.ZipFile(zip_buffer, "a", zipfile.ZIP_DEFLATED) as zf:
            for name, img in bordered_images:

                img_buffer = io.BytesIO()
                img.save(img_buffer, format="PNG")
                
                zf.writestr(name, img_buffer.getvalue())

    st.download_button(
        label="Download all",
        data=zip_buffer,
        file_name="processed_images.zip",
        mime="application/zip"
    )
    
