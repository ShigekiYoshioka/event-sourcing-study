from __future__ import annotations

import uuid
from dataclasses import dataclass
from enum import Enum
from functools import singledispatchmethod
from typing import overload, List

from event_sourcing_study.domain.shared.base_domain_object import (
    BaseEntity,
    BaseId,
    DomainEvent,
    SingleDataValueObject,
)


@dataclass
class CreateToDoItem(DomainEvent):
    to_do_item_id: ToDoItemId
    title: ToDoItemTitle


@dataclass
class ChangeStatus(DomainEvent):
    to_do_item_id: ToDoItemId
    next_status: ToDoItemStatus


@dataclass
class ChangeTitle(DomainEvent):
    to_do_item_id: ToDoItemId
    new_title: ToDoItemTitle


class ToDoItemId(BaseId):
    @staticmethod
    def generate() -> ToDoItemId:
        return ToDoItemId(value=str(uuid.uuid4()))

    @staticmethod
    def of(value: str) -> ToDoItemId:
        return ToDoItemId(value=value)


class ToDoItemTitle(SingleDataValueObject[str]):
    @staticmethod
    def of(value: str) -> ToDoItemTitle:
        return ToDoItemTitle(value=value)


class ToDoItemStatus(Enum):
    TODO = 'TODO'
    DOING = 'DOING'
    DONE = 'DONE'
    DELETED = 'DELETED'

    @staticmethod
    def of(name: str) -> ToDoItemStatus:
        for e in ToDoItemStatus:
            if e.name == name:
                return e
        raise ValueError(f'unknown status: {name}')


@dataclass
class ToDoItem(BaseEntity[ToDoItemId]):
    title: ToDoItemTitle
    status: ToDoItemStatus

    @overload
    def __init__(self, create_event: CreateToDoItem): ...

    @overload
    def __init__(self, events: List[DomainEvent]): ...

    @singledispatchmethod
    def __init__(self, create_event: CreateToDoItem):
        self._apply(create_event)

    @__init__.register
    def _replay_constructor(self, events: list):
        for event in events:
            self._mutate(event)

    @overload
    def _when(self, event: CreateToDoItem) -> None: ...

    @overload
    def _when(self, event: ChangeTitle) -> None: ...

    @singledispatchmethod
    def _when(self, event) -> None:
        raise NotImplementedError('error')

    @_when.register
    def _create_to_do(self, event: CreateToDoItem) -> None:
        super(ToDoItem, self).__init__(event.to_do_item_id)
        self.title = event.title
        self.status = ToDoItemStatus.TODO

    def change_status(self, next_status: ToDoItemStatus) -> None:
        event = ChangeStatus(to_do_item_id=self.id, next_status=next_status)
        self._apply(event)

    @_when.register
    def _change_status(self, event: ChangeStatus) -> None:
        self.status = event.next_status

    def change_title(self, new_title: ToDoItemTitle) -> None:
        event = ChangeTitle(to_do_item_id=self.id, new_title=new_title)
        self._apply(event)

    @_when.register
    def _change_title(self, event: ChangeTitle) -> None:
        self.title = event.new_title

    @staticmethod
    def create(title: ToDoItemTitle) -> ToDoItem:
        event = CreateToDoItem(
            to_do_item_id=ToDoItemId.generate(),
            title=title
        )
        return ToDoItem(event)
