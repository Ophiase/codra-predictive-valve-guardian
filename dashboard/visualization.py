import numpy as np
import pandas as pd
import streamlit as st


def plot_cycle(
    ps2_cycle: np.ndarray,
    fs1_cycle: np.ndarray,
    cycle_idx: int,
    prediction: bool = None,
):
    """Plot PS2 and FS1 signals for a specific cycle."""
    st.markdown(f"### Cycle {cycle_idx}")

    if prediction is not None:
        status = "Optimal" if prediction else "Faulty"
        color = "green" if prediction else "red"
        st.markdown(f"**Prediction:** :{color}[{status}]")

    col1, col2 = st.columns(2)
    with col1:
        st.write("PS2 Signal (Pressure)")
        st.line_chart(ps2_cycle)
    with col2:
        st.write("FS1 Signal (Flow)")
        st.line_chart(fs1_cycle)


def display_predictions(predictions: np.ndarray) -> None:
    """Display all predictions in a table and provide download option."""
    if predictions is None:
        return

    with st.expander("View All Predictions"):
        results = pd.DataFrame(
            {
                "cycle": np.arange(len(predictions)),
                "valve_optimal": predictions,
            }
        )
        st.dataframe(results, use_container_width=True)

        csv = results.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download Predictions CSV",
            csv,
            "predictions.csv",
            "text/csv",
            key="download-csv",
        )
