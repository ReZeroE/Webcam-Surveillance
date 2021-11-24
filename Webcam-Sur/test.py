import os
import psutil

fan = psutil.disk_usage(path=os.path.dirname(os.path.abspath(__file__)))
print(fan.percent)