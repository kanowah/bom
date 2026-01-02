<<<<<<< HEAD
# bom
clean excel
=======
# EZ Statement Converter

A Streamlit web application for converting EZ_STMT.csv files to clean Excel format.

## Features

- 🔐 Secure login authentication
- 📁 File upload interface
- 📊 Data preview and statistics
- 📥 Excel file download
- 🧹 Automatic data cleaning and formatting

## Login Credentials

- **Username:** EZDash
- **Password:** EZDash@2026

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
streamlit run app.py
```

3. Open your browser to `http://localhost:8501`

## Deployment

### Streamlit Cloud (Free)

1. Push this code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Deploy!

### Other Options

- **Heroku:** Add `setup.sh` and `Procfile`
- **Railway:** Direct deployment from GitHub
- **Render:** Connect GitHub repository

## How It Works

The application processes CSV files by:

1. Removing empty lines and separator lines
2. Combining multiline records (starting with 1D, 2C, etc.)
3. Splitting data using pipe (|) delimiters
4. Adding descriptive column headers
5. Exporting to Excel with date suffix

## File Structure

```
├── app.py              # Main Streamlit application
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── convertcsv.py      # Original Python script (reference)
```
>>>>>>> cf1438e (Initial commit: EZ Statement Converter Streamlit app)
