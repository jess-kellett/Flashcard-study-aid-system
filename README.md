A REST API for revision flashcards, built with Python and FastAPI. Each card has a topic, a question and an answer. A small command-line quiz script uses the API to test you on your cards.

> **Work in progress.** This is the early stage of the project. Cards are currently stored in memory, so they reset when the server restarts. Moving storage to a SQLite database is the next step.

## Features so far

- Full **CRUD** for flashcards: create, read, update and delete
- **Partial updates** with `PATCH`, so you can fix one field without resending the whole card
- **Filter by topic**, e.g. `GET /cards?topic=Networks`
- **Request validation** with Pydantic models: invalid requests get a clear `422` error automatically
- Correct HTTP status codes: `201 Created`, `204 No Content`, `404 Not Found`, `422 Unprocessable Entity`
- **Interactive API docs** generated automatically at `/docs`
- **Quiz client** (`quiz.py`) that fetches your cards over HTTP, shuffles them and keeps score

## Endpoints

| Method | Path | What it does | Success code |
|--------|------|--------------|--------------|
| `GET` | `/` | Check the API is running | 200 |
| `GET` | `/cards` | List all cards (optional `?topic=` filter) | 200 |
| `GET` | `/cards/{card_id}` | Get one card by ID | 200 |
| `POST` | `/cards` | Create a new card | 201 |
| `PUT` | `/cards/{card_id}` | Replace a card (all fields required) | 200 |
| `PATCH` | `/cards/{card_id}` | Update only the fields you send | 200 |
| `DELETE` | `/cards/{card_id}` | Delete a card | 204 |

Any request for a card ID that doesn't exist returns `404 Card not found`.

### Example card

```json
{
  "id": 1,
  "topic": "Networks",
  "question": "What does TCP stand for?",
  "answer": "Transmission Control Protocol"
}
```

## Project structure

```
├── main.py      # the FastAPI app: card models and all endpoints
└── quiz.py      # command-line quiz client that calls the API
```

### Data models

- **`CardIn`**: the shape of a new or replacement card (`topic`, `question`, `answer`, all required). Used by `POST` and `PUT`.
- **`CardPatch`**: the same fields, all optional. Used by `PATCH`, with `model_dump(exclude_unset=True)` so only the fields the client actually sent are changed.

## How to run

This project uses [uv](https://docs.astral.sh/uv/) to manage Python and dependencies.

1. Install the dependencies:
   ```
   uv add "fastapi[standard]" httpx
   ```
2. Start the API server:
   ```
   uv run uvicorn main:app --reload
   ```
   The API runs at `http://127.0.0.1:8000`.
3. Open `http://127.0.0.1:8000/docs` in a browser to see and try every endpoint.
4. In a **second terminal**, with the server still running, start the quiz:
   ```
   uv run quiz.py
   ```

## Technologies

- Python 3
- FastAPI
- Pydantic
- Uvicorn
- httpx
- uv

## Roadmap

- [x] CRUD endpoints for cards
- [x] Quiz client
- [x] Filter cards by topic
- [x] Partial updates with `PATCH`
- [ ] Response models, so the API has a fixed output shape
- [ ] Refactor the repeated "card not found" check into a helper function
- [ ] Store cards in a SQLite database so they survive a restart
- [ ] Track quiz attempts, to see which cards you get wrong most often

## Author

Jess Kellett
