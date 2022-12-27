from event_sourcing_study.domain.to_do_items.repository import ToDoItemRepository
from event_sourcing_study.domain.to_do_items.to_do_item import ToDoItemId, ToDoItemTitle
from event_sourcing_study.usercase.dto import ToDoItemDto


class ChangeToDoTitle:
    def __init__(self, repository: ToDoItemRepository):
        self._repository = repository

    def __call__(self, todo_id_str: str, new_title_str: str) -> ToDoItemDto:
        todo_id = ToDoItemId.of(todo_id_str)
        new_title = ToDoItemTitle.of(new_title_str)
        todo = self._repository.find_by_id(todo_id)
        todo.change_title(new_title)
        todo = self._repository.save(todo)
        return ToDoItemDto(
            id=todo.id.value,
            title=todo.title.value,
            status=todo.status.name
        )
