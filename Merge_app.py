import streamlit as st
from pypdf import PdfWriter, PdfReader
from PIL import Image
import tempfile
import os


# --------------------------------------
# Page Configuration
# --------------------------------------

st.set_page_config(
    page_title="PDF / Image File Merger",
    page_icon="📄",
    layout="centered"
)


# --------------------------------------
# Title
# --------------------------------------

st.title("📄 PDF / Image File Merger")

st.write(
    "Upload PDF or image files and merge them into one PDF."
)


# --------------------------------------
# 1. Upload Files
# --------------------------------------

st.subheader("1. Upload PDF / Image Files")

uploaded_files = st.file_uploader(
    "Choose PDF or Image files",
    type=["pdf", "jpg", "jpeg", "png"],
    accept_multiple_files=True
)


# --------------------------------------
# Upload Status
# --------------------------------------

if uploaded_files:

    st.success("✅ Files uploaded successfully!")


# --------------------------------------
# 2. Display Uploaded Files
# --------------------------------------

st.subheader("2. Uploaded Files")

if uploaded_files:

    for file in uploaded_files:
        st.write(f"📄 {file.name}")

else:

    st.info("No files uploaded yet.")


# --------------------------------------
# Remove Files
# --------------------------------------

if uploaded_files:

    if st.button("🗑️ Remove Files"):

        st.session_state.clear()
        st.rerun()


# --------------------------------------
# 3. Merge Files
# --------------------------------------

st.subheader("3. Merge PDF / Image Files")

if uploaded_files:

    if st.button("🔄 Merge PDF / Image Files"):

        try:

            output_path = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            ).name

            pdf_writer = PdfWriter()

            for uploaded_file in uploaded_files:

                file_name = uploaded_file.name.lower()

                # ----------------------------------
                # PDF File
                # ----------------------------------

                if file_name.endswith(".pdf"):

                    reader = PdfReader(uploaded_file)

                    for page in reader.pages:
                        pdf_writer.add_page(page)

                # ----------------------------------
                # Image File
                # ----------------------------------

                elif file_name.endswith(
                    (".jpg", ".jpeg", ".png")
                ):

                    image = Image.open(uploaded_file).convert("RGB")

                    image_path = tempfile.NamedTemporaryFile(
                        delete=False,
                        suffix=".pdf"
                    ).name

                    image.save(image_path, "PDF")

                    reader = PdfReader(image_path)

                    for page in reader.pages:
                        pdf_writer.add_page(page)

            # ----------------------------------
            # Save Merged PDF
            # ----------------------------------

            with open(output_path, "wb") as output_file:

                pdf_writer.write(output_file)


            # ----------------------------------
            # 4. Status
            # ----------------------------------

            st.success(
                "✅ Files merged successfully!"
            )


            # ----------------------------------
            # 5. Download File
            # ----------------------------------

            with open(output_path, "rb") as file:

                st.download_button(
                    label="⬇️ 5. Download Merged File",
                    data=file,
                    file_name="merged_files.pdf",
                    mime="application/pdf"
                )


        except Exception as e:

            st.error(
                f"❌ Error: {str(e)}"
            )

else:

    st.warning(
        "⚠️ Please upload files before merging."
    )
