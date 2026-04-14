from datetime import datetime

from pydantic import BaseModel


class BaseEntity(BaseModel):
    # Базовая схема для всех инфраструктурных сущностей в API.
    # Уникальный идентификатор сущности.
    id: int
    # Человекочитаемое имя сущности.
    name: str
    # Текущее состояние сущности, например running/stopped или up/down.
    status: str
    # Дата и время создания сущности.
    createdAt: datetime


class Network(BaseEntity):
    # Схема сети, доступной для подключения интерфейсов.
    # Подсеть сети в CIDR-формате.
    cidr: str


class VirtualMachine(BaseEntity):
    # Схема виртуальной машины с привязкой к связанным сетям.
    # Список идентификаторов сетей, в которых у ВМ есть интерфейсы.
    networkIds: list[int]


class NetworkInterface(BaseEntity):
    # Схема сетевого интерфейса, который соединяет ВМ и сеть.
    # Идентификатор виртуальной машины, которой принадлежит интерфейс.
    vmId: int
    # Идентификатор сети, в которую включен интерфейс.
    networkId: int
