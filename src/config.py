# Configuration and constants
import os
from dotenv import load_dotenv
import nltk

# NLTK downloads
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('stopwords')

# Load environment variables
load_dotenv()

# Sample data
SAMPLE_RESUME = """
Experienced Python Developer with knowledge of REST APIs, Django, and machine learning.
Worked on data analysis and visualization using pandas, matplotlib.
Internship experience includes building web applications and automating scripts.
"""

SAMPLE_JOB_DESCRIPTION = """
We are looking for a software engineer experienced in Python, REST APIs, and Django.
Knowledge of data science libraries such as pandas and matplotlib is a plus.
The role involves developing web applications and scripting automation tasks.
"""

SKILLS = ['Python', 'REST APIs', 'Django', 'Flask', 'Machine Learning', 'Data Analysis',
          'pandas', 'matplotlib', 'scikit-learn', 'Web Development', 'Automation']

SAMPLE_JD = """
We are looking for a Software Engineer Intern with experience in React.js, Node.js, MongoDB, and REST APIs.
The ideal candidate should be comfortable with Git, Agile practices, and building scalable web applications.
Bonus if you have exposure to Docker or cloud services like AWS.
"""

LOTTIE_URL = "https://assets3.lottiefiles.com/packages/lf20_jcikwtux.json"
SIDEBAR_IMAGE = "https://u-static.haozhaopian.net/uid_1f26e52fc45044fbb67feeacc48a1565/aiImage/8e99f9e2b50243dc99a10a0dbccf59a2.jpg"