import streamlit as st
import pandas as pd
import os
from io import BytesIO

# Set up our App
st.set_page_config(page_title="💿Data Sweeper by Zeejay🙅‍♂️", layout="wide")
st.title("💿Data Sweeper by ZeeJay🙅‍♂️")
st.write("Transform your files between CSV and Excel formats with built-in data cleaning and visualization!")

# File uploader
uploaded_files = st.file_uploader("Upload your files (CSV or Excel):", type=["csv", "xlsx"], accept_multiple_files=True)

if uploaded_files:
    for file in uploaded_files:
        file_ext = os.path.splitext(file.name)[-1].lower()

        if file_ext == ".csv":
            df = pd.read_csv(file)
        elif file_ext == ".xlsx":
            df = pd.read_excel(file, engine="openpyxl")  # Explicitly specify the engine
        else:
            st.error(f"Unsupported file format: {file_ext}")
            continue

        # Display info about the file
        st.write(f"**File name:** {file.name}")
        st.write(f"**File Size:** {file.size/1024:.2f} KB")

        # Show preview
        st.write("🔍Preview the Head of the DataFrame:")
        st.dataframe(df.head())

        # Data Cleaning Options
        st.subheader("🛠️ Data Cleaning Options")
        if st.checkbox(f"Clean Data for {file.name}"):
            col1, col2 = st.columns(2)

            with col1:
                if st.button(f"Remove Duplicates from {file.name}"):
                    df.drop_duplicates(inplace=True)
                    st.write("✅ Duplicates removed!")

            with col2:
                if st.button(f"Fill Missing Values for {file.name}"):
                    numeric_cols = df.select_dtypes(include=["number"]).columns
                    df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
                    st.write("✅ Missing values have been filled!")

        # Choose Specific Columns
        st.subheader("🎯 Choose Columns to Convert")
        columns = st.multiselect(f"Select Columns for {file.name}", list(df.columns), default=list(df.columns))
        df = df[columns]

        # Create Visualizations
        st.subheader("📊 Data Visualization")
        if st.checkbox(f"Show Visualizations for {file.name}"):
            st.bar_chart(df.select_dtypes(include="number").iloc[:, :2])

        # Conversion Options
        st.subheader("⌛ Conversion Options")
        conversion_type = st.radio(f"Select Conversion Type", ["CSV", "Excel"], key=file.name)

        # **Define `buffer` before the button is clicked**
        buffer = BytesIO()
        file_name = None
        mime_type = None

        if st.button(f"Convert {file.name}"):
            if conversion_type == "CSV":
                df.to_csv(buffer, index=False)
                file_name = file.name.replace(file_ext, ".csv")
                mime_type = "text/csv"

            elif conversion_type == "Excel":
                df.to_excel(buffer, index=False, engine="openpyxl")  # Ensure openpyxl is used
                file_name = file.name.replace(file_ext, ".xlsx")
                mime_type = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            
            buffer.seek(0)
            st.success(f"✅ {file.name} converted to {conversion_type}!")

        # **Check if conversion was done before allowing download**
        if file_name and mime_type:
            st.download_button(
                label=f"⬇️ Download {file.name} as {conversion_type} file",
                data=buffer,
                file_name=file_name,
                mime=mime_type
            )

# Footer
st.success("🎉 All files processed!")
st.write("Built by ❤️ by [Zohaib Javed](https://www.linkedin.com/in/zohaib-javd/)")
