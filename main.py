from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from psutil import virtual_memory, disk_usage, cpu_percent, boot_time
import datetime

from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware

inicio = datetime.datetime.fromtimestamp(boot_time())

app = FastAPI()


def get_client_ip(request: Request):
    return (
        request.headers.get("CF-Connecting-IP")
        or request.headers.get("X-Forwarded-For", "").split(",")[0].strip()
        or request.client.host
    )


limiter = Limiter(key_func=get_client_ip)

app.state.limiter = limiter
app.add_exception_handler(
    RateLimitExceeded,
    _rate_limit_exceeded_handler
)
app.add_middleware(SlowAPIMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://server.kunibo.net",
    ],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


@app.get("/status")
@limiter.limit("35/minute")
def status(request: Request):
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