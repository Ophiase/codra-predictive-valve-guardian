import numpy as np
import pandas as pd
import streamlit as st

from processor.model.predictor import Predictor

st.set_page_config(page_title="Predictive Valve Guardian", layout="wide")


def clear_predictions():
    """Clear predictions from session state when new files are uploaded."""
    if "predictions" in st.session_state:
        del st.session_state["predictions"]


@st.cache_data
def load_data(file) -> np.ndarray:
    """Load data from uploaded file."""
    return np.loadtxt(file)


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


def main():
    st.title("Predictive Valve Guardian")

    # Initialize session state for predictions
    if "predictions" not in st.session_state:
        st.session_state.predictions = None

    # File Upload Section
    st.sidebar.header("Data Upload")
    ps2_file = st.sidebar.file_uploader(
        "Upload PS2 signal",
        type=["txt", "csv", "tsv"],
        key="ps2",
        on_change=clear_predictions,
    )
    fs1_file = st.sidebar.file_uploader(
        "Upload FS1 signal",
        type=["txt", "csv", "tsv"],
        key="fs1",
        on_change=clear_predictions,
    )

    if ps2_file and fs1_file:
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

        # Data Info
        st.sidebar.success(f"Loaded {ps2.shape[0]} cycles.")

        # Cycle Selection
        st.subheader("Cycle Inspection")
        max_cycle = ps2.shape[0] - 1
        selected_cycle = st.number_input(
            "Select cycle to inspect", min_value=0, max_value=max_cycle, value=0, step=1
        )

        # Prediction Logic
        col_pred, col_space = st.columns([1, 4])
        with col_pred:
            if st.button("Run Predictions", type="primary"):
                with st.spinner("Running predictions..."):
                    try:
                        predictor = Predictor()
                        # Predictor expects (n_samples, n_timesteps)
                        preds = predictor.predict(ps2, fs1)
                        st.session_state.predictions = preds
                        st.success("Done!")
                    except Exception as e:
                        st.error(f"Prediction failed: {e}")

        # Determine current prediction
        current_prediction = None
        if st.session_state.predictions is not None:
            if len(st.session_state.predictions) == len(ps2):
                current_prediction = st.session_state.predictions[selected_cycle]
            else:
                st.warning(
                    "Data changed since last prediction. Please run predictions again."
                )
                st.session_state.predictions = None

        # Plotting
        plot_cycle(
            ps2[selected_cycle], fs1[selected_cycle], selected_cycle, current_prediction
        )

        # Show all predictions if available
        if st.session_state.predictions is not None:
            with st.expander("View All Predictions"):
                results = pd.DataFrame(
                    {
                        "cycle": np.arange(len(st.session_state.predictions)),
                        "valve_optimal": st.session_state.predictions,
                    }
                )
                st.dataframe(results, use_container_width=True)

                # Download results
                csv = results.to_csv(index=False).encode("utf-8")
                st.download_button(
                    "Download Predictions CSV",
                    csv,
                    "predictions.csv",
                    "text/csv",
                    key="download-csv",
                )

    else:
        st.info("Please upload both PS2 and FS1 signal files to begin.")


if __name__ == "__main__":
    main()
