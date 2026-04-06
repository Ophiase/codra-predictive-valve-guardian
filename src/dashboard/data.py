import numpy as np
import streamlit as st


@st.cache_data
def load_data(file) -> np.ndarray:
    """Load data from uploaded file."""
    return np.loadtxt(file)
