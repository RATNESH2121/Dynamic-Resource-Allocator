import os
import psutil
import subprocess
from enum import Enum, auto
from typing import Dict
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    filename='optimizer.log'
)

class ThrottleMethod(Enum):
    NICE = auto()   
    CGROUPS = auto()
    PAUSE = auto()

    class ProtectionLevel(Enum):
    SAFE = auto()
    AGGRESSIVE = auto()
    EMERGENCY = auto()



class ResourceOptimizer:
    def __init__(self):
        self.active_limits: Dict[int, ThrottleMethod] = {}
        self.protection_level = ProtectionLevel.SAFE

    def throttle_process(self, pid: int, method: ThrottleMethod = ThrottleMethod.NICE) -> bool:
        try:
            proc = psutil.Process(pid)
            proc_name = proc.name()
            
            if method == ThrottleMethod.NICE:
                os.system(f"renice +10 {pid}")
                self.active_limits[pid] = method
                logging.info(f"Set nice+10 on {proc_name} (PID:{pid})")
                return True