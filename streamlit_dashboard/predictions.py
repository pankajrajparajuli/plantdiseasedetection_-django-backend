import streamlit as st
import pandas as pd
import utils

def render_predictions():
    st.title("\U0001F489 Predictions Management")
    st.markdown("View, filter, and export predictions.")

    search = st.text_input("Search by ID")
    user = st.text_input("Filter by Username")
    disease = st.text_input("Filter by Disease")
    date = st.date_input("Filter by Date", value=None)

    preds_qs = utils.get_predictions(search=search, user=user, disease=disease, date=date if date else None)
    preds_list = []
    for p in preds_qs:
        preds_list.append({
            "ID": p.id,
            "User First Name": p.user.first_name,
            "User Last Name": p.user.last_name,
            "Username": p.user.username,
            "Disease": p.disease,
            "Confidence": p.confidence,
            "Timestamp": p.timestamp,
        })
    df = pd.DataFrame(preds_list)
    st.dataframe(df, use_container_width=True)

    st.download_button("Export as CSV", df.to_csv(index=False), "predictions.csv")

    st.markdown("### Prediction Details")
    for idx, row in df.iterrows():
        with st.expander(f"Prediction ID: {row['ID']}"):
            st.json(row.to_dict())

def render_history():
    st.title("\U0001F4DC History Management")
    st.markdown("View, filter, and export history.")

    search = st.text_input("Search by ID")
    user = st.text_input("Filter by Username")
    disease = st.text_input("Filter by Disease")
    date = st.date_input("Filter by Date", value=None)

    hist_qs = utils.get_history(search=search, user=user, disease=disease, date=date if date else None)
    hist_list = []
    for h in hist_qs:
        hist_list.append({
            "ID": h.id,
            "User First Name": h.user.first_name,
            "User Last Name": h.user.last_name,
            "Username": h.user.username,
            "Disease": h.disease,
            "Confidence": h.confidence,
            "Remedy": h.remedy,
            "Timestamp": h.timestamp,
        })
    df = pd.DataFrame(hist_list)
    st.dataframe(df, use_container_width=True)

    st.download_button("Export as CSV", df.to_csv(index=False), "history.csv")

    st.markdown("### History Details")
    for idx, row in df.iterrows():
        with st.expander(f"History ID: {row['ID']}"):
            st.json(row.to_dict()) 