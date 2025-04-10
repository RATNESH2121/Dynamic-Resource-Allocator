import psutil
import time
from typing import List, Dict, Tuple
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='monitor.log'
)

class SystemMonitor:
    def __init__(self, refresh_rate: float = 1.0):
        self.refresh_rate = refresh_rate
        self._last_update = 0
        self._cached_metrics = {}
        self._historical_data = {
            'cpu': [],
            'memory': [],
            'timestamp': []
        }
