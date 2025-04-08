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
