import streamlit as st
from datetime import datetime
import time
import pandas as pd
import plotly.express as px
from monitor import get_cpu_usage, get_memory_usage, get_top_processes, monitor
from optimizer import throttle_process, release_process, optimizer, ThrottleMethod, ProtectionLevel

st.set_page_config(
    page_title="Resource Optimizer",
    page_icon="🖥️",
    layout="wide"
)

st.markdown("""
<style>
    .metric-card {
        background: #2a2a2a;
        border-radius: 8px;
        padding: 15px;
        margin-bottom: 15px;
    }
    .stProgress > div > div > div {
        background-color: #4a8cff;
    }
</style>
""", unsafe_allow_html=True)

class Dashboard:
    def __init__(self):
        self.refresh_rate = 2
        self.last_update = 0
        self._init_session_state()
        
    def _init_session_state(self):
        if 'auto_throttle' not in st.session_state:
            st.session_state.auto_throttle = False
        if 'throttle_history' not in st.session_state:
            st.session_state.throttle_history = []
    
    def _update_metrics(self):
        monitor.refresh()
        self.last_update = time.time()
    
    def _render_header(self):
        col1, col2, col3 = st.columns([3, 2, 2])
        with col1:
            st.title("🖥️ Resource Optimizer")
        with col2:
            st.session_state.auto_throttle = st.toggle("Auto-Throttle")
        with col3:
            if st.button("Force Refresh"):
                self._update_metrics()
                st.rerun()
    