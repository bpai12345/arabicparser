import streamlit as st
from pdf2image import convert_from_path
import os
from ArabicOcr import arabicocr

# Create a Streamlit app title
st.title("Arabic Text Extraction")

# Create a file upload widget
uploaded_file = st.file_uploader("Upload a PDF file", type=["pdf"])

# Check if a file is uploaded
if uploaded_file:
    # Save the uploaded PDF as a temporary file
    with open("arabic_image.pdf", "wb") as temp_pdf:
        temp_pdf.write(uploaded_file.read())

    # Convert the PDF to images using pdf2image
    images = convert_from_path("arabic_image.pdf")

    # Create columns for layout
    col1, col2 = st.columns(2)

    # Select a page
    with col1:
        # Create a dropdown to select a page
        page_number = st.selectbox("Select a Page", range(len(images)))

        # Display the selected page image
        st.image(images[page_number])

    # Perform Arabic OCR on the selected page
    image_path = f"page-{page_number}.png"
    out_image = 'out.jpg'
    images[page_number].save(image_path)
    results = arabicocr.arabic_ocr(image_path, out_image)

    # Extract and display the text
    words = [result[1] for result in results]
    text = " ".join(words)

    # Display the text in the right column
    with col2:
        st.header("Extracted Text")
        st.text(text)

    # Save the extracted text as a text file
    with open('file.txt', 'w', encoding='utf-8') as myfile:
        myfile.write(text)

    # Clean up the temporary PDF file after processing
    if os.path.exists("arabic_image.pdf"):
        os.remove("arabic_image.pdf")

    # Clean up the temporary image file after processing
    if os.path.exists(image_path):
        os.remove(image_path)
