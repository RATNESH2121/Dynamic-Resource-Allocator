 1| import psutil
 2| import time
 3| from typing import List, Dict, Tuple
 4| import logging
 5| 
 6| logging.basicConfig(
 7|     level=logging.INFO,
 8|     format='%(asctime)s - %(levelname)s - %(message)s',
 9|     filename='monitor.log'
10| )

12| class SystemMonitor:
13|     def __init__(self, refresh_rate: float = 1.0):
14|         self.refresh_rate = refresh_rate
15|         self._last_update = 0
16|         self._cached_metrics = {}
17|         self._historical_data = {
18|             'cpu': [],
19|             'memory': [],
20|             'timestamp': []
21|         }

23|     def refresh(self):
24|         """Update all metrics"""
25|         self._update_system_metrics()
26|         self._update_historical_data()
