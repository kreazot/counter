import aioredis
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

from schemas.counter import CounterResponse

app = FastAPI()

# todo перенести в core + сделать конфиг
# todo redis вынести в DPI
redis = aioredis.from_url("redis://localhost", decode_responses=True)


@app.on_event("startup")
async def start_up():
    try:
        await redis.ping()
    except Exception as e:
        raise RuntimeError("Redis is not available") from e


# todo перенести в модуль api/v1
@app.get("/api/v1/healthcheck", response_class=PlainTextResponse)
async def healthcheck():
    return "Ok"


@app.get("/api/v1/counter/{key}", response_model=CounterResponse)
async def counter(key: str):
    """Получение счетчика."""
    count = await redis.get(key)
    return CounterResponse(key=key, count=int(count or 0))


@app.post("/api/v1/counter/{key}/increment")
async def counter(key: str):
    """Создание/увеличение счетчика."""
    count = await redis.incr(key)
    return CounterResponse(key=key, count=count)
