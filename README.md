# Automate Finances with Python 💰📊

A personal finance dashboard built with Python and Streamlit.  
Upload your bank statement, categorize your expenses, visualize your spending habits — all in one clean interface.

---

## 🚀 Features

- 📁 Upload CSV bank statements (e.g. from CIBC)
- 🧹 Clean and parse transaction data
- 🏷️ Categorize expenses manually or automatically
- 💾 Categories saved and reused via `categories.json`
- 📊 Summary table of total spend per category
- 🥧 Interactive Pie Chart using Plotly
- ☁️ Streamlit Cloud ready

---

## 📷 Screenshot

![App Screenshot](https://user-images.githubusercontent.com/YOUR_ID/your-screenshot.png)

---

## 🛠️ Tech Stack

- [Streamlit](https://streamlit.io/) – Web app framework
- [Pandas](https://pandas.pydata.org/) – Data manipulation
- [Plotly](https://plotly.com/python/) – Charts

---
⚠️ Make sure your CSV file follows this format:
Date,Details,Debit,Credit,CardNumber

## 📦 Setup

```bash
git clone https://github.com/Mikehk11/automate-finances-with-python.git
cd automate-finances-with-python
pip install -r requirements.txt
streamlit run main.py

automate-finances-with-python/
├── main.py               # Streamlit app
├── requirements.txt      # Python dependencies
├── .gitignore            # Ignore venv, CSV, etc.
└── README.md             # Project overview

🧠 Why This Project?

This app was built as a personal tool to better understand monthly spending habits.
It’s also a great portfolio piece to demonstrate:
	•	Python skills
	•	Data wrangling
	•	Interactive UI with Streamlit
