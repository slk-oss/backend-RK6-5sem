from sqlalchemy import select
from sqlalchemy.orm import Session
from app.database import db
from app.models.order import Order


def get_by_id(db: Session, order_id: int, product_id: int) -> Order | None:
    return db.get(order_id, product_id)

def get_by_user(db:Session, user_id: int) -> list[Order]:
    stmt = (
        select(Order)
        .where(Order.user_id == user_id)
        .order_by(Order.created_at.desc())
    )
    return list(db.execute(stmt).scalars())