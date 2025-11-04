# CRM-Lead-Processing

**AI-Powered Email Lead Analyzer** that automatically fetches, classifies, and tracks Gmail emails into **Lead, Support, Spam, Follow-up** categories. Built with **Flask**, **SocketIO**, and **Hugging Face AI** for real-time updates and beautiful dashboard.

[![GitHub stars](https://img.shields.io/github/stars/anuanshad7306/CRM-Lead-Processing.svg?style=social)](https://github.com/anuanshad7306/CRM-Lead-Processing/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/anuanshad7306/CRM-Lead-Processing.svg?style=social)](https://github.com/anuanshad7306/CRM-Lead-Processing/network/members)

---

## ✨ Features

| Feature | Description |
|-------|-------------|
| **AI Classification** | Zero-shot AI classifies emails instantly |
| **Real-Time Updates** | Dashboard refreshes every **2 minutes** |
| **Date Filtering** | View emails from **today, yesterday, or any date** |
| **Email Details** | Name, email, phone, company, content, attachments |
| **Responsive UI** | Beautiful **glass-morphism** design |
| **SQLite Database** | Stores leads for **history & analytics** |
| **SocketIO Live** | Instant updates without page refresh |

---

## 🛠 Tech Stack

```text
Backend: Python, Flask, SocketIO
AI: Hugging Face (DistilBERT)
Email: IMAP (Gmail)
Frontend: HTML, Tailwind CSS, JavaScript
Database: SQLite
Real-time: SocketIO

📁 Project Structure
textCRM-Lead-Processing/
│
├── dashboard.py/
│   ├── app.py                 # Main Flask app + AI + SocketIO
│   ├── templates/
│   │   └── dashboard.html     # Responsive UI
│   └── db/
│       └── crm.db             # SQLite database
├── src/
│   ├── __init__.py
│   ├── crm.py                 # Database functions
│   ├── email_fetcher.py
│   ├── email_parser.py
│   ├── lead_extractor.py
│   ├── show_results.py
│   └── utils.py
├── tests/
│   └── test_crm.py
├── data/
│   └── fetched_emails/
├── requirements.txt
├── .gitignore
└── README.md

🚀 Quick Start
1. Clone the Repository
bashgit clone https://github.com/anuanshad7306/CRM-Lead-Processing.git
cd CRM-Lead-Processing
2. Set Up Environment
bashpython -m venv .venv
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows
3. Install Dependencies
bashpip install -r requirements.txt
4. Configure Gmail

Enable 2FA on your Gmail account
Generate App Password: myaccount.google.com/apppasswords
Update app.py:

pythonEMAIL = "your-email@gmail.com"
PASSWORD = "your-app-password"  # 16-character app password
5. Run the App
bashpython dashboard.py/app.py
6. Open Dashboard
Go to: http://127.0.0.1:5000

📱 Dashboard Preview





















ViewScreenshotMain Dashboard<img src="screenshots/dashboard.png" alt="Dashboard">AI Classification<img src="screenshots/classification.png" alt="AI">Date Filter<img src="screenshots/filter.png" alt="Date Filter">
(Add screenshots to screenshots/ folder)

🎯 How It Works

Connect to Gmail → Fetch emails via IMAP
AI Analysis → Classify using DistilBERT model
Store Data → Save to SQLite database
Live Update → Push to dashboard via SocketIO
Filter & View → Toggle types, dates, real-time


🤖 AI Model Details

Model: typeform/distilbert-base-uncased-mnli
Type: Zero-shot classification (no training needed)
Accuracy: ~80% on real emails (manual testing)
Speed: 60% faster than BERT


📊 Database Schema













TableColumnsleadsname, email, phone, classification, date

🔧 Troubleshooting

























IssueSolutionNo emailsCheck Gmail App Password & IMAP enabledSlow loadingIncrease MAX_EMAILS or use Redis cacheSocketIO errorsCheck browser console (F12)Database errorEnsure db/ folder exists

🤝 Contributing

Fork the repo
Create branch: git checkout -b feature/new-filter
Commit: git commit -m "Add new filter"
Push: git push origin feature/new-filter
Open Pull Request


📄 License
This project is MIT Licensed — free to use, modify, and distribute.

👥 Authors

Muhammad Anshad
Vaseek Muhammed
