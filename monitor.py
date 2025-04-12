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

44|     def _get_process_list(self) -> List[Dict]:
45|         """Get sorted process list by CPU usage"""
46|         processes = []
47|         for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent', 'status']):
48|             try:
49|                 processes.append({
50|                     'pid': proc.info['pid'],
51|                     'name': proc.info['name'] or 'Unknown',
52|                     'cpu': proc.info['cpu_percent'],
53|                     'memory': proc.info['memory_percent'],
54|                     'status': proc.info['status']
55|                 })
56|             except (psutil.NoSuchProcess, psutil.AccessDenied):
57|                 continue
58|         return sorted(processes, key=lambda x: x['cpu'], reverse=True)

60|     def _update_historical_data(self):
61|         """Maintain historical data"""
62|         if not self._cached_metrics:
63|             return
64|         
65|         self._historical_data['cpu'].append(self._cached_metrics['cpu'])
66|         self._historical_data['memory'].append(self._cached_metrics['memory'])
67|         self._historical_data['timestamp'].append(time.time())
68|         
69|         # Keep last 300 samples
70|         for key in self._historical_data:
71|             if len(self._historical_data[key]) > 300:
72|                 self._historical_data[key].pop(0)

74|     def get_metrics(self) -> Dict:
75|         """Get current metrics with cache control"""
76|         if (time.time() - self._last_update) > self.refresh_rate:
77|             self.refresh()
78|             self._last_update = time.time()
79|         return self._cached_metrics


81|     def get_historical_data(self, metric: str = 'cpu', window: int = 60) -> Tuple[List[float], List[float]]:
82|         """Get time-series data for visualization"""
83|         if metric not in self._historical_data:
84|             return [], []
85|         
86|         cutoff = time.time() - window
87|         filtered = [
88|             (t, v) for t, v in zip(
89|                 self._historical_data['timestamp'],
90|                 self._historical_data[metric]
91|             ) if t >= cutoff
92|         ]
93|         return zip(*filtered) if filtered else ([], [])
