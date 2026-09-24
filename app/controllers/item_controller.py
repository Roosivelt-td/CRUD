from fastapi import APIRouter, Depends, Request, Form, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional

from app.database import get_db
from app.models.item import ItemModel

router = APIRouter()
templates = Jinja2Templates(directory="app/views/templates")

@router.get("/")
def read_root(request: Request, search: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(ItemModel)
    if search:
        query = query.filter(
            ItemModel.title.ilike(f"%{search}%") |
            ItemModel.description.ilike(f"%{search}%")
        )
    items = query.order_by(ItemModel.created_at.desc()).all()
    return templates.TemplateResponse("index.html", {
        "request": request,
        "items": items,
        "search": search or ""
    })

@router.post("/items")
def create_item(
    title: str = Form(...),
    description: Optional[str] = Form(None),
    completed: bool = Form(False),
    db: Session = Depends(get_db)
):
    new_item = ItemModel(title=title, description=description, completed=completed)
    db.add(new_item)
    db.commit()
    db.refresh(new_item)
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/items/{item_id}/update")
def update_item(
    item_id: int,
    title: str = Form(...),
    description: Optional[str] = Form(None),
    completed: bool = Form(False),
    db: Session = Depends(get_db)
):
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    item.title = title
    item.description = description
    item.completed = completed
    db.commit()
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/items/{item_id}/delete")
def delete_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(item)
    db.commit()
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
