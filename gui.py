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
    
    def _render_system_metrics(self):
        cpu = get_cpu_usage()
        mem = get_memory_usage()
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.markdown(f"""
            <div class="metric-card">
                <h3>CPU Usage</h3>
                <h1>{cpu:.1f}%</h1>
            </div>
            """, unsafe_allow_html=True)
            st.progress(cpu / 100)
            
        with col2:
            st.markdown(f"""
            <div class="metric-card">
                <h3>Memory Usage</h3>
                <h1>{mem:.1f}%</h1>
            </div>
            """, unsafe_allow_html=True)
            st.progress(mem / 100)
            
        with col3:
            optimizer.protection_level = st.selectbox(
                "Protection Level",
                options=[level.name for level in ProtectionLevel],
                index=0
            )
    
    def _render_process_table(self):
        processes = get_top_processes(10)
        
        st.markdown("### Process Management")
        for proc in processes:
            col1, col2, col3, col4, col5, col6 = st.columns([1, 3, 2, 2, 1, 1])
            with col1:
                st.text(proc['pid'])
            with col2:
                st.text(proc['name'])
            with col3:
                # Clamp CPU value between 0 and 100 before dividing
                cpu_value = min(max(proc['cpu'], 0), 100) / 100
                st.progress(cpu_value, text=f"{proc['cpu']:.1f}%")
            with col4:
                # Clamp memory value between 0 and 100 before dividing
                mem_value = min(max(proc['memory'], 0), 100) / 100
                st.progress(mem_value, text=f"{proc['memory']:.1f}%")
            with col5:
                if st.button("⏸️", key=f"throttle_{proc['pid']}"):
                    throttle_process(proc['pid'])
                    st.session_state.throttle_history.append(
                        (datetime.now(), "THROTTLE", proc['pid'], proc['name'])
                    )
                    st.rerun()
            with col6:
                if st.button("▶️", key=f"release_{proc['pid']}"):
                    release_process(proc['pid'])
                    st.session_state.throttle_history.append(
                        (datetime.now(), "RELEASE", proc['pid'], proc['name'])
                    )
                    st.rerun()