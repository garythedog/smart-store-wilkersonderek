# Smart Store Analytics – Derek Wilkerson

**Smart Store Analytics** is a professional Python project created for the *Business Intelligence and Analytics* course at Northwest Missouri State University.
It demonstrates how to organize, document, and run analytics code using modern tools such as **uv**, **VS Code**, and **MkDocs**.

---

## 🧭 What This Project Does
- Provides a clean Python project layout under `src/analytics_project/`
- Includes demo modules for basics, stats, languages, and visualization
- Demonstrates how to manage dependencies and environments with `uv`
- Builds project documentation automatically with MkDocs and GitHub Pages

---

## ⚙️ How to Set Up

### Clone the repo
```powershell
git clone https://github.com/garythedog/smart-store-wilkersonderek.git
cd smart-store-wilkersonderek
---

## 🚀 Project Workflow – P2 (BI Python)

This section records the key commands and workflow used to complete Tasks 3 – 5.

### 🧰 Environment Setup (Windows 11 + PowerShell)
```powershell
# Activate local virtual environment
& .\.venv\Scripts\Activate.ps1

# Verify versions
python --version
uv --version
# Run the data preparation module
uv run python -m src.analytics_project.data_prep
