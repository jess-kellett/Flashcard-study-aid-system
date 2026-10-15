from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Study API is running"}

cards = {
    1: {
        "id" : 1,
        "topic" : "Networks",
        "question" : "What does TCP stand for?",
        "answer" : "Transmission Control Protocol",
    },
    2: {
        "id" : 2,
        "topic" : "Python",
        "question" : "What does a decorator do?",
        "answer" : "Wraps a function to change or extend its behaviours",
    }
}

@app.get("/cards/{card_id}")
def get_cards(card_id:int):
    if card_id not in cards:
        raise HTTPException(status_code = 404, detail="Card not found")
    return cards[card_id]

class CardIn(BaseModel):
    topic: str
    question: str
    answer: str

@app.post("/cards", status_code=201)
def create_card(card: CardIn):
    new_id = max(cards, default=0) + 1
    cards[new_id] = {"id": new_id, **card.model_dump()}
    return cards[new_id]

@app.put("/cards/{card_id}")
def update_card(card_id: int, card: CardIn):
    if card_id not in cards:
        raise HTTPException(status_code=404, detail="Card not found")
    cards[card_id] = {"id": card_id, **card.model_dump()}
    return cards[card_id]

@app.delete("/cards/{card_id}", status_code=204)
def delete_card(card_id: int):
    if card_id not in cards:
        raise HTTPException(status_code=404, detail="Card not found")
    del cards[card_id]

@app.get("/cards")
def list_cards(topic: str | None = None):
    result = list(cards.values())
    if topic:
        result = [c for c in result if c["topic"] == topic]
    return result


class CardPatch(BaseModel):
    topic: str | None = None
    question: str | None = None
    answer: str | None = None

@app.patch("/cards/{card_id}")
def patch_card(card_id: int, card: CardPatch):
    if card_id not in cards:
        raise HTTPException(status_code=404, detail="Card not found")
    cards[card_id].update(card.model_dump(exclude_unset=True))
    return cards[card_id]
