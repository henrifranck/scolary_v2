from typing import Any

from sqlalchemy.orm import as_declarative, declared_attr


def camel_to_snake(name: str) -> str:
    """Convert CamelCase class name to snake_case table name."""
    snake_case = ""
    for i, char in enumerate(name):
        if char.isupper() and i != 0:
            snake_case += "_"
        snake_case += char.lower()
    return snake_case


@as_declarative()
class Base:
    id: Any
    __name__: str

    # Generate __tablename__ automatically
    @declared_attr
    def __tablename__(cls) -> str:
        return camel_to_snake(cls)
