import numpy as np
import pandas as pd
import streamlit as st

from processor.model.predictor import Predictor


st.set_page_config(
    page_title="Predictive Valve Guardian",
    layout="wide"
)

st.title("Predictive Valve Guardian")

col1, col2 = st.columns(2)

with col1:
    ps2_file = st.file_uploader(
        "Upload PS2 signal", type=["txt", "csv", "tsv"])

with col2:
    fs1_file = st.file_uploader(
        "Upload FS1 signal", type=["txt", "csv", "tsv"])


def load_array(file) -> np.ndarray:
    return np.loadtxt(file)


if ps2_file and fs1_file:
    ps2 = load_array(ps2_file)
    fs1 = load_array(fs1_file)

    if ps2.shape[0] != fs1.shape[0]:
        st.error("PS2 and FS1 must have the same number of cycles")
        st.stop()

    st.subheader("Data preview")

    c1, c2 = st.columns(2)
    with c1:
        st.write(f"PS2 shape: {ps2.shape}")
        st.dataframe(pd.DataFrame(ps2[:5]))

    with c2:
        st.write(f"FS1 shape: {fs1.shape}")
        st.dataframe(pd.DataFrame(fs1[:5]))

    if st.button("Predict"):
        predictor = Predictor()
        predictions = predictor.predict(ps2, fs1)

        results = pd.DataFrame({
            "cycle": np.arange(len(predictions)),
            "valve_optimal": predictions
        })

        st.subheader("Predictions")
        st.dataframe(results, height=400)

        selected_cycle = st.selectbox(
            "Select cycle to inspect",
            results["cycle"].tolist()
        )

        st.subheader(f"Cycle {selected_cycle} signals")

        c1, c2 = st.columns(2)

        with c1:
            st.write("PS2")
            st.line_chart(ps2[selected_cycle])

        with c2:
            st.write("FS1")
            st.line_chart(fs1[selected_cycle])
