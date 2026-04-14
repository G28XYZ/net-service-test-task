from pydantic import BaseModel


class StatusChangeRequest(BaseModel):
    """Схема запроса на изменение состояния ВМ или интерфейса."""

    # Целевой статус сущности, который должен применить backend.
    status: str
