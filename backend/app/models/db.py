from datetime import UTC, datetime

from sqlalchemy import DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.base import Base


class NetworkDB(Base):
    # Таблица сетей, к которым можно подключать интерфейсы виртуальных машин.
    __tablename__ = "networks"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="active")
    createdAt: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )
    cidr: Mapped[str] = mapped_column(String(64), nullable=False)

    # Обратная связь на все интерфейсы, подключенные к этой сети.
    interfaces: Mapped[list["NetworkInterfaceDB"]] = relationship(back_populates="network")


class VirtualMachineDB(Base):
    # Таблица виртуальных машин, которыми управляет сервис.
    __tablename__ = "virtual_machines"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="stopped")
    createdAt: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )

    # Все интерфейсы ВМ удаляются вместе с ней через каскад ORM.
    interfaces: Mapped[list["NetworkInterfaceDB"]] = relationship(
        back_populates="virtual_machine",
        cascade="all, delete-orphan",
    )


class NetworkInterfaceDB(Base):
    # Таблица сетевых интерфейсов, связывающих ВМ и сети.
    __tablename__ = "network_interfaces"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    status: Mapped[str] = mapped_column(String(32), nullable=False, default="down")
    createdAt: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=lambda: datetime.now(UTC),
    )
    vmId: Mapped[int] = mapped_column(ForeignKey("virtual_machines.id"), nullable=False)
    networkId: Mapped[int] = mapped_column(ForeignKey("networks.id"), nullable=False)

    # Связь с владельцем интерфейса — виртуальной машиной.
    virtual_machine: Mapped["VirtualMachineDB"] = relationship(back_populates="interfaces")
    # Связь с сетью, в которую включен интерфейс.
    network: Mapped["NetworkDB"] = relationship(back_populates="interfaces")
