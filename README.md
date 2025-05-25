# 📄 ATS Resume Expert

An AI-powered tool to optimize resumes for Applicant Tracking Systems (ATS) using NLP and Gemini AI.

[![Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://ats-resume-checker-dfhz.onrender.com/)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)

 ## 📂 Project Structure

```bash
resume-analyzer/
├── app.py                # Main Streamlit application
├── Sample_Resume.pdf     # Example resume for testing
├── requirements.txt      # Python dependencies
├── .env                  # Environment variables
├── assets/               # Static files
│   ├── css/              # Custom stylesheets
│
└── src/                  # Core backend logic
    ├── __init__.py       # Package initialization
    ├── config.py         # Constants & API keys
    ├── analysis.py       # NLP processing and scoring
    ├── utils.py          # Helper functions
    └── visualization.py  # Data visualization
```

## ✨ Features

- 🔍 **ATS Compatibility Score** - Checks resume against job descriptions
- 📊 **Keyword Analysis** - Highlights missing skills and keywords
- ✍️ **AI Suggestions** - Powered by Google Gemini for resume improvements
- 📈 **Visual Reports** - Interactive charts and PDF exports

## 🛠️ Tech Stack

- **Frontend**: Streamlit
- **Backend**: Python
- **NLP**: NLTK, spaCy
- **AI**: Gemini API
- **Visualization**: Matplotlib, Seaborn

## 🚀 Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/resume-analyzer.git
