from pydantic import BaseModel, ConfigDict

from app.models.entities import VirtualMachine


class VirtualMachineCreateRequest(BaseModel):
    """Схема запроса на создание виртуальной машины."""

    # Имя новой виртуальной машины.
    name: str


class VirtualMachineResponse(VirtualMachine):
    """Схема ответа с данными виртуальной машины."""

    model_config = ConfigDict(from_attributes=True)


class VirtualMachineListResponse(BaseModel):
    """Схема ответа со списком виртуальных машин."""

    model_config = ConfigDict(from_attributes=True)
    # Коллекция виртуальных машин, доступных пользователю.
    items: list[VirtualMachineResponse]
