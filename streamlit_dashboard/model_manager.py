import streamlit as st
import utils
import pandas as pd

def render():
    st.title("\U0001F916 Model Management")
    st.markdown("Upload, view, and set active ML models.")

    # --- Upload Model ---
    with st.form("upload_model_form"):
        uploaded_file = st.file_uploader("Upload Model (.pkl, .h5)", type=["pkl", "h5"])
        submit = st.form_submit_button("Upload")
        if submit and uploaded_file:
            utils.save_model_file(uploaded_file)
            st.success("Model uploaded successfully.")
            st.experimental_rerun()

    # --- List Models ---
    st.markdown("### Uploaded Models")
    models = utils.list_models()
    if models:
        df = pd.DataFrame([{
            "Name": m["name"],
            "Upload Date": m["upload_date"],
            "Active": (m["name"] == utils.get_active_model())
        } for m in models])
        st.dataframe(df, use_container_width=True)

        for m in models:
            col1, col2 = st.columns([3,1])
            col1.markdown(f"**{m['name']}** (Uploaded: {m['upload_date']})")
            if m["name"] == utils.get_active_model():
                col2.success("Active")
            else:
                if col2.button("Set Active", key=f"set_active_{m['name']}"):
                    utils.set_active_model(m["name"])
                    st.success(f"{m['name']} set as active model.")
                    st.experimental_rerun()
    else:
        st.info("No models uploaded yet.") 