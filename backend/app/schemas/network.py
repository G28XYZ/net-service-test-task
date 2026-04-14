from pydantic import BaseModel, ConfigDict

from app.models.entities import Network


class NetworkResponse(Network):
    """Схема ответа с данными сети."""

    model_config = ConfigDict(from_attributes=True)


class NetworkListResponse(BaseModel):
    """Схема ответа со списком сетей."""

    model_config = ConfigDict(from_attributes=True)
    # Коллекция сетей, доступных для просмотра и выбора.
    items: list[NetworkResponse]
