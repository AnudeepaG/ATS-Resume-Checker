# Visualization functions
import matplotlib.pyplot as plt
import seaborn as sns
from fpdf import FPDF
from pandas.plotting import table

def save_pdf_with_table(dataframe, filename):
    fig, ax = plt.subplots(figsize=(10, len(dataframe) * 0.5 + 1))
    ax.axis('off')
    tbl = table(ax, dataframe, loc='center', cellLoc='center', colWidths=[0.2]*len(dataframe.columns))
    tbl.auto_set_font_size(False)
    tbl.set_fontsize(10)
    plt.title("Resume vs Job Description Match", fontsize=14)
    plt.savefig("table_plot.png", bbox_inches='tight')
    plt.close()

    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Resume vs Job Description Match Report", ln=True, align='C')
    pdf.image("table_plot.png", x=10, y=30, w=190)
    pdf.output(filename)

def plot_keyword_density_chart(density_data):
    sorted_data = sorted(density_data, key=lambda x: x['match_percentage'], reverse=True)
    top_15 = sorted_data[:15]
    keywords = [d['keyword'] for d in top_15]
    percentages = [d['match_percentage'] for d in top_15]
    emojis = [d['emoji'] for d in top_15]

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x=percentages, y=keywords, palette='viridis', ax=ax)
    ax.set_title('Keyword Match Percentage (Top 15)', fontsize=16)
    ax.set_xlabel('Match Percentage (%)')
    ax.set_ylabel('Keyword')
    
    for i, (pct, emoji) in enumerate(zip(percentages, emojis)):
        ax.text(pct + 1, i, f"{emoji} {pct}%", va='center', fontsize=10)

    return fig