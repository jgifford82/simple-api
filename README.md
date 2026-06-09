# Simple API

A minimal FastAPI service with in-memory CRUD for items.

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
source .venv/bin/activate
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

- Docs: http://127.0.0.1:8000/docs
- OpenAPI: http://127.0.0.1:8000/openapi.json

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/items` | List all items |
| GET | `/items/{id}` | Get one item |
| POST | `/items` | Create item (`{"name": "..."}`) |
| PUT | `/items/{id}` | Update item name |
| DELETE | `/items/{id}` | Delete item |

## Examples

```bash
curl http://127.0.0.1:8000/health

curl -X POST http://127.0.0.1:8000/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Widget"}'

curl http://127.0.0.1:8000/items

curl -X PUT http://127.0.0.1:8000/items/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Super Widget"}'

curl -X DELETE http://127.0.0.1:8000/items/1
```

Data is stored in memory and resets when the server restarts.
