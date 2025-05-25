# Analysis functions
import re
import pandas as pd
from difflib import SequenceMatcher
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from collections import Counter
from src.config import SKILLS

def calculate_similarity(resume_text, job_text):
    resume_clean = re.sub(r'\s+', ' ', resume_text.strip().lower())
    job_clean = re.sub(r'\s+', ' ', job_text.strip().lower())
    return round(SequenceMatcher(None, resume_clean, job_clean).ratio() * 100, 2)

def skill_matching(resume_text, job_text):
    resume_clean = re.sub(r'\s+', ' ', resume_text.strip().lower())
    job_clean = re.sub(r'\s+', ' ', job_text.strip().lower())
    overall_match_score = calculate_similarity(resume_text, job_text)
    
    data = []
    for skill in SKILLS:
        s_lower = skill.lower()
        in_resume = s_lower in resume_clean
        in_job = s_lower in job_clean
        match_score = overall_match_score if in_resume and in_job else 0
        data.append({
            'Skill': skill,
            'In Resume': in_resume,
            'In Job Description': in_job,
            'Match %': match_score
        })
    
    return pd.DataFrame(data)

def keyword_density(resume_text, job_text, top_n=15):
    stop_words = set(stopwords.words('english'))
    lemmatizer = WordNetLemmatizer()
    
    job_keywords = [
        lemmatizer.lemmatize(w) 
        for w in re.findall(r'\w+', job_text.lower()) 
        if w not in stop_words
    ]
    
    resume_words = [
        lemmatizer.lemmatize(w) 
        for w in re.findall(r'\w+', resume_text.lower()) 
        if w not in stop_words
    ]
    
    job_count = Counter(job_keywords)
    resume_count = Counter(resume_words)

    density = []
    for word, freq in job_count.items():
        r_freq = resume_count.get(word, 0)
        match = (r_freq / freq) * 100 if freq else 0
        emoji = "✅" if match >= 75 else "🟡" if match >= 40 else "❌"
        density.append({
            'keyword': word,
            'job_count': freq,
            'resume_count': r_freq,
            'match_percentage': round(match, 2),
            'emoji': emoji
        })
    
    return sorted(density, key=lambda x: -x['match_percentage'])[:top_n]