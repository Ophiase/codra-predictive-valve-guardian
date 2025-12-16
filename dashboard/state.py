import streamlit as st

from dashboard.constants import PREDICTIONS_KEY


def init_session_state():
    """Initialize session state variables."""
    if PREDICTIONS_KEY not in st.session_state:
        st.session_state[PREDICTIONS_KEY] = None


def clear_predictions():
    """Clear predictions from session state."""
    if PREDICTIONS_KEY in st.session_state:
        del st.session_state[PREDICTIONS_KEY]


def get_predictions():
    """Get predictions from session state."""
    return st.session_state.get(PREDICTIONS_KEY)


def set_predictions(predictions):
    """Set predictions in session state."""
    st.session_state[PREDICTIONS_KEY] = predictions
