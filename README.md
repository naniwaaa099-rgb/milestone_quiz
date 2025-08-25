
# Milestone Quiz (Streamlit, 100 items)

This repository contains a polished Streamlit app and a 100‑item milestone question bank.

## Files
- `milestone_quiz_clean.py` — **MAIN FILE** (set this in Streamlit Cloud)
- `milestone_quiz_questions.json` — question bank
- `requirements.txt` — Python deps

## Run locally
```bash
pip install -r requirements.txt
python -m streamlit run milestone_quiz_clean.py
```

## Deploy on Streamlit Community Cloud
1) Create a **public** GitHub repo and upload these three files to the repo **root**.
2) In https://streamlit.io/cloud → **New app**:
   - Repository: `<your-username>/<your-repo>`
   - Branch: `main`
   - Main file path: `milestone_quiz_clean.py`  ⟵ make sure this matches exactly
3) Deploy and share the URL it gives you.

If you see a "You do not have access" page, sign out of Streamlit Cloud and sign back in with the **same GitHub** account that owns the repo, and ensure the repo is **Public**.
