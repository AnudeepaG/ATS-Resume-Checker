import os
import sys
from pathlib import Path
import streamlit as st
from streamlit_lottie import st_lottie 

# Add src directory to Python path
sys.path.insert(0, str(Path(__file__).parent))

# Now import from src
from src.config import *
from src.utils import *
from src.analysis import *
from src.visualization import *

# Define the PDF path
RESUME_PATH = Path(__file__).parent / "Sample_Resume.pdf"

# --- Fix 1: Add safe CSS loader (prevents crash if file missing) ---
def load_css(file_path):
    try:
        with open(file_path, "r") as f:
            return f"<style>{f.read()}</style>"
    except FileNotFoundError:
        st.warning(f"⚠️ CSS file not found: {file_path}")
        return ""

# --- Fix 2: Initialize Streamlit session early (prevents SessionInfo error) ---
if "job_desc" not in st.session_state:
    st.session_state["job_desc"] = ""

# Page setup
st.set_page_config(page_title="ATS Resume Expert", layout="wide", page_icon="📄")

# Load CSS
BASE_DIR = Path(__file__).parent
CSS_MAIN = load_css(str(BASE_DIR / "assets" / "css" / "main.css"))
CSS_DARK = load_css(str(BASE_DIR / "assets" / "css" / "dark.css"))

# Apply styles
st.markdown(CSS_MAIN, unsafe_allow_html=True)
if st.sidebar.checkbox("🌙 Dark Mode"):
    st.markdown(CSS_DARK, unsafe_allow_html=True)

# --- Load Lottie ---
lottie_url_anim = load_lottieurl(LOTTIE_URL)

# --- Inline Layout: Lottie + Heading ---
col1, col2 = st.columns([2, 10])

with col1:
    if lottie_url_anim:
        st_lottie(lottie_url_anim, height=100, key="url_anim")
    else:
        st.warning("⚠️ Animation failed to load.")

with col2:
    st.markdown("""
        <div style="display: flex; align-items: center; height: 100%;">
            <div style="text-align: center; top: 0; left: 0; width: 100%; background: white; z-index: 1000; padding: 0 0;">
                <h1 style="font-size: 35px; color: #4B9CD3;">🚀 ATS Resume Expert</h1>
                <p style="font-size: 15px; color: #666;">Optimize your resume to beat Applicant Tracking Systems (ATS)</p>
            </div>
        </div>
        <div style="height: 20px;"></div>
    """, unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.subheader("📋 Sample Job Description")
st.sidebar.code(SAMPLE_JD, language="markdown")

try:
    with open(RESUME_PATH, "rb") as f:
        st.sidebar.download_button(
            label="📥 Download Sample Resume",
            data=f,
            file_name="Sample_Resume.pdf",
            mime="application/pdf"
        )
except FileNotFoundError:
    st.sidebar.error(f"File not found at: {RESUME_PATH}")
    st.sidebar.write("Current directory contents:", os.listdir(Path(__file__).parent))

if st.sidebar.button("🔄 Use Sample Job Description"):
    st.session_state['job_desc'] = SAMPLE_JD

st.sidebar.image(
    SIDEBAR_IMAGE,
    caption="Optimize your resume for success!",
)
st.sidebar.markdown("<div class='sidebar-title'>🌟 Bonus Features</div>", unsafe_allow_html=True)
st.sidebar.markdown("<div class='sidebar-section'>🚀 **Boost Your Resume**<br>• 🔍 ATS Matching<br>• 💡 Skill Insights<br>• 📈 Keyword Breakdown</div>", unsafe_allow_html=True)

# --- Main Inputs ---
job_desc = st.text_area("📝 Paste Job Description:", height=150, value=st.session_state.get('job_desc', ''))
uploaded_file = st.file_uploader("📂 Upload Resume (PDF Only)", type=["pdf"])

if uploaded_file and job_desc:
    resume_text = input_pdf_text(uploaded_file)

    prompts = {
        "📄 Detailed Analysis": "You are a seasoned HR. Analyze resume, give strengths & improvements.",
        "🔍 Missing Keywords": "You're an ATS expert. Identify missing keywords from resume vs JD.",
        "📊 Match Score": "You're a recruiter. Compare resume vs job description and give a score.",
        "✍️ Rewrite Suggestions": "You are an expert resume writer. Suggest rewritten version of resume."
    }

    st.subheader("🧠 AI Tools")
    for label, prompt in prompts.items():
        if st.button(label):
            with st.spinner(f"Analyzing: {label}"):
                result = get_gemini_response(prompt, resume_text, job_desc)
                st.markdown(f"*{label}*\n\n{result}")
                pdf_buffer = export_pdf(result)
                st.download_button(
                    "📤 Export as PDF",
                    pdf_buffer,
                    file_name="output_analysis.pdf",
                    mime="application/pdf"
                )

    st.divider()
    st.subheader("📊 Keyword Density")

    density = keyword_density(resume_text, job_desc)
    fig = plot_keyword_density_chart(density)
    st.pyplot(fig)

    st.markdown("### 🧾 Keyword Match Table")
    st.dataframe(
        [{
            "Keyword": d['keyword'],
            "Resume Count": d['resume_count'],
            "JD Count": d['job_count'],
            "Match %": d['match_percentage'],
            "Feedback": d['emoji']
        } for d in density]
    )
else:
    st.info("👆 Upload a resume and paste the job description to begin.")
