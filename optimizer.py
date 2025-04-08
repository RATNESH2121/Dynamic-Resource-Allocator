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
            
              elif method == ThrottleMethod.CGROUPS:
                cgroup_name = f"limit_{pid}"
                subprocess.run(['cgcreate', '-g', f'cpu:/{cgroup_name}'], check=True)
                subprocess.run(['cgset', '-r', 'cpu.cfs_quota_us=50000', cgroup_name], check=True)
                subprocess.run(['cgclassify', '-g', f'cpu:/{cgroup_name}', str(pid)], check=True)
                self.active_limits[pid] = method
                logging.info(f"Set CPU limit on {proc_name} via cgroups")
                return True
            
                 elif method == ThrottleMethod.PAUSE:
                proc.suspend()
                self.active_limits[pid] = method
                logging.warning(f"Paused {proc_name} (PID:{pid})")
                return True
                
        except Exception as e:
            logging.error(f"Failed to throttle PID {pid}: {e}")
            return False

    def release_process(self, pid: int) -> bool:
        if pid not in self.active_limits:
            return False
            
        try:
            method = self.active_limits[pid]
            proc = psutil.Process(pid)
            proc_name = proc.name()
            
            if method == ThrottleMethod.NICE:
                os.system(f"renice 0 {pid}")
                

                  elif method == ThrottleMethod.CGROUPS:
                cgroup_name = f"limit_{pid}"
                subprocess.run(['cgdelete', '-g', f'cpu:/{cgroup_name}'], check=True)
                
            elif method == ThrottleMethod.PAUSE:
                proc.resume()
                
            del self.active_limits[pid]
            logging.info(f"Released limits on {proc_name} (PID:{pid})")
            return True
            
        except Exception as e:
            logging.error(f"Failed to release PID {pid}: {e}")
            return False
