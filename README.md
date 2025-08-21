# Freelance Project Proposal Generator

A Python-based tool that helps freelancers and agencies quickly generate professional project proposals. The app collects client/project details through a **Streamlit interface**, fills them into a **styled HTML template**, and exports a **polished PDF proposal** ready to send.

---

## 🚀 Features
- 📋 Collects project details via an easy-to-use Streamlit form  
- 🎨 Auto-fills data into a styled HTML/CSS template  
- 🖨️ Exports proposals as professional PDFs  
- 🔁 Reusable for multiple clients/projects  
- ⚡ Saves time and improves professionalism  

---

## 🛠️ Tech Stack
- **Python 3.10+**
- [Streamlit](https://streamlit.io/) – Interactive UI  
- [Jinja2](https://jinja.palletsprojects.com/) – Templating engine  
- [xhtml2pdf](https://github.com/xhtml2pdf/xhtml2pdf) – PDF generation  

---

## 📦 Installation

Clone the repo:

```bash
git clone https://github.com/your-username/freelance-proposal-generator.git
cd freelance-proposal-generator
```

Create a virtual environment and install dependencies: 
```
python -m venv .venv
source .venv/bin/activate   # macOS/Linux
.venv\Scripts\activate      # Windows

pip install -r requirements.txt
```

---
## ▶️ Usage
Run the Streamlit app: 
``` streamlit run app.py ```
1. Enter client details, project scope, and pricing info in the form
2. Preview your proposal in real-time
3. Download the final PDF and send it to your client 🎉

---
## 📂 Project Structure
```
freelance-proposal-generator/
│── app.py                      # Main Streamlit app
│── templates/
│   └── proposal_template.html  # HTML template with Jinja2 placeholders
│── assets/
│   ├── logo.png
│   └── signature.png
│── requirements.txt
│── README.md
```

---

