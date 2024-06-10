import pandas as pd
import streamlit as st
import plotly.figure_factory as ff
import plotly.express as px
import numpy as np
import time
from streamlit import runtime
from streamlit_dynamic_filters import DynamicFilters


# Replace 'raw_csv_url' with the URL of the raw CSV file on GitHub

# Use st.set_page_config to configure the layout
st.set_page_config(
    layout="wide",  # Set the layout to "wide"
    page_title="Portal de inversiones autos",  # Set the title of the app
)

st.text("hola")