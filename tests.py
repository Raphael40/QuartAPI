import pytest
import pytest_asyncio
from quart import Quart

from app import app

@pytest_asyncio.fixture(name="test_app",scope="function")
async def _test_app() -> Quart:
    async with app.test_app() as test_app:
        yield test_app

@pytest.mark.asyncio
async def test_create_card(test_app: Quart) -> None:
    test_client = test_app.test_client()
    response = await test_client.post(
        "/cards/",
        json={"question": "test question", "answer": "test answer"},
    )
    assert response.status_code == 200
    data = await response.get_json()
    assert "id" in data
    assert data["question"] == "test question"
    assert data["answer"] == "test answer"

@pytest.mark.asyncio
async def test_create_card_bad_data(test_app: Quart) -> None:
    test_client = test_app.test_client()
    response = await test_client.post(
        "/cards/",
        json={"quesion": "test question", "anser": "test answer"},
    )
    assert response.status_code == 400
