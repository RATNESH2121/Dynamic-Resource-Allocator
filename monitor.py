 | import psutil
  import time
 from typing import List, Dict, Tuple
  import logging
| 
  logging.basicConfig(
     level=logging.INFO,
     format='%(asctime)s - %(levelname)s - %(message)s',
     filename='monitor.log'
| )

| class SystemMonitor:
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

28|     def _update_system_metrics(self):
29|         """Collect current system metrics"""
30|         try:
31|             self._cached_metrics = {
32|                 'cpu': psutil.cpu_percent(interval=0.5),
33|                 'memory': psutil.virtual_memory().percent,
34|                 'processes': self._get_process_list()
35|             }
36|         except Exception as e:
37|             logging.error(f"Monitoring failed: {e}")
38|             self._cached_metrics = {
39|                 'cpu': -1,
40|                 'memory': -1,
41|                 'processes': []
42|             }
