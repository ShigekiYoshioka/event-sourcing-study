from event_sourcing_study.domain.to_do_items.repository import ToDoItemRepository
from event_sourcing_study.domain.to_do_items.to_do_item import ToDoItemId, ToDoItemStatus
from event_sourcing_study.usercase.dto import ToDoItemDto


class ChangeToDoStatus:
    def __init__(self, repository: ToDoItemRepository):
        self._repository = repository

    def __call__(self, todo_id_str: str, next_status_str: str) -> ToDoItemDto:
        todo_id = ToDoItemId.of(todo_id_str)
        next_status = ToDoItemStatus.of(next_status_str)
        todo = self._repository.find_by_id(todo_id)
        todo.change_status(next_status)
        todo = self._repository.save(todo)
        return ToDoItemDto(
            id=todo.id.value,
            title=todo.title.value,
            status=todo.status.name
        )
