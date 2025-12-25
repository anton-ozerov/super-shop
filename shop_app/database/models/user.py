from sqlalchemy.orm import Mapped, mapped_column

from shop_app.database.database import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str]
    hashed_password: Mapped[str]
    name: Mapped[str] = mapped_column(default='Anonymous')
    email: Mapped[str | None]
    phone: Mapped[str | None]
    is_blocked: Mapped[bool] = mapped_column(default=False)
    is_deleted: Mapped[bool] = mapped_column(default=False)
