# --- dashboard/app.py (Streamlit Interface) ---

import streamlit as st
import pandas as pd
from sqlalchemy.orm import Session
from db.models import Mention, Review, Summary, Company
from db.session import SessionLocal

st.set_page_config(page_title="📊 Company Reputation Tracker", layout="wide")

company_name = st.sidebar.text_input("Company Name", value="Acme Corp")

st.title(f"📈 Reputation Dashboard — {company_name}")

session: Session = SessionLocal()
company = session.query(Company).filter(Company.name == company_name).first()

if not company:
    st.warning("Company not found in database.")
else:
    mentions = session.query(Mention).filter(Mention.company_id == company.id).all()
    reviews = session.query(Review).filter(Review.company_id == company.id).all()
    summaries = session.query(Summary).filter(Summary.company_id == company.id).all()

    st.subheader("📰 Mentions")
    st.dataframe(pd.DataFrame([m.__dict__ for m in mentions]))

    st.subheader("⭐ Reviews")
    st.dataframe(pd.DataFrame([r.__dict__ for r in reviews]))

    st.subheader("🧠 Weekly Summaries")
    for summary in summaries:
        st.markdown(f"**{summary.timeframe}** — {summary.summary}")