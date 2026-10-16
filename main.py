from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

class CardIn(BaseModel):
    topic: str
    question: str
    answer: str

class Card(CardIn):
    id: int

class CardPatch(BaseModel):
    topic: str | None = None
    question: str | None = None
    answer: str | None = None

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

def get_or_404(card_id: int) -> dict:
    if card_id not in cards:
        raise HTTPException(status_code=404, detail="Card not found")
    return cards[card_id]

@app.get("/")
def home():
    return {"message": "Study API is running"}


@app.post("/cards", status_code=201, response_model=Card)
def create_card(card: CardIn):
    new_id = max(cards, default=0) + 1
    cards[new_id] = {"id": new_id, **card.model_dump()}
    return cards[new_id]

@app.get("/cards", response_model=list[Card])
def list_cards(topic: str | None = None):
    result = list(cards.values())
    if topic:
        result = [c for c in result if c["topic"] == topic]
    return result

@app.get("/cards/{card_id}", response_model=Card)
def get_card(card_id: int):
    return get_or_404(card_id)


@app.put("/cards/{card_id}", response_model=Card)
def update_card(card_id: int, card: CardIn):
    get_or_404(card_id)
    cards[card_id] = {"id": card_id, **card.model_dump()}
    return cards[card_id]


@app.patch("/cards/{card_id}", response_model=Card)
def patch_card(card_id: int, card: CardPatch):
    get_or_404(card_id).update(card.model_dump(exclude_unset=True))
    return cards[card_id]


@app.delete("/cards/{card_id}", status_code=204)
def delete_card(card_id: int):
    get_or_404(card_id)
    del cards[card_id]
