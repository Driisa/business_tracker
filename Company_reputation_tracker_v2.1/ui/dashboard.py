import streamlit as st
from database.db_utils import get_db_session
from database.schema import Company, Mention
import pandas as pd

def main():
    st.title("Company Reputation Tracker Dashboard")
    session = get_db_session()
    companies = session.query(Company).all()

    if not companies:
        st.write("No companies found.")
        return

    company_names = [c.name for c in companies]
    selected_company_name = st.selectbox("Select a company", company_names)
    selected_company = next(c for c in companies if c.name == selected_company_name)

    mentions = session.query(Mention).filter(Mention.company_id == selected_company.id).all()
    sentiment_filter = st.selectbox("Filter by sentiment", ("All", "POSITIVE", "NEGATIVE", "NEUTRAL"))
    if sentiment_filter != "All":
        mentions = [m for m in mentions if m.sentiment == sentiment_filter]

    data = [{
        "Title": m.title,
        "Sentiment": m.sentiment,
        "Published": m.published_at,
        "Source": m.source,
        "URL": m.url,
    } for m in mentions]

    st.dataframe(pd.DataFrame(data))

    sentiments = [m.sentiment for m in mentions]
    sentiment_counts = pd.Series(sentiments).value_counts()
    st.bar_chart(sentiment_counts)

    session.close()

if __name__ == "__main__":
    main()
