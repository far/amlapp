from typing import Literal

from pydantic import BaseModel, Field


class CheckAddressRequest(BaseModel):
    address: str = Field(max_length=64)
    currency: Literal['BTC', 'ETH', 'USDT']


class CheckAddressResponse(BaseModel):
    status: str
    risk_score: float | None = None
    risk_level: str | None = None
    categories: list[str] | None = None
    pdf_url: str | None = None
