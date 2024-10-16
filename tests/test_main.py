import pytest
from httpx import AsyncClient
# from unittest.mock import patch
from src.main import app
# from pydantic import BaseModel


# class VolatilityData(BaseModel):
#     symbol: str
#     volatility: float
#     timestamp: str


# @pytest.fixture
# def sample_data():
#     return VolatilityData(
#         symbol="AAPL", volatility=0.25, timestamp="2023-10-01T12:00:00Z"
#     ).dict()


# @pytest.mark.asyncio
# async def test_read_root():
#     async with AsyncClient(app=app, base_url="http://test") as ac:
#         response = await ac.get("/")
#     assert response.status_code == 200
#     assert response.json() == {"Hello": "World"}


# @pytest.mark.asyncio
# async def test_write_data_success(sample_data):
#     async with AsyncClient(app=app, base_url="http://test") as client:
#         with patch("db.write_api.write") as mock_write:
#             response = await client.post("/write/volatility/", json=sample_data)
#             assert response.status_code == 200
#             assert response.json() == {
#                 "message": "Volatility data written successfully."
#             }
#             mock_write.assert_called_once()
