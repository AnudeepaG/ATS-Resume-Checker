import os
import sys
from pathlib import Path
import streamlit as st
from streamlit_lottie import st_lottie

# Local imports
sys.path.insert(0, str(Path(__file__).parent))
from src.config import *
from src.utils import *
from src.analysis import *
from src.visualization import *

def main():
    st.set_page_config(page_title="ATS Resume Expert", layout="wide", page_icon="📄")

    # CSS
    base_dir = Path(__file__).parent
    css_main = load_css(str(base_dir / "assets" / "css" / "main.css"))
    css_dark = load_css(str(base_dir / "assets" / "css" / "dark.css"))
    st.markdown(css_main, unsafe_allow_html=True)
    if st.sidebar.checkbox("🌙 Dark Mode"):
        st.markdown(css_dark, unsafe_allow_html=True)

    # Header
    col1, col2 = st.columns([2, 10])
    with col1:
        lottie_url_anim = load_lottieurl(LOTTIE_URL)
        if lottie_url_anim:
            st_lottie(lottie_url_anim, height=100, key="url_anim")
        else:
            st.warning("⚠️ Animation failed to load.")
    with col2:
        st.markdown("""
            <div style="text-align: center;">
                <h1 style="font-size: 35px; color: #4B9CD3;">🚀 ATS Resume Expert</h1>
                <p style="font-size: 15px; color: #666;">Optimize your resume to beat ATS filters</p>
            </div>
        """, unsafe_allow_html=True)

    # Sidebar
    st.sidebar.subheader("📋 Sample Job Description")
    st.sidebar.code(SAMPLE_JD, language="markdown")

    resume_path = Path(__file__).parent / "Sample_Resume.pdf"
    if resume_path.exists():
        with open(resume_path, "rb") as f:
            st.sidebar.download_button(
                "📥 Download Sample Resume",
                data=f,
                file_name="Sample_Resume.pdf",
                mime="application/pdf"
            )

    if st.sidebar.button("🔄 Use Sample Job Description"):
        st.session_state['job_desc'] = SAMPLE_JD

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
                    st.markdown(f"### {label}\n\n{result}")
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

if __name__ == "__main__":
    main()

