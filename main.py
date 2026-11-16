import sqlite3

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

DB_PATH = "cards.db"

app = FastAPI()

def get_conn() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db() -> None:
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS cards (
            id          INTEGER PRIMARY KEY AUTOINCrEMENT,
            topic       TEXT NOT NULL,
            question    TEXT NOT NULL,
            answer      TEXT NOT NULL
            )
        """)

init_db()

class CardIn(BaseModel):
    topic: str
    question: str
    answer: str

class CardPatch(BaseModel):
    topic: str | None = None
    question: str | None = None
    answer: str | None = None

class Card(CardIn):
    id: int

def get_or_404(conn: sqlite3.Connection, card_id: int) -> dict:
    row = conn.execute("SELECT * FROM cards WHERE id = ?", (card_id,)).fetchone()
    if row is None:
        raise HTTPException(status_code=404, detail="Card not found")
    return dict(row)

@app.post("/cards", status_code=201, response_model=Card)
def create_card(card: CardIn):
    with get_conn() as conn:
        cur = conn.execute(
            "INSERT INTO cards (topic, question, answer) VALUES (?, ?, ?)",
            (card.topic, card.question, card.answer),
        )
        return get_or_404(conn, cur.lastrowid)

@app.get("/cards", response_model=list[Card])
def list_cards(topic: str | None = None):
    with get_conn() as conn:
        if topic:
            rows = conn.execute("SELECT * FROM cards WHERE topic = ?", (topic,)).fetchall()
        else:
            rows = conn.execute("SELECT * FROM cards").fetchall()
    return [dict(row) for row in rows]

@app.get("/cards/{card_id}", response_model=Card)
def get_card(card_id: int):
    with get_conn() as conn:
        return get_or_404(conn, card_id)


@app.put("/cards/{card_id}", response_model=Card)
def update_card(card_id: int, card: CardIn):
    with get_conn() as conn:
        get_or_404(conn, card_id)
        conn.execute(
            "UPDATE cards SET topic = ?, question = ?, answer = ? WHERE id = ?",
            (card.topic, card.question, card.answer, card_id),
        )
        return get_or_404(conn, card_id)


@app.patch("/cards/{card_id}", response_model=Card)
def patch_card(card_id: int, card: CardPatch):
    with get_conn() as conn:
        merged = {**get_or_404(conn, card_id), **card.model_dump(exclude_unset=True)}
        conn.execute(
            "UPDATE cards SET topic = ?, question = ?, answer = ? WHERE id = ?",
            (merged["topic"], merged["question"], merged["answer"], card_id),
        )
        return get_or_404(conn, card_id)


@app.delete("/cards/{card_id}", status_code=204)
def delete_card(card_id: int):
    with get_conn() as conn:
        get_or_404(conn, card_id)
        conn.execute("DELETE FROM cards WHERE id = ?", (card_id,))