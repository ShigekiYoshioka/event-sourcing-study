from __future__ import annotations

from abc import ABCMeta, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from typing import TypeVar, Generic, List

from pydantic.generics import GenericModel

T = TypeVar('T')


class SingleDataValueObject(GenericModel, Generic[T], metaclass=ABCMeta):
    value: T

    def __hash__(self):
        return hash(self.value)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return other.value == self.value

    class Config:
        allow_mutation = False


class BaseId(SingleDataValueObject[str], metaclass=ABCMeta):
    pass


ID = TypeVar('ID', bound=BaseId)


@dataclass
class BaseEntity(Generic[ID], metaclass=ABCMeta):
    id: ID
    revision: int = field(default=0, init=False)
    changes: List[DomainEvent] = field(default_factory=list, init=False)

    def _mutate(self, event) -> None:
        self._when(event)
        self.revision += 1

    def _apply(self, event: DomainEvent):
        self._mutate(event)
        self.changes.append(event)

    @abstractmethod
    def _when(self, event: DomainEvent) -> None:
        raise NotImplementedError('error')

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return False
        return other.id == self.id


@dataclass
class DomainEvent(metaclass=ABCMeta):
    created_at: datetime = field(default_factory=datetime.now, init=False)
