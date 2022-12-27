from event_sourcing_study.domain.to_do_items.repository import ToDoItemRepository
from event_sourcing_study.domain.to_do_items.to_do_item import ToDoItemTitle, ToDoItem
from event_sourcing_study.usercase.dto import ToDoItemDto


class CreateNewToDo:
    def __init__(self, repository: ToDoItemRepository):
        self._repository = repository

    def __call__(self, title_str: str) -> ToDoItemDto:
        title = ToDoItemTitle.of(title_str)
        todo = ToDoItem.create(title)
        todo = self._repository.save(todo)
        return ToDoItemDto(
            id=todo.id.value,
            title=todo.title.value,
            status=todo.status.name
        )
