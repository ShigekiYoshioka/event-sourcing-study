# EventSourcingStudy

```
In [0]: from event_sourcing_study.infrastructure.to_do_items.repository import OnMemoryToDoItemRepository
In [1]: repository = OnMemoryToDoItemRepository()

// create todo
In [2]: from event_sourcing_study.usercase.create_new_to_do import CreateNewToDo
In [3]: create_new_to_do = CreateNewToDo(repository)
In [4]: todo = create_new_to_do('hello world')
In [5]: todo
Out[5]: ToDoItemDto(id='b0054284-fdfe-46db-bc15-c71a3ded607b', title='hello world', status='TODO')

// change title
In [6]: from event_sourcing_study.usercase.change_to_do_title import ChangeToDoTitle
In [7]: change_to_do_title = ChangeToDoTitle(repository)
In [8]: change_to_do_title(todo.id, 'hello world2')
Out[8]: ToDoItemDto(id='b0054284-fdfe-46db-bc15-c71a3ded607b', title='hello world2', status='TODO')

// change status
In [9]: from event_sourcing_study.usercase.change_to_do_status import ChangeToDoStatus
In [10]: change_to_do_status = ChangeToDoStatus(repository)
In [11]: change_to_do_status(todo.id, 'DOING')
Out[11]: ToDoItemDto(id='b0054284-fdfe-46db-bc15-c71a3ded607b', title='hello world2', status='DOING')

// see events
In [12]: repository._kvs
Out[12]: 
{(ToDoItemId(value='b0054284-fdfe-46db-bc15-c71a3ded607b'),
  0): CreateToDoItem(created_at=datetime.datetime(2022, 12, 27, 22, 42, 38, 59557), to_do_item_id=ToDoItemId(value='b0054284-fdfe-46db-bc15-c71a3ded607b'), title=ToDoItemTitle(value='hello world')),
 (ToDoItemId(value='b0054284-fdfe-46db-bc15-c71a3ded607b'),
  1): ChangeTitle(created_at=datetime.datetime(2022, 12, 27, 22, 43, 38, 506604), to_do_item_id=ToDoItemId(value='b0054284-fdfe-46db-bc15-c71a3ded607b'), new_title=ToDoItemTitle(value='hello world2')),
 (ToDoItemId(value='b0054284-fdfe-46db-bc15-c71a3ded607b'),
  2): ChangeStatus(created_at=datetime.datetime(2022, 12, 27, 22, 44, 38, 28341), to_do_item_id=ToDoItemId(value='b0054284-fdfe-46db-bc15-c71a3ded607b'), next_status=<ToDoItemStatus.DOING: 'DOING'>)}
```