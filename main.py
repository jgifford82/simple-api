from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI(title="Simple API")

items: dict[int, dict] = {}
next_id = 1


class ItemCreate(BaseModel):
    name: str


class Item(BaseModel):
    id: int
    name: str


class ItemUpdate(BaseModel):
    name: str


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/items", response_model=list[Item])
def list_items():
    return [Item(**item) for item in items.values()]


@app.get("/items/{item_id}", response_model=Item)
def get_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return Item(**items[item_id])


@app.post("/items", response_model=Item, status_code=201)
def create_item(body: ItemCreate):
    global next_id
    item = {"id": next_id, "name": body.name}
    items[next_id] = item
    next_id += 1
    return Item(**item)


@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, body: ItemUpdate):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    items[item_id]["name"] = body.name
    return Item(**items[item_id])


@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: int):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    del items[item_id]
