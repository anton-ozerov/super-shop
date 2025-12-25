from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from shop_app.database.database import Base


class Group(Base):
    __tablename__ = 'group'

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str | None]

class GroupProdictAssignment(Base):
    __tablename__ = 'group_prodict_assignment'

    id: Mapped[int] = mapped_column(primary_key=True)
    group_id: Mapped[int] = mapped_column(
        ForeignKey('group.id', ondelete='CASCADE'),
    )
    product_id: Mapped[int] = mapped_column(
        ForeignKey('product.id', ondelete='CASCADE'),
    )
    product_value: Mapped[str]

# Not ready yet
