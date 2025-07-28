import streamlit as st
import pandas as pd
import os
import shutil
import zipfile
import tempfile
from tabular_tools import handle_missing_values
from image_tools import resize_images_recursive, delete_unwanted_formats_recursive

st.set_page_config(page_title="AI Data Cleaner", layout="centered")
st.title("🧼 AI-Powered Data Cleaning System")

data_type = st.radio("Select data type:", ["Tabular", "Image"])

uploaded_file = st.file_uploader("Upload your file", type=["csv", "xlsx", "zip"])

# 🧼 Tabular Logic
if data_type == "Tabular" and uploaded_file:
    try:
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(".xlsx"):
            df = pd.read_excel(uploaded_file)

        st.subheader("📊 Original Data Preview")
        st.dataframe(df.head())

        threshold = st.slider("Missing value threshold (%):", 0, 100, 2) / 100

        if st.button("🧹 Clean Tabular Data"):
            cleaned_df = handle_missing_values(df, threshold)
            st.success("✅ Cleaning complete!")

            st.subheader("✅ Cleaned Data Preview")
            st.dataframe(cleaned_df.head())

            csv = cleaned_df.to_csv(index=False).encode("utf-8")
            st.download_button("📥 Download Cleaned CSV", data=csv, file_name="cleaned_data.csv", mime="text/csv")

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

# 🧼 Image Logic
elif data_type == "Image" and uploaded_file:
    try:
        if uploaded_file.name.endswith(".zip"):
            temp_dir = tempfile.mkdtemp()
            zip_path = os.path.join(temp_dir, uploaded_file.name)
            with open(zip_path, "wb") as f:
                f.write(uploaded_file.read())

            extract_dir = os.path.join(temp_dir, "extracted")
            os.makedirs(extract_dir, exist_ok=True)

            with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                zip_ref.extractall(extract_dir)

            st.success("✅ ZIP extracted!")

            width = st.number_input("New Width:", value=224)
            height = st.number_input("New Height:", value=224)
            formats_to_delete = st.multiselect(
                "Select unwanted formats to delete:",
                [".webp", ".tiff", ".bmp", ".svg"]
            )

            if st.button("🧹 Clean Image Dataset"):
                resize_images_recursive(extract_dir, (width, height))
                deleted_count = delete_unwanted_formats_recursive(extract_dir, formats_to_delete)

                # Repack cleaned folder into new zip
                cleaned_zip_path = os.path.join(temp_dir, "cleaned_images.zip")
                shutil.make_archive(cleaned_zip_path.replace(".zip", ""), 'zip', extract_dir)

                st.success(f"✅ Cleaning done! {deleted_count} unwanted images deleted.")
                with open(cleaned_zip_path, "rb") as f:
                    st.download_button("📥 Download Cleaned ZIP", f.read(), file_name="cleaned_images.zip")

        else:
            st.error("❌ Please upload a ZIP file for image datasets.")

    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
