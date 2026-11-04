from sqlalchemy import select

from sqlalchemy.orm import Session
from app.models.user import User, UserRole


class UserRepo:

    def __init__(self, db: Session):
        self.db = db


    def get_by_id(self, user_id: int) -> User | None:
        return self.db.get(User, user_id)

    def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        return self.db.execute(stmt).scalar_one_or_none()

    def list_all(self) -> list[User]:
        stmt = select(User).order_by(User.user_id)
        return list(self.db.execute(stmt).scalars())

    def create(
        self,
        *,
        email: str,
        password_hash: str,
        first_name: str | None = None,
        last_name: str | None = None,
        role: UserRole = UserRole.CUSTOMER, 
    ) -> User:
        user = User(
            email=email,
            password_hash=password_hash,
            first_name=first_name,
            last_name=last_name,
            role=role,
        )
        self.db.add(user)
        self.db.flush() # Отправляет INSERT в БД, но не коммитит транзакцию
        return user

    def update_role(self, user: User, role: UserRole) -> User:
        user.role = role
        self.db.flush()
        return user