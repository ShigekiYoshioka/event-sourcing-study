from abc import ABCMeta

from event_sourcing_study.domain.shared.repository_base import BaseRepository
from event_sourcing_study.domain.to_do_items.to_do_item import ToDoItemId, ToDoItem


class ToDoItemRepository(BaseRepository[ToDoItemId, ToDoItem], metaclass=ABCMeta):
    pass
