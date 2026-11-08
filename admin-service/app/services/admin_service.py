from app.models.user import UserRole
from app.repo.user_repo import UserRepo


class AdminService:
    def __init__(self, session):
        self.user_repo = UserRepo(session)

    def get_users(self):
        return self.user_repo.list_all()

    def change_role(self, actor_id, user_id, role_value):
        user = self.user_repo.get_by_id(user_id)

        if user is None:
            raise ValueError("Пользователь не найден.")

        try:
            role = UserRole(role_value)
        except ValueError:
            raise ValueError("Неизвестная роль.") from None

        if actor_id == user_id:
            raise ValueError("Свою роль здесь изменить нельзя.")

        return self.user_repo.update_role(user, role)