from sqlalchemy import select

from app.database import db
from app.models.user import User, UserRole


class UserRepo:
    def get_by_id(self, user_id: int) -> User | None:
        return db.session.get(User, user_id)

    def get_by_email(self, email: str) -> User | None:
        stmt = select(User).where(User.email == email)
        return db.session.execute(stmt).scalar_one_or_none()

    def list_all(self) -> list[User]:
        stmt = select(User).order_by(User.user_id)
        return list(db.session.execute(stmt).scalars())

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
        db.session.add(user)
        db.session.flush() # Отправляет INSERT в БД, но не коммитит транзакцию
        return user

    def update_role(self, user: User, role: UserRole) -> User:
        user.role = role
        db.session.flush()
        return user