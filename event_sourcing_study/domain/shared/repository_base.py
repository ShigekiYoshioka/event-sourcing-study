from abc import ABCMeta, abstractmethod
from typing import TypeVar, Generic

from event_sourcing_study.domain.shared.base_domain_object import BaseId, BaseEntity

ID = TypeVar('ID', bound=BaseId)
T = TypeVar('T', bound=BaseEntity)


class BaseRepository(Generic[ID, T], metaclass=ABCMeta):
    @abstractmethod
    def find_by_id(self, identifier: ID) -> T: ...

    @abstractmethod
    def save(self, entity: T) -> T: ...
