from sqlalchemy.exc import IntegrityError
from werkzeug.security import check_password_hash, generate_password_hash

from app.database import db
from app.models.user import User, UserRole
from app.repo.user_repo import UserRepo


class AuthError(Exception):
    pass

class WeakPassword(AuthError):
    pass

class EmailAlreadyRegistered(AuthError):
    pass

class InvalidCredentials(AuthError):
    pass

MIN_PASSWORD_LENGTH = 8

def _normalize_email(email: str) -> str:
    return email.strip().lower()

class AuthService:
    def __init__(self):
        self.user_repo = UserRepo()

    def register(self, email: str, password: str, first_name: str = None, last_name: str = None) -> User:
        email = _normalize_email(email)

        if len(password) < MIN_PASSWORD_LENGTH:
            raise WeakPassword(f'Пароль должен быть не короче {MIN_PASSWORD_LENGTH} символов')

        if self.user_repo.get_by_email(email) is not None:
            raise EmailAlreadyRegistered('Пользователь с таким email уже существует')

        try:
            user = self.user_repo.create(
                email=email,
                password_hash=generate_password_hash(password),
                first_name=first_name,
                last_name=last_name,
            )
            db.session.commit()
            return user
        except IntegrityError:
            db.session.rollback()
            raise EmailAlreadyRegistered('Пользователь с таким email уже существует')

    def login(self, email: str, password: str) -> User:
        email = _normalize_email(email)
        user = self.user_repo.get_by_email(email)

        if user is None or not check_password_hash(user.password_hash, password):
            raise InvalidCredentials('Неверный email или пароль')

        return user