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
