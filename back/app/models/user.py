import enum
from flask_login import UserMixin

from sqlalchemy import Column, Integer, String
from sqlalchemy.dialects.postgresql import ENUM as PgEnum
from sqlalchemy.orm import relationship

from app.database import Base


class UserRole(str, enum.Enum):
    ADMIN = 'admin'
    MANAGER = 'manager'
    CUSTOMER = 'customer'


class User(UserMixin, Base):
    __tablename__ = 'users'

    user_id = Column(Integer, primary_key=True)
    first_name = Column(String(50))
    last_name = Column(String(50))
    email = Column(String(100), unique=True, nullable=False)
    password_hash = Column(String, nullable=False)
    role = Column(
        PgEnum(
            UserRole,
            name='user_role',
            create_type=False,
            values_callable=lambda e: [m.value for m in e],
        ),
        nullable=False,
        default=UserRole.CUSTOMER,
        server_default='customer',
    )

    orders = relationship('Order', back_populates='user')

    def get_id(self):
        return str(self.user_id)