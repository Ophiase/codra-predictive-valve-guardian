import streamlit as st

from dashboard.constants import FS1_KEY, PS2_KEY
from dashboard.state import clear_predictions


def render_sidebar():
    """Render the sidebar for file uploads."""
    st.sidebar.header("Data Upload")
    ps2_file = st.sidebar.file_uploader(
        "Upload PS2 signal",
        type=["txt", "csv", "tsv"],
        key=PS2_KEY,
        on_change=clear_predictions,
    )
    fs1_file = st.sidebar.file_uploader(
        "Upload FS1 signal",
        type=["txt", "csv", "tsv"],
        key=FS1_KEY,
        on_change=clear_predictions,
    )
    return ps2_file, fs1_file
