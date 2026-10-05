import html

import numpy as np
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from fpdf import FPDF

# ============================================================
# PAGE SETUP
# ============================================================
st.set_page_config(page_title="Student Result Analyzer", page_icon="🎓", layout="wide")

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700&display=swap');

/* ---------- Page ---------- */
.stApp {
  background: linear-gradient(135deg, #0f0c29 0%, #302b63 50%, #24243e 100%);
  background-attachment: fixed;
}
h1, h2, h3, h4, p, label, [data-testid="stMarkdownContainer"] {
  font-family: 'Poppins', sans-serif;
}
#MainMenu, footer { visibility: hidden; }
[data-testid="stHeader"] { background: transparent; }
.block-container { padding-top: 2rem; max-width: 1200px; }

/* ---------- Sidebar ---------- */
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #1b1740, #0f0c29);
  border-right: 1px solid rgba(255, 255, 255, 0.08);
}

/* ---------- Hero ---------- */
.stApp .hero {
  text-align: center;
  padding: 40px 20px;
  margin-bottom: 26px;
  border-radius: 26px;
  background: linear-gradient(120deg, #667eea, #764ba2, #f093fb, #4facfe);
  background-size: 300% 300%;
  animation: gradientShift 10s ease infinite;
  box-shadow: 0 20px 50px rgba(118, 75, 162, 0.5);
}
.stApp .hero h1 {
  margin: 0;
  padding: 0;
  font-size: 40px;
  font-weight: 700;
  color: #ffffff;
  text-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
}
.stApp .hero p {
  margin: 8px 0 0;
  font-size: 16px;
  color: #ffffff;
  opacity: 0.95;
}
.hero .badge {
  display: inline-block;
  margin-top: 16px;
  padding: 6px 20px;
  font-size: 13px;
  color: #ffffff;
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.35);
  border-radius: 50px;
}

/* ---------- Summary cards ---------- */
.stat-card {
  position: relative;
  overflow: hidden;
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px 22px;
  border-radius: 22px;
  color: #ffffff;
  box-shadow: 0 12px 28px rgba(0, 0, 0, 0.35);
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  animation: popIn 0.6s ease backwards;
}
.stat-card::before {
  content: "";
  position: absolute;
  top: -40%;
  right: -20%;
  width: 70%;
  height: 180%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.35), transparent 70%);
  pointer-events: none;
}
.stat-card:hover {
  transform: translateY(-6px) scale(1.02);
  box-shadow: 0 20px 38px rgba(0, 0, 0, 0.45);
}
.stat-icon {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  width: 54px;
  height: 54px;
  font-size: 26px;
  background: rgba(255, 255, 255, 0.25);
  border: 1px solid rgba(255, 255, 255, 0.4);
  border-radius: 50%;
}
.stat-label {
  font-size: 12px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  opacity: 0.95;
}
.stat-value {
  font-size: 26px;
  font-weight: 700;
  line-height: 1.15;
  text-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}
.g-blue { background: linear-gradient(135deg, #2193b0, #6dd5ed); }
.g-purple { background: linear-gradient(135deg, #667eea, #764ba2); }
.g-green { background: linear-gradient(135deg, #11998e, #38ef7d); }
.g-orange { background: linear-gradient(135deg, #f7971e, #ffd200); }

/* ---------- Section titles ---------- */
.section-title {
  margin: 26px 0 14px;
  font-size: 22px;
  font-weight: 700;
  color: #ffffff;
}
.section-title::after {
  content: "";
  display: block;
  width: 54px;
  height: 4px;
  margin-top: 8px;
  background: linear-gradient(90deg, #667eea, #f093fb);
  border-radius: 10px;
}

/* ---------- Tabs ---------- */
.stTabs [data-baseweb="tab-list"] {
  gap: 10px;
  padding: 8px;
  background: rgba(255, 255, 255, 0.06);
  border-radius: 50px;
}
.stTabs [data-baseweb="tab"] {
  height: 46px;
  padding: 0 24px;
  font-weight: 600;
  color: #c5cae9;
  background: transparent;
  border-radius: 50px;
}
.stTabs [aria-selected="true"] {
  color: #ffffff !important;
  background: linear-gradient(135deg, #667eea, #764ba2) !important;
  box-shadow: 0 6px 18px rgba(118, 75, 162, 0.55);
}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] {
  display: none;
}

/* ---------- Buttons ---------- */
.stDownloadButton > button, .stButton > button {
  padding: 12px 28px;
  font-weight: 600;
  color: #ffffff !important;
  background: linear-gradient(135deg, #667eea, #764ba2, #f093fb);
  background-size: 200% 200%;
  border: none;
  border-radius: 14px;
  box-shadow: 0 8px 20px rgba(118, 75, 162, 0.5);
  transition: transform 0.25s ease, box-shadow 0.25s ease, background-position 0.4s ease;
}
.stDownloadButton > button:hover, .stButton > button:hover {
  transform: translateY(-3px);
  background-position: 100% 0;
  box-shadow: 0 14px 28px rgba(118, 75, 162, 0.6);
  border: none;
}

/* ---------- Tables, alerts, images ---------- */
[data-testid="stDataFrame"] {
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 16px;
  overflow: hidden;
}
[data-testid="stAlert"] { border-radius: 16px; }
[data-testid="stImage"] img {
  padding: 12px;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255, 255, 255, 0.1);
  border-radius: 20px;
}

/* ---------- Topper podium ---------- */
.podium {
  padding: 28px 16px;
  text-align: center;
  border-radius: 24px;
  box-shadow: 0 14px 32px rgba(0, 0, 0, 0.4);
  transition: transform 0.3s ease;
  animation: fadeUp 0.7s ease backwards;
}
.podium:hover { transform: translateY(-8px); }
.podium.small { margin-top: 30px; }
.podium .medal { font-size: 50px; }
.podium .pname { margin-top: 6px; font-size: 20px; font-weight: 700; }
.podium .ppct { margin-top: 2px; font-size: 32px; font-weight: 700; }
.podium .pmeta { margin-top: 4px; font-size: 13px; font-weight: 500; opacity: 0.85; }
.podium.gold { color: #3b2a00; background: linear-gradient(135deg, #f7b733, #ffe259); }
.podium.silver { color: #2c3e50; background: linear-gradient(135deg, #bdc3c7, #eef1f5); }
.podium.bronze { color: #3a1f00; background: linear-gradient(135deg, #cd7f32, #f0b27a); }

/* ---------- Report card ---------- */
.rc {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: space-between;
  gap: 22px;
  padding: 28px 32px;
  margin-bottom: 18px;
  background: rgba(255, 255, 255, 0.07);
  border: 1px solid rgba(255, 255, 255, 0.15);
  border-radius: 24px;
  box-shadow: 0 14px 34px rgba(0, 0, 0, 0.35);
}
.rc-name { font-size: 28px; font-weight: 700; color: #ffffff; }
.rc-sub { margin-top: 2px; font-size: 14px; color: #c5cae9; }
.rc-status {
  display: inline-block;
  margin-top: 12px;
  padding: 5px 18px;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 1px;
  border-radius: 50px;
}
.rc-status.pass { color: #38ef7d; background: rgba(56, 239, 125, 0.15); border: 1px solid #38ef7d; }
.rc-status.fail { color: #ff6b6b; background: rgba(255, 107, 107, 0.15); border: 1px solid #ff6b6b; }
.rc-remark { margin-top: 10px; font-size: 14px; font-style: italic; color: #e8eaf6; }
.rc-nums { display: flex; gap: 14px; }
.num-box {
  padding: 12px 20px;
  text-align: center;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 16px;
}
.num-box b { display: block; font-size: 22px; color: #ffffff; }
.num-box span {
  font-size: 11px;
  letter-spacing: 1px;
  text-transform: uppercase;
  color: #c5cae9;
}
.grade-circle {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 108px;
  height: 108px;
  font-size: 42px;
  font-weight: 700;
  color: #ffffff;
  border: 4px solid rgba(255, 255, 255, 0.45);
  border-radius: 50%;
  box-shadow: 0 0 30px rgba(255, 255, 255, 0.2);
}
.sub-card {
  padding: 18px 26px;
  margin-bottom: 18px;
  background: rgba(255, 255, 255, 0.06);
  border: 1px solid rgba(255, 255, 255, 0.12);
  border-radius: 20px;
}
.sub-row {
  display: flex;
  align-items: center;
  gap: 14px;
  margin: 14px 0;
  font-size: 14px;
  color: #ffffff;
}
.sub-name { width: 110px; font-weight: 600; }
.bar {
  flex: 1;
  height: 14px;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.12);
  border-radius: 20px;
}
.fill { height: 100%; border-radius: 20px; }
.fill.ok { background: linear-gradient(90deg, #11998e, #38ef7d); }
.fill.bad { background: linear-gradient(90deg, #cb2d3e, #ff6a5f); }
.sub-marks { width: 80px; font-weight: 600; text-align: right; }

/* ---------- Footer ---------- */
.app-footer {
  margin-top: 40px;
  text-align: center;
  font-size: 13px;
  color: #c5cae9;
  opacity: 0.8;
}

/* ---------- Animations ---------- */
@keyframes gradientShift {
  0% { background-position: 0% 50%; }
  50% { background-position: 100% 50%; }
  100% { background-position: 0% 50%; }
}
@keyframes popIn {
  from { opacity: 0; transform: scale(0.85) translateY(16px); }
  to { opacity: 1; transform: scale(1) translateY(0); }
}
@keyframes fadeUp {
  from { opacity: 0; transform: translateY(24px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)


def md(markup):
    st.markdown(markup, unsafe_allow_html=True)


md(
    '<div class="hero"><h1>🎓 Student Result Analyzer</h1>'
    "<p>Enter marks and get grades, rankings, graphs and report cards instantly</p>"
    '<span class="badge">✨ Fast • Accurate • Teacher Friendly</span></div>'
)

# ============================================================
# MATPLOTLIB DARK STYLE
# ============================================================
plt.rcParams.update(
    {
        "figure.facecolor": "none",
        "axes.facecolor": "none",
        "savefig.facecolor": "none",
        "savefig.transparent": True,
        "text.color": "#f5f3ff",
        "axes.labelcolor": "#e8eaf6",
        "axes.titlecolor": "#ffffff",
        "xtick.color": "#c5cae9",
        "ytick.color": "#c5cae9",
        "font.size": 10,
    }
)

PALETTE = ["#667eea", "#11998e", "#f7971e", "#ff6b9d", "#2193b0", "#a78bfa", "#38ef7d", "#ffd200"]


def style_ax(ax):
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    for side in ("left", "bottom"):
        ax.spines[side].set_color("#5c6bc0")
    ax.grid(axis="y", alpha=0.2, color="#9fa8da")
    ax.set_axisbelow(True)


# ============================================================
# CONSTANTS AND HELPERS
# ============================================================
GRADE_ORDER = ["A+", "A", "B", "C", "D", "F"]

GRADE_COLORS = {
    "A+": "#11998e",
    "A": "#38ef7d",
    "B": "#667eea",
    "C": "#f7971e",
    "D": "#ff6b9d",
    "F": "#e53935",
}

GRADE_TEXT = {
    "A+": "#ffffff",
    "A": "#0b3d2e",
    "B": "#ffffff",
    "C": "#3b2a00",
    "D": "#ffffff",
    "F": "#ffffff",
}

REMARKS = {
    "A+": "Outstanding performance!",
    "A": "Excellent work!",
    "B": "Good work. Keep it up!",
    "C": "Satisfactory. Can do better with more effort.",
    "D": "Needs improvement. Please work harder.",
    "F": "Needs extra attention and hard work.",
}


def get_grade(percentage):
    if percentage >= 90:
        return "A+"
    elif percentage >= 80:
        return "A"
    elif percentage >= 70:
        return "B"
    elif percentage >= 60:
        return "C"
    elif percentage >= 50:
        return "D"
    else:
        return "F"


def safe(text):
    # The PDF font only supports basic Latin characters
    return str(text).encode("latin-1", "replace").decode("latin-1")


def sample_data():
    return pd.DataFrame(
        {
            "Roll No": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            "Name": [
                "Ali Khan", "Sara Ahmed", "Hamza Malik", "Ayesha Noor", "Usman Raza",
                "Fatima Zahra", "Bilal Hussain", "Maryam Iqbal", "Hassan Ali", "Zainab Shah",
            ],
            "Math": [85, 92, 45, 70, 30, 78, 66, 95, 58, 81],
            "English": [78, 88, 52, 65, 40, 82, 59, 91, 62, 75],
            "Urdu": [90, 85, 60, 72, 35, 88, 70, 89, 55, 79],
            "Science": [88, 91, 48, 68, 28, 76, 64, 94, 60, 83],
            "Computer": [95, 89, 55, 80, 45, 90, 72, 97, 67, 86],
        }
    )


def analyze(raw, total_marks, pass_marks):
    df = raw.copy()

    # Remove rows without a name
    df = df[df["Name"].notna()]
    df = df[df["Name"].astype(str).str.strip() != ""]
    df = df.reset_index(drop=True)

    df["Roll No"] = df["Roll No"].fillna("").astype(str).str.replace(r"\.0$", "", regex=True)

    # Every column except Roll No and Name is a subject
    subjects = [c for c in df.columns if c not in ("Roll No", "Name")]
    for s in subjects:
        df[s] = pd.to_numeric(df[s], errors="coerce").fillna(0)

    if df.empty or not subjects:
        return df, subjects

    df["Total"] = df[subjects].sum(axis=1)
    max_total = total_marks * len(subjects)
    df["Percentage"] = (df["Total"] / max_total * 100).round(2)
    df["Grade"] = df["Percentage"].apply(get_grade)
    df["Status"] = df[subjects].apply(
        lambda row: "Pass" if (row >= pass_marks).all() else "Fail", axis=1
    )
    df["Failed In"] = df[subjects].apply(
        lambda row: ", ".join([s for s in subjects if row[s] < pass_marks]) or "-", axis=1
    )
    df["Rank"] = df["Total"].rank(ascending=False, method="min").astype(int)
    return df, subjects


def stat_card(icon, label, value, style):
    return (
        f'<div class="stat-card {style}"><div class="stat-icon">{icon}</div>'
        f'<div><div class="stat-label">{label}</div>'
        f'<div class="stat-value">{value}</div></div></div>'
    )


def podium_card(pos, row):
    cls = ["gold", "silver", "bronze"][pos]
    medal = ["🥇", "🥈", "🥉"][pos]
    extra = "" if pos == 0 else " small"
    return (
        f'<div class="podium {cls}{extra}"><div class="medal">{medal}</div>'
        f'<div class="pname">{html.escape(str(row["Name"]))}</div>'
        f'<div class="ppct">{row["Percentage"]}%</div>'
        f'<div class="pmeta">Grade {row["Grade"]} • Rank {row["Rank"]} • Total {row["Total"]:g}</div></div>'
    )


def style_table(frame):
    def grade_style(value):
        bg = GRADE_COLORS.get(value, "#444444")
        fg = GRADE_TEXT.get(value, "#ffffff")
        return f"background-color: {bg}; color: {fg}; font-weight: 700; text-align: center"

    def status_style(value):
        if value == "Pass":
            return "color: #38ef7d; font-weight: 700"
        return "color: #ff6b6b; font-weight: 700"

    return frame.style.map(grade_style, subset=["Grade"]).map(status_style, subset=["Status"])


def make_report_card(student, subjects, total_marks, pass_marks, school_name):
    pdf = FPDF()
    pdf.add_page()

    # Colored header band
    pdf.set_fill_color(102, 126, 234)
    pdf.rect(0, 0, 210, 40, "F")
    pdf.set_y(9)
    pdf.set_font("Helvetica", "B", 22)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(0, 12, safe(school_name), align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Helvetica", "", 13)
    pdf.cell(0, 9, "Student Report Card", align="C", new_x="LMARGIN", new_y="NEXT")
    pdf.set_y(50)

    # Student info
    pdf.set_text_color(0, 0, 0)
    pdf.set_font("Helvetica", "B", 12)
    pdf.cell(95, 9, f"Name: {safe(student['Name'])}")
    pdf.cell(95, 9, f"Roll No: {safe(student['Roll No'])}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(4)

    # Table header
    pdf.set_fill_color(102, 126, 234)
    pdf.set_text_color(255, 255, 255)
    pdf.cell(70, 10, "Subject", border=1, align="C", fill=True)
    pdf.cell(40, 10, "Marks Obtained", border=1, align="C", fill=True)
    pdf.cell(40, 10, "Total Marks", border=1, align="C", fill=True)
    pdf.cell(40, 10, "Result", border=1, align="C", fill=True, new_x="LMARGIN", new_y="NEXT")

    # Table rows
    pdf.set_font("Helvetica", "", 12)
    for s in subjects:
        marks = student[s]
        passed = marks >= pass_marks
        pdf.set_text_color(0, 0, 0)
        pdf.cell(70, 9, safe(s), border=1)
        pdf.cell(40, 9, f"{marks:g}", border=1, align="C")
        pdf.cell(40, 9, f"{total_marks}", border=1, align="C")
        if passed:
            pdf.set_text_color(17, 153, 142)
        else:
            pdf.set_text_color(229, 57, 53)
        pdf.cell(40, 9, "Pass" if passed else "Fail", border=1, align="C",
                 new_x="LMARGIN", new_y="NEXT")

    # Summary
    pdf.set_text_color(0, 0, 0)
    pdf.ln(6)
    pdf.set_font("Helvetica", "B", 13)
    pdf.cell(95, 10, f"Total: {student['Total']:g} / {total_marks * len(subjects)}")
    pdf.cell(95, 10, f"Percentage: {student['Percentage']}%", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(95, 10, f"Grade: {student['Grade']}")
    pdf.cell(95, 10, f"Rank in class: {student['Rank']}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 10, f"Final Result: {student['Status']}", new_x="LMARGIN", new_y="NEXT")
    pdf.ln(2)
    pdf.set_font("Helvetica", "I", 12)
    pdf.multi_cell(0, 8, f"Remarks: {REMARKS[student['Grade']]}", new_x="LMARGIN", new_y="NEXT")

    # Signatures
    pdf.ln(22)
    pdf.set_font("Helvetica", "", 12)
    pdf.cell(95, 8, "____________________")
    pdf.cell(95, 8, "____________________", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(95, 8, "Class Teacher")
    pdf.cell(95, 8, "Principal", new_x="LMARGIN", new_y="NEXT")

    return bytes(pdf.output())


# ============================================================
# SIDEBAR (SETTINGS)
# ============================================================
st.sidebar.header("⚙️ Settings")
school_name = st.sidebar.text_input("School name", "THE INSPIRATION MODEL SCHOOL CAMPUS VIII")
total_marks = st.sidebar.number_input("Total marks per subject", min_value=1, value=100)
pass_marks = st.sidebar.number_input("Pass marks per subject", min_value=0, value=33)
source = st.sidebar.radio("Data source", ["Sample data", "Upload CSV", "Enter manually"])

# ============================================================
# LOAD DATA
# ============================================================
if source == "Sample data":
    raw = sample_data()

elif source == "Upload CSV":
    uploaded = st.file_uploader("Upload your marks CSV file", type="csv")
    if uploaded is None:
        st.info("Upload a CSV with columns: Roll No, Name, and one column for each subject.")
        st.stop()
    raw = pd.read_csv(uploaded)

else:
    md('<div class="section-title">✍️ Enter marks</div>')
    st.caption("Click a cell to edit it. Use the empty last row to add more students.")
    template = pd.DataFrame(
        {
            "Roll No": [1, 2, 3, 4, 5],
            "Name": ["", "", "", "", ""],
            "Math": [0, 0, 0, 0, 0],
            "English": [0, 0, 0, 0, 0],
            "Urdu": [0, 0, 0, 0, 0],
            "Science": [0, 0, 0, 0, 0],
            "Computer": [0, 0, 0, 0, 0],
        }
    )
    raw = st.data_editor(template, num_rows="dynamic", key="editor")

if "Roll No" not in raw.columns or "Name" not in raw.columns:
    st.error("The data must have 'Roll No' and 'Name' columns.")
    st.stop()

df, subjects = analyze(raw, total_marks, pass_marks)

if df.empty or not subjects:
    st.warning("Please add at least one student with a name and marks.")
    st.stop()

# ============================================================
# SUMMARY CARDS
# ============================================================
c1, c2, c3, c4 = st.columns(4)
c1.markdown(stat_card("👥", "Students", len(df), "g-blue"), unsafe_allow_html=True)
c2.markdown(stat_card("📈", "Class Average", f"{df['Percentage'].mean():.1f}%", "g-purple"),
            unsafe_allow_html=True)
c3.markdown(stat_card("✅", "Pass Rate", f"{(df['Status'] == 'Pass').mean() * 100:.0f}%", "g-green"),
            unsafe_allow_html=True)
c4.markdown(stat_card("🏆", "Highest", f"{df['Percentage'].max():.1f}%", "g-orange"),
            unsafe_allow_html=True)

md("<br>")

# ============================================================
# TABS
# ============================================================
tab1, tab2, tab3, tab4 = st.tabs(["📋 Results", "🏆 Toppers", "📊 Graphs", "📄 Report Card"])

# ---------- Tab 1: Results ----------
with tab1:
    md('<div class="section-title">Class Result</div>')
    ranked = df.sort_values("Rank")
    st.dataframe(
        style_table(ranked),
        hide_index=True,
        column_config={
            "Percentage": st.column_config.ProgressColumn(
                "Percentage", min_value=0, max_value=100, format="%.1f%%"
            )
        },
    )
    st.download_button(
        "⬇️ Download Result (CSV)",
        ranked.to_csv(index=False).encode("utf-8"),
        "class_result.csv",
        "text/csv",
    )

    md('<div class="section-title">⚠️ Students who need attention</div>')
    failed = df[df["Status"] == "Fail"]
    if failed.empty:
        st.success("No failed students. Great job!")
    else:
        st.dataframe(failed[["Roll No", "Name", "Total", "Percentage", "Failed In"]], hide_index=True)

# ---------- Tab 2: Toppers ----------
with tab2:
    md('<div class="section-title">Top 3 Students</div>')
    top3 = df.sort_values("Rank").head(3)
    order = [1, 0, 2] if len(top3) == 3 else list(range(len(top3)))
    cols = st.columns(len(top3))
    for col, pos in zip(cols, order):
        col.markdown(podium_card(pos, top3.iloc[pos]), unsafe_allow_html=True)

    md('<div class="section-title">Subject-wise Toppers</div>')
    topper_rows = []
    for s in subjects:
        best = df.loc[df[s].idxmax()]
        topper_rows.append({"Subject": s, "Topper": best["Name"], "Marks": best[s]})
    st.dataframe(pd.DataFrame(topper_rows), hide_index=True)

# ---------- Tab 3: Graphs ----------
with tab3:
    col1, col2 = st.columns(2)

    with col1:
        fig, ax = plt.subplots(figsize=(6, 4))
        averages = df[subjects].mean()
        bars = ax.bar(
            subjects, averages, color=[PALETTE[i % len(PALETTE)] for i in range(len(subjects))]
        )
        ax.bar_label(bars, fmt="%.1f", color="white", padding=3, fontsize=9)
        ax.set_ylim(0, total_marks)
        ax.set_title("Subject-wise Class Average", fontsize=13, fontweight="bold", pad=12)
        ax.set_ylabel("Average Marks")
        plt.setp(ax.get_xticklabels(), rotation=30, ha="right")
        style_ax(ax)
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)

    with col2:
        counts = df["Grade"].value_counts().reindex(GRADE_ORDER).dropna()
        fig, ax = plt.subplots(figsize=(6, 4))
        ax.pie(
            counts,
            labels=counts.index,
            autopct="%1.0f%%",
            startangle=90,
            pctdistance=0.78,
            colors=[GRADE_COLORS[g] for g in counts.index],
            wedgeprops={"width": 0.45, "edgecolor": "#1b1740", "linewidth": 2},
            textprops={"color": "white", "fontsize": 10},
        )
        ax.set_title("Grade Distribution", fontsize=13, fontweight="bold", pad=12)
        st.pyplot(fig)
        plt.close(fig)

    ordered = df.sort_values("Percentage", ascending=False)
    fig, ax = plt.subplots(figsize=(10, 4.2))
    ax.bar(
        ordered["Name"],
        ordered["Percentage"],
        color=[GRADE_COLORS[g] for g in ordered["Grade"]],
    )
    ax.set_ylim(0, 105)
    ax.set_ylabel("Percentage")
    ax.set_title("Percentage of Every Student (colored by grade)", fontsize=13,
                 fontweight="bold", pad=12)
    plt.setp(ax.get_xticklabels(), rotation=40, ha="right")
    present = [g for g in GRADE_ORDER if g in set(df["Grade"])]
    ax.legend(
        handles=[Patch(color=GRADE_COLORS[g], label=g) for g in present],
        frameon=False,
        labelcolor="white",
        ncol=len(present),
        loc="upper right",
    )
    style_ax(ax)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

# ---------- Tab 4: Report Card ----------
with tab4:
    md('<div class="section-title">Individual Report Card</div>')
    idx = st.selectbox(
        "Select student",
        df.index,
        format_func=lambda i: f"{df.loc[i, 'Roll No']} - {df.loc[i, 'Name']}",
    )
    student = df.loc[idx]

    grade = student["Grade"]
    passed = student["Status"] == "Pass"
    status_cls = "pass" if passed else "fail"
    status_text = "✅ PASSED" if passed else "❌ FAILED"

    rows = ""
    for s in subjects:
        m = float(student[s])
        pct = max(0, min(100, m / total_marks * 100))
        cls = "ok" if m >= pass_marks else "bad"
        rows += (
            f'<div class="sub-row"><span class="sub-name">{html.escape(str(s))}</span>'
            f'<div class="bar"><div class="fill {cls}" style="width:{pct:.0f}%"></div></div>'
            f'<span class="sub-marks">{m:g}/{total_marks}</span></div>'
        )

    md(
        '<div class="rc"><div>'
        f'<div class="rc-name">{html.escape(str(student["Name"]))}</div>'
        f'<div class="rc-sub">Roll No: {html.escape(str(student["Roll No"]))} • Rank {student["Rank"]} in class</div>'
        f'<span class="rc-status {status_cls}">{status_text}</span>'
        f'<div class="rc-remark">{REMARKS[grade]}</div></div>'
        '<div class="rc-nums">'
        f'<div class="num-box"><b>{student["Total"]:g}</b><span>Total</span></div>'
        f'<div class="num-box"><b>{student["Percentage"]}%</b><span>Percentage</span></div></div>'
        f'<div class="grade-circle" style="background:{GRADE_COLORS[grade]};'
        f'color:{GRADE_TEXT[grade]}">{grade}</div></div>'
    )
    md(f'<div class="sub-card">{rows}</div>')

    if not passed:
        st.error(f"Needs improvement in: {student['Failed In']}")

    x = np.arange(len(subjects))
    width = 0.38
    fig, ax = plt.subplots(figsize=(9, 4))
    student_bars = ax.bar(
        x - width / 2, [student[s] for s in subjects], width, color="#667eea", label=student["Name"]
    )
    ax.bar(
        x + width / 2, [df[s].mean() for s in subjects], width, color="#f7971e", label="Class average"
    )
    ax.bar_label(student_bars, fmt="%g", color="white", padding=3, fontsize=9)
    ax.set_xticks(x)
    ax.set_xticklabels(subjects)
    ax.set_ylim(0, total_marks + 8)
    ax.set_title("Student vs Class Average", fontsize=13, fontweight="bold", pad=12)
    ax.legend(frameon=False, labelcolor="white")
    style_ax(ax)
    fig.tight_layout()
    st.pyplot(fig)
    plt.close(fig)

    st.download_button(
        "⬇️ Download Report Card (PDF)",
        make_report_card(student, subjects, total_marks, pass_marks, school_name),
        f"{safe(student['Name']).replace(' ', '_')}_report_card.pdf",
        "application/pdf",
    )

md('<div class="app-footer">Made with ❤️ for teachers • Student Result Analyzer</div>')
