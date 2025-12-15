import numpy as np
import streamlit as st

from processor.model.predictor import Predictor

st.set_page_config(page_title="Valve Condition Predictor")

st.title("Predictive Valve Guardian")

ps2_file = st.file_uploader("Upload PS2 signal", type=["txt", "csv", "tsv"])
fs1_file = st.file_uploader("Upload FS1 signal", type=["txt", "csv", "tsv"])

if ps2_file and fs1_file:
    ps2: np.ndarray = np.loadtxt(ps2_file)
    fs1: np.ndarray = np.loadtxt(fs1_file)

    if st.button("Predict"):
        predictor = Predictor()
        pred = predictor.predict(ps2, fs1)

        if pred == 1:
            st.success("Valve condition is OPTIMAL (100%)")
        else:
            st.error("Valve condition is NOT optimal")
