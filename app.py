import streamlit as st
import pandas as pd
from datetime import datetime
import io
import os

# Authentication credentials
USERNAME = "EZDash"
PASSWORD = "EZDash@2026"

def authenticate():
    """Handle user authentication"""
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
    
    if not st.session_state.authenticated:
        st.title("🔐 EZ Statement Converter - Login")
        
        with st.form("login_form"):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submit = st.form_submit_button("Login")
            
            if submit:
                if username == USERNAME and password == PASSWORD:
                    st.session_state.authenticated = True
                    st.success("Login successful! Please refresh the page or click below.")
                    if st.button("Continue to App"):
                        pass  # This will trigger a rerun naturally
                else:
                    st.error("Invalid username or password")
        
        if not st.session_state.authenticated:
            st.stop()

def process_csv_content(file_content):
    """Process the CSV content using the original logic"""
    # Convert bytes to string and split into lines
    content_str = file_content.decode('utf-8')
    lines = content_str.split('\n')
    
    # Step 1: Clean raw lines
    all_lines = []
    for line in lines:
        stripped = line.strip()
        if not stripped or set(stripped) <= {"-", "|"}:
            continue  # Skip empty lines and separator lines
        all_lines.append(stripped)
    
    # Step 2: Combine multiline records (starting with 1D, 2C, etc.)
    combined_rows = []
    current_row = ""
    
    for line in all_lines:
        if line[:2] in ("1D", "2C"):  # Add more types if needed
            if current_row:
                combined_rows.append(current_row)
            current_row = line
        else:
            current_row += " " + line
    
    if current_row:
        combined_rows.append(current_row)
    
    # Step 3: Split into columns using pipe (|) delimiter
    all_data = [row.split("|") for row in combined_rows]
    
    # Step 4: Create a DataFrame
    df = pd.DataFrame(all_data)
    
    # Step 5: Clean DataFrame
    df = df.dropna(axis=1, how="all")  # Drop columns that are entirely empty
    df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)
    
    # Step 6: Rename first few columns for clarity
    column_names = {
        0: "Type",
        1: "Amount", 
        2: "TransactionID",
        3: "Details1",
        4: "Details2",
        5: "FromParty",
        6: "ToParty",
        7: "Code",
        8: "Debit",
        9: "Credit"
    }
    
    # Only rename columns that exist
    existing_columns = {k: v for k, v in column_names.items() if k < len(df.columns)}
    df.rename(columns=existing_columns, inplace=True)
    
    return df

def main():
    """Main application"""
    authenticate()
    
    st.title("📊 EZ Statement Converter")
    st.markdown("Convert your EZ_STMT.csv files to clean Excel format")
    
    # Logout button
    if st.button("Logout"):
        st.session_state.authenticated = False
        st.success("Logged out successfully! Please refresh the page.")
    
    st.divider()
    
    # File upload
    uploaded_file = st.file_uploader(
        "Upload your EZ_STMT.csv file", 
        type=['csv'],
        help="Select the CSV file you want to convert"
    )
    
    if uploaded_file is not None:
        try:
            # Show file details
            st.success(f"✅ File uploaded: {uploaded_file.name}")
            st.info(f"File size: {uploaded_file.size:,} bytes")
            
            # Process the file
            with st.spinner("Processing your file..."):
                file_content = uploaded_file.read()
                df = process_csv_content(file_content)
            
            st.success(f"✅ Processing complete! Found {len(df)} records")
            
            # Show preview
            st.subheader("📋 Data Preview")
            st.dataframe(df.head(10), use_container_width=True)
            
            if len(df) > 10:
                st.info(f"Showing first 10 rows of {len(df)} total records")
            
            # Generate Excel file
            date_suffix = datetime.now().strftime("%d%b")
            output_filename = f"EZ_Statement_Cleaned_{date_suffix}.xlsx"
            
            # Create Excel file in memory
            excel_buffer = io.BytesIO()
            df.to_excel(excel_buffer, index=False, engine='openpyxl')
            excel_buffer.seek(0)
            
            # Download button
            st.download_button(
                label="📥 Download Excel File",
                data=excel_buffer.getvalue(),
                file_name=output_filename,
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
            
            # Show statistics
            st.subheader("📈 File Statistics")
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("Total Records", len(df))
            
            with col2:
                st.metric("Total Columns", len(df.columns))
            
            with col3:
                if 'Type' in df.columns:
                    unique_types = df['Type'].nunique()
                    st.metric("Unique Types", unique_types)
                else:
                    st.metric("Data Quality", "✅ Good")
                    
        except Exception as e:
            st.error(f"❌ Error processing file: {str(e)}")
            st.info("Please make sure you uploaded a valid EZ_STMT.csv file")
    
    else:
        st.info("👆 Please upload a CSV file to get started")
        
        # Show instructions
        with st.expander("📖 How to use this tool"):
            st.markdown("""
            1. **Upload** your EZ_STMT.csv file using the file uploader above
            2. **Wait** for the processing to complete
            3. **Preview** your data to ensure it looks correct
            4. **Download** the cleaned Excel file
            
            **What this tool does:**
            - Removes empty lines and separator lines
            - Combines multiline records into single rows
            - Splits data using pipe (|) delimiters
            - Adds descriptive column headers
            - Exports to Excel format with date suffix
            """)

if __name__ == "__main__":
    main()