from dataclasses import dataclass


@dataclass
class ToDoItemDto:
    id: str
    title: str
    status: str
