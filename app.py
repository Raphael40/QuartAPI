from dataclasses import dataclass

from quart import abort, g, Quart
from quart_db import QuartDB
from quart_schema import QuartSchema, validate_request, validate_response

app = Quart(__name__)
QuartDB(app, url="sqlite:///database.db")
QuartSchema(app)

@dataclass
class CardInput:
    question: str
    answer: str

@dataclass
class Card(CardInput):
    id: int

@app.post("/cards/")
@validate_request(CardInput)
@validate_response(Card)
async def create_card(data: CardInput) -> Card:
    """Create a new Anki Card"""
    result = await g.connection.fetch_one(
        """INSERT INTO cards (question, answer)
                VALUES (:question, :answer)
            RETURNING id, question, answer""",
            {"question": data.question, "answer": data.answer},
    )
    return Card(**result)

@dataclass
class Cards:
    cards: list[Card]

@app.get("/cards/")
@validate_response(Cards)
async def get_cards() -> Cards:
    """Show all Anki Cards"""
    query = """SELECT id, question, answer
                FROM cards"""
    cards = [
        Card(**row)
        async for row in g.connection.iterate(query)
    ]
    return Cards(cards=cards)

@app.put("/cards/<int:id>/")
@validate_request(CardInput)
@validate_response(Card)
async def update_card(id: int, data: CardInput) -> Card:
    result = await g.connection.fetch_one(
        """UPDATE cards
            SET question = :question, answer = :answer
            WHERE id = :id
        RETURNING id, question, answer""",
            {"id": id, "question": data.question, "answer": data.answer},
    )
    if result is None:
        abort(404)
    return Card(**result)

@app.delete("/cards/<int:id>/")
async def delete_card(id: int) -> str:
    await g.connection.execute(
        "DELETE FROM cards WHERE id = :id",
        {"id": id}
    )
    return ""