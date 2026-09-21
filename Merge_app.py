import streamlit as st
from pypdf import PdfWriter, PdfReader
from PIL import Image
import tempfile
import base64


# -----------------------------
# Page Configuration
# -----------------------------

st.set_page_config(
    page_title="PDF / Image File Merger",
    page_icon="📄",
    layout="centered"
)


# -----------------------------
# Title
# -----------------------------

st.title("📄 PDF / Image File Merger")

st.write(
    "Upload PDF or image files, view them, merge them into one PDF, "
    "and view or download the merged PDF."
)


# -----------------------------
# Upload Files
# -----------------------------

st.subheader("1. Upload PDF / Image Files")

uploaded_files = st.file_uploader(
    "Choose PDF or Image files",
    type=["pdf", "jpg", "jpeg", "png"],
    accept_multiple_files=True
)


# -----------------------------
# Upload Status
# -----------------------------

if uploaded_files:
    st.success("✅ Files uploaded successfully!")
else:
    st.info("📂 Please upload PDF or image files.")


# -----------------------------
# Remove Files
# -----------------------------

if uploaded_files:

    if st.button("🗑️ Remove Files"):

        st.session_state["uploaded_files"] = []

        st.rerun()


# -----------------------------
# View Uploaded Files
# -----------------------------

if uploaded_files:

    if st.button("👁️ View Files"):

        st.subheader("📁 Uploaded Files")

        for file in uploaded_files:

            st.write(f"📄 **{file.name}**")

            file_type = file.name.lower()

            # Show images
            if file_type.endswith((".jpg", ".jpeg", ".png")):

                image = Image.open(file)

                st.image(
                    image,
                    caption=file.name,
                    use_container_width=True
                )

            # Show PDF
            elif file_type.endswith(".pdf"):

                pdf_bytes = file.getvalue()

                base64_pdf = base64.b64encode(
                    pdf_bytes
                ).decode("utf-8")

                pdf_display = f"""
                <iframe
                    src="data:application/pdf;base64,{base64_pdf}"
                    width="100%"
                    height="600"
                    type="application/pdf">
                </iframe>
                """

                st.markdown(
                    pdf_display,
                    unsafe_allow_html=True
                )


# -----------------------------
# Merge Files
# -----------------------------

st.subheader("2. Merge PDF / Image Files")


if uploaded_files:

    if st.button(
        "🔄 Merge PDF / Image Files",
        type="primary"
    ):

        try:

            # Create temporary output PDF
            output_path = tempfile.NamedTemporaryFile(
                delete=False,
                suffix=".pdf"
            ).name

            pdf_writer = PdfWriter()


            # Process each file
            for uploaded_file in uploaded_files:

                file_name = uploaded_file.name.lower()


                # -----------------------------
                # PDF File
                # -----------------------------

                if file_name.endswith(".pdf"):

                    reader = PdfReader(uploaded_file)

                    for page in reader.pages:

                        pdf_writer.add_page(page)


                # -----------------------------
                # Image File
                # -----------------------------

                elif file_name.endswith(
                    (".jpg", ".jpeg", ".png")
                ):

                    image = Image.open(
                        uploaded_file
                    ).convert("RGB")


                    image_path = tempfile.NamedTemporaryFile(
                        delete=False,
                        suffix=".pdf"
                    ).name


                    image.save(
                        image_path,
                        "PDF"
                    )


                    reader = PdfReader(
                        image_path
                    )


                    for page in reader.pages:

                        pdf_writer.add_page(page)


            # -----------------------------
            # Save Merged PDF
            # -----------------------------

            with open(
                output_path,
                "wb"
            ) as output_file:

                pdf_writer.write(
                    output_file
                )


            # Store merged PDF path
            st.session_state[
                "merged_pdf"
            ] = output_path


            st.success(
                "✅ Files merged successfully!"
            )


        except Exception as e:

            st.error(
                f"❌ Error: {str(e)}"
            )


# -----------------------------
# View / Download Merged PDF
# -----------------------------

if "merged_pdf" in st.session_state:

    merged_pdf = st.session_state[
        "merged_pdf"
    ]


    st.subheader("3. Merged PDF")


    # -----------------------------
    # View Merged PDF
    # -----------------------------

    if st.button("👁️ View Merged PDF"):

        with open(
            merged_pdf,
            "rb"
        ) as pdf_file:

            pdf_bytes = pdf_file.read()


        base64_pdf = base64.b64encode(
            pdf_bytes
        ).decode("utf-8")


        pdf_display = f"""
        <iframe
            src="data:application/pdf;base64,{base64_pdf}"
            width="100%"
            height="700"
            type="application/pdf">
        </iframe>
        """


        st.markdown(
            pdf_display,
            unsafe_allow_html=True
        )


    # -----------------------------
    # Download Merged PDF
    # -----------------------------

    with open(
        merged_pdf,
        "rb"
    ) as pdf_file:

        st.download_button(
            label="⬇️ Download Merged PDF",
            data=pdf_file,
            file_name="merged_files.pdf",
            mime="application/pdf"
        )
