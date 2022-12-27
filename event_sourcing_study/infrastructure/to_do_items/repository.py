from typing import Dict, Tuple

from event_sourcing_study.domain.shared.base_domain_object import DomainEvent
from event_sourcing_study.domain.to_do_items.repository import ToDoItemRepository
from event_sourcing_study.domain.to_do_items.to_do_item import ToDoItemId, ToDoItem


class OnMemoryToDoItemRepository(ToDoItemRepository):
    def __init__(self):
        self._kvs: Dict[Tuple[ToDoItemId, int], DomainEvent] = dict()

    def find_by_id(self, identifier: ToDoItemId) -> ToDoItem:
        events = list(map(lambda item: item[1], sorted(filter(lambda item: item[0][0] == identifier, self._kvs.items()), key=lambda item: item[0][1])))
        return ToDoItem(events)

    def save(self, entity: ToDoItem) -> ToDoItem:
        change_count = len(entity.changes)
        initial_revision = entity.revision - change_count
        for n, event in enumerate(entity.changes):
            key = (entity.id, initial_revision + n)
            if key in self._kvs:
                raise RuntimeError('conflict event')
            self._kvs[key] = event
        return entity
