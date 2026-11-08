from app.repo.order_repo import OrderRepo


class ManagerService:
    def __init__(self, session):
        self.order_repo = OrderRepo(session)

    def get_orders(self):
        return self.order_repo.list_all()