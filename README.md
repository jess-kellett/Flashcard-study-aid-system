# Flashcard Study Aid API

A REST API for revision flashcards, built with Python, FastAPI and SQLite. Each card has a topic, a question and an answer. Cards are stored in a SQLite database, so they survive a restart, and a small command-line quiz script uses the API to test you on them.

## Features

- Full **CRUD** for flashcards: create, read, update and delete
- **Persistent storage** in a SQLite database, using Python's built-in `sqlite3` module
- **Parameterised SQL queries** (`?` placeholders) throughout, to prevent SQL injection
- **Partial updates** with `PATCH`, so you can fix one field without resending the whole card
- **Filter by topic**, e.g. `GET /cards?topic=Networks`
- **Request validation** with Pydantic models: invalid requests get a clear `422` error automatically
- **Response models**, so every endpoint returns a consistent, documented shape
- Correct HTTP status codes: `201 Created`, `204 No Content`, `404 Not Found`, `422 Unprocessable Entity`
- **Interactive API docs** generated automatically at `/docs`
- **Quiz client** (`quiz.py`) that fetches your cards over HTTP, shuffles them and keeps score

## Endpoints

| Method | Path | What it does | Success code |
|--------|------|--------------|--------------|
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

## How it works

### Database

Cards are stored in a single table in `cards.db`:

```sql
CREATE TABLE IF NOT EXISTS cards (
    id       INTEGER PRIMARY KEY AUTOINCREMENT,
    topic    TEXT NOT NULL,
    question TEXT NOT NULL,
    answer   TEXT NOT NULL
);
```

The table is created automatically when the server starts. The database assigns each card's `id`, and `NOT NULL` makes sure no field can be left empty.

Each HTTP method maps to a SQL statement:

| Action | HTTP | SQL |
|--------|------|-----|
| Create | `POST` | `INSERT` |
| Read | `GET` | `SELECT` |
| Update | `PUT` / `PATCH` | `UPDATE` |
| Delete | `DELETE` | `DELETE` |

All values are passed to SQLite separately using `?` placeholders, never pasted into the SQL string. This means user input can't change the query itself, which protects the database against SQL injection.

### Data models

- **`CardIn`**: the shape of a new or replacement card (`topic`, `question`, `answer`, all required). Used by `POST` and `PUT`.
- **`CardPatch`**: the same fields, all optional. Used by `PATCH`, with `model_dump(exclude_unset=True)` so only the fields the client actually sent are changed.
- **`Card`**: the shape of a card the API sends back. It extends `CardIn` with an `id`, and is used as the `response_model` for every endpoint except `DELETE`.

Because the API promises a fixed output shape with `Card`, the storage layer is kept separate from what clients see. The database can change without affecting the endpoints, the docs or the quiz client.

### Helper function

`get_or_404` looks up a card by ID and returns a `404` if it doesn't exist. Every endpoint that works on a single card uses it, so the "not found" check is written only once.

## Project structure

```
├── main.py          # the FastAPI app: database setup, models and all endpoints
├── quiz.py          # command-line quiz client that calls the API
├── pyproject.toml   # project details and dependencies
├── uv.lock          # exact dependency versions
└── .gitignore       # keeps .venv, cache files and the database out of the repo
```

`cards.db` is created automatically the first time you run the server. It's in `.gitignore`, so everyone who runs the project gets their own database.

## How to run

This project uses [uv](https://docs.astral.sh/uv/) to manage Python and dependencies.

1. Clone the repo and install the dependencies:
   ```
   git clone https://github.com/jess-kellett/Flashcard-study-aid-system.git
   cd Flashcard-study-aid-system
   uv sync
   ```
2. Start the API server:
   ```
   uv run uvicorn main:app --reload
   ```
   The API runs at `http://127.0.0.1:8000`.
3. Open `http://127.0.0.1:8000/docs` in a browser to see and try every endpoint. Use **POST /cards** to add your first cards. Opening http://127.0.0.1:8000/ also redirects here.
4. In a **second terminal**, with the server still running, start the quiz:
   ```
   uv run quiz.py
   ```

To look at the data directly, open `cards.db` in a database client such as [Beekeeper Studio](https://www.beekeeperstudio.io/), or from the terminal with `sqlite3 cards.db`.

## Technologies

- Python 3
- FastAPI
- Pydantic
- SQLite (`sqlite3`)
- Uvicorn
- httpx
- uv
- Git and GitHub (feature branches and pull requests)

## Possible extensions

- Track quiz attempts in a second table, to show which cards are answered wrong most often
- Add user accounts, so each person has their own set of cards

## Author

Jess Kellett
