from typing import Optional, Tuple

import numpy as np
import streamlit as st

from dashboard.constants import FS1_KEY, LAYOUT, PAGE_TITLE, PS2_KEY
from dashboard.data import load_data
from dashboard.sidebar import render_sidebar
from dashboard.state import get_predictions, init_session_state, set_predictions
from dashboard.visualization import display_predictions, plot_cycle
from processor.model.predictor import Predictor

st.set_page_config(page_title=PAGE_TITLE, layout=LAYOUT)


def process_data(ps2_file, fs1_file):
    """Load and validate data from uploaded files."""
    try:
        ps2 = load_data(ps2_file)
        fs1 = load_data(fs1_file)
    except Exception as e:
        st.error(f"Error loading data: {e}")
        st.stop()

    if ps2.shape[0] != fs1.shape[0]:
        st.error(
            f"PS2 and FS1 must have the same number of cycles. PS2: {ps2.shape[0]}, FS1: {fs1.shape[0]}"
        )
        st.stop()

    st.sidebar.success(f"Loaded {ps2.shape[0]} cycles.")
    return ps2, fs1


def handle_predictions(ps2, fs1):
    """Handle the prediction logic and button."""
    col_pred, _ = st.columns([1, 4])
    with col_pred:
        if st.button("Run Predictions", type="primary"):
            with st.spinner("Running predictions..."):
                try:
                    predictor = Predictor()
                    preds = predictor.predict(ps2, fs1)
                    set_predictions(preds)
                    st.success("Done!")
                except Exception as e:
                    st.error(f"Prediction failed: {e}")


def main():
    st.title(PAGE_TITLE)
    init_session_state()

    ps2_file, fs1_file = render_sidebar()

    if not (ps2_file and fs1_file):
        st.info("Please upload both PS2 and FS1 signal files to begin.")
        return

    ps2, fs1 = process_data(ps2_file, fs1_file)

    # Cycle Selection
    st.subheader("Cycle Inspection")
    max_cycle = ps2.shape[0] - 1
    selected_cycle = st.number_input(
        "Select cycle to inspect", min_value=0, max_value=max_cycle, value=0, step=1
    )

    predictions = get_predictions()

    current_cycle_prediction: Optional[bool] = None
    if predictions is not None:
        current_cycle_prediction = predictions[selected_cycle]
    current_ps2 = ps2[selected_cycle]
    current_fs1 = fs1[selected_cycle]

    handle_predictions(ps2, fs1)
    plot_cycle(current_ps2, current_fs1, selected_cycle, current_cycle_prediction)
    display_predictions(predictions)


if __name__ == "__main__":
    main()
