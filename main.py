from fastapi import FastAPI
from psutil import virtual_memory, disk_usage, cpu_percent, net_io_counters, boot_time
import datetime 
inicio = datetime.datetime.fromtimestamp(boot_time())


app = FastAPI()

@app.get("/status")
def status():
    memory = virtual_memory()
    disk = disk_usage("/")
    cpu = cpu_percent()
    return {
        "status": "online",
        "memory": {
            "total": memory.total,
            "available": memory.available,
            "percent": memory.percent
        },
        "disk": {
            "total": disk.total,
            "used": disk.used,
            "free": disk.free,
            "percent": disk.percent
        },
        "cpu": {
            "percent": cpu
        },
        "uptime": datetime.datetime.now() - inicio
    }