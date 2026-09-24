from fastapi import APIRouter, Depends, Request, Form, HTTPException, status
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from typing import Optional
from collections import defaultdict

from app.database import get_db
from app.models.product import ProductModel
from app.models.order import OrderModel
from app.models.user import UserModel

router = APIRouter()
templates = Jinja2Templates(directory="app/views/templates")

def get_session_user(request: Request, db: Session = Depends(get_db)):
    email = request.cookies.get("user_email")
    if not email:
        return None
    return db.query(UserModel).filter(UserModel.email == email).first()

@router.get("/")
def store_home(
    request: Request,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    user = get_session_user(request, db)
    role = user.role if user else "visitor"

    # Query products with optional search
    query = db.query(ProductModel)
    if search:
        query = query.filter(
            ProductModel.name.ilike(f"%{search}%") |
            ProductModel.description.ilike(f"%{search}%")
        )
    products = query.order_by(ProductModel.created_at.desc()).all()

    if role == "admin":
        orders = db.query(OrderModel).order_by(OrderModel.created_at.desc()).all()

        # Prepare data for Chart.js
        product_names = [p.name for p in products]
        product_stocks = [p.stock for p in products]

        # Calculate revenue per product from orders
        product_revenue = defaultdict(float)
        product_sales_qty = defaultdict(int)
        for o in orders:
            if o.product:
                product_revenue[o.product.name] += o.total_price
                product_sales_qty[o.product.name] += o.quantity

        chart_labels = list(product_revenue.keys()) if product_revenue else product_names
        chart_revenues = [product_revenue[name] for name in chart_labels] if product_revenue else [0.0] * len(product_names)

        return templates.TemplateResponse("admin_dashboard.html", {
            "request": request,
            "user": user,
            "role": role,
            "products": products,
            "orders": orders,
            "product_names": product_names,
            "product_stocks": product_stocks,
            "chart_labels": chart_labels,
            "chart_revenues": chart_revenues,
            "search": search or ""
        })
    else:
        my_orders = []
        if user:
            my_orders = db.query(OrderModel).filter(OrderModel.user_id == user.id).order_by(OrderModel.created_at.desc()).all()

        return templates.TemplateResponse("user_store.html", {
            "request": request,
            "user": user,
            "role": role,
            "products": products,
            "my_orders": my_orders,
            "search": search or ""
        })

# --- ADMIN ACTIONS (Product CRUD) ---
@router.post("/admin/products")
def create_product(
    request: Request,
    name: str = Form(...),
    description: Optional[str] = Form(None),
    price: float = Form(...),
    stock: int = Form(...),
    image_url: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    user = get_session_user(request, db)
    if not user or user.role != "admin":
        raise HTTPException(status_code=403, detail="Acceso denegado. Solo para administradores.")

    new_product = ProductModel(
        name=name,
        description=description,
        price=price,
        stock=stock,
        image_url=image_url or "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&auto=format&fit=crop&q=60"
    )
    db.add(new_product)
    db.commit()
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/admin/products/{product_id}/update")
def update_product(
    product_id: int,
    request: Request,
    name: str = Form(...),
    description: Optional[str] = Form(None),
    price: float = Form(...),
    stock: int = Form(...),
    image_url: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    user = get_session_user(request, db)
    if not user or user.role != "admin":
        raise HTTPException(status_code=403, detail="Acceso denegado. Solo para administradores.")

    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    product.name = name
    product.description = description
    product.price = price
    product.stock = stock
    if image_url:
        product.image_url = image_url

    db.commit()
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

@router.post("/admin/products/{product_id}/delete")
def delete_product(
    product_id: int,
    request: Request,
    db: Session = Depends(get_db)
):
    user = get_session_user(request, db)
    if not user or user.role != "admin":
        raise HTTPException(status_code=403, detail="Acceso denegado. Solo para administradores.")

    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    db.delete(product)
    db.commit()
    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)

# --- USER ACTIONS (Buy Product - No registration required) ---
@router.post("/user/buy")
def buy_product(
    request: Request,
    product_id: int = Form(...),
    quantity: int = Form(...),
    buyer_name: str = Form("Cliente General"),
    db: Session = Depends(get_db)
):
    user = get_session_user(request, db)

    product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    if product.stock < quantity:
        raise HTTPException(status_code=400, detail="Stock insuficiente para esta compra.")

    product.stock -= quantity
    total_price = product.price * quantity

    final_buyer_name = user.username if user else buyer_name
    user_id = user.id if user else None

    new_order = OrderModel(
        product_id=product.id,
        user_id=user_id,
        quantity=quantity,
        total_price=total_price,
        buyer_name=final_buyer_name
    )
    db.add(new_order)
    db.commit()

    return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
