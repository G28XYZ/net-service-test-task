from app.models.entities import NetworkInterface
from pydantic import BaseModel, ConfigDict


class InterfaceCreateRequest(BaseModel):
    """Схема запроса на создание сетевого интерфейса."""

    # Имя нового интерфейса, например eth0.
    name: str
    # Идентификатор виртуальной машины, к которой подключается интерфейс.
    vmId: int
    # Идентификатор сети, в которую подключается интерфейс.
    networkId: int


class InterfaceResponse(NetworkInterface):
    """Схема ответа с данными сетевого интерфейса."""

    model_config = ConfigDict(from_attributes=True)


class InterfaceListResponse(BaseModel):
    """Схема ответа со списком сетевых интерфейсов."""

    model_config = ConfigDict(from_attributes=True)
    # Коллекция интерфейсов, доступных пользователю.
    items: list[InterfaceResponse]
