from pydantic import BaseModel


class CounterResponse(BaseModel):
    key: str
    count: int
