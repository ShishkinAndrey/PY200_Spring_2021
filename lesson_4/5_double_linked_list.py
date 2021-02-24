from typing import Any, Sequence, Optional

"""
Двусвязный список на основе односвязного списка.
    Самостоятельное задание. В двусвязном списке должны быть следующие методы:
    - **`__str__`**
    - **`__repr__`**
    - **`__getitem__`**
    - **`__setitem__`**
    - **`__len__`**
    - **`insert`**
    - **`index`**
    - **`remove`**
    - **`append`**
    - **`__iter__`**
    Необязательно все эти методы должны быть переопределены в явном виде. По максимуму используйте
    наследование, если поведение списков в контексте реализации указанных метод схоже.
    С точки зрения наследования по минимуму перегружайте методы. При необходимости рефакторите базовый класс,
    чтобы локализовать части кода во вспомогательные функции, которые имеют различное поведение
    в связном и двусвязном списках.
    Стремитесь к минимизации кода в дочернем классе.
    Есть какой-то метод класса DoubleLinkedList хотите отработать в явном виде ещё раз, не возбраняется.
"""


# ToDo импорт любой вашей реалиазации LinkedList

class LinkedList:
    class Node:
        """
        Внутренний класс, класса LinkedList.
        Пользователь напрямую не работает с узлами списка, узлами оперирует список.
        """

        def __init__(self, value: Any, next_: Optional['Node'] = None):
            """
            Создаем новый узел для односвязного списка
            :param value: Любое значение, которое помещено в узел
            :param next_: следующий узел, если он есть
            """
            self.value = value
            self.next = next_  # Вызывается сеттер

        def _check_node(self, node_):
            if not isinstance(node_, self.__class__) and node_ is not None:
                msg = f"Устанавливаемое значение должно быть экземпляром класса {self.__class__.__name__} " \
                      f"или None, не {node_.__class__.__name__}"
                raise TypeError(msg)

        @property
        def next(self):
            """Getter возвращает следующий узел связного списка"""
            return self.__next

        @next.setter
        def next(self, next_: Optional['Node']):
            """Setter проверяет и устанавливает следующий узел связного списка"""
            self._check_node(next_)
            self.__next = next_

        def __repr__(self):
            """Метод должен возвращать строку, показывающую, как может быть создан экземпляр."""
            return f"Node({self.value}, next_={None})"

        def __str__(self):
            """Вызывается функциями str, print и format. Возвращает строковое представление объекта."""
            return f"{self.value}"

    def __init__(self, data: Sequence = None):
        """Конструктор связного списка"""
        self._len = 0
        self.head = None  # Node
        self.tail = None

        if self.is_iterable(data):  # ToDo Проверить, что объект итерируемый. Метод self.is_iterable
            for value in data:
                self.append(value)

    @property
    def _len(self):
        return self.__len

    @_len.setter
    def _len(self, len_value):
        if not isinstance(len_value, int):
            raise TypeError()
        elif len_value < 0:
            raise ValueError()
        self.__len = len_value

    def __str__(self):
        """Вызывается функциями str, print и format. Возвращает строковое представление объекта."""
        result = self.__copy__()
        return f"{result}"

    def __repr__(self):
        """Метод должен возвращать строку, показывающую, как может быть создан экземпляр."""
        result = self.__copy__()
        return f'{self.__class__.__name__}({result})'

    def __copy__(self):
        copy_list = []
        current_node = self.head
        for _ in range(self._len):
            copy_list.append(current_node.value)
            current_node = current_node.next
        return copy_list

    def __len__(self):
        return self._len

    def __getitem__(self, item: (int, slice)) -> Any:
        print('Вызван __getitem__')
        if isinstance(item, slice):
            start, stop, step = item.indices(len(self))
            return [self[i] for i in range(start, stop, step)]
        else:
            self.__check_index(item)
            current_node = self._step_by_step_to_node(item)
            return current_node.value

    def __setitem__(self, key, value):
        self.__check_index(key)
        current_node = self._step_by_step_to_node(key)
        current_node.value = value

    def __iter__(self):
        print('Вызван метод __iter__')
        value = self.__node_iterator()
        return value

    def __node_iterator(self):
        print('Вызван метод __node_iterator')
        current_val = self.head
        while current_val is not None:
            yield current_val
            current_val = current_val.next

    def __check_index(self, index) -> None:
        print('Вызван __check_index')
        if not isinstance(index, int):
            raise TypeError()
        elif abs(index) >= self._len:
            raise IndexError()

    def _step_by_step_to_node(self, index) -> 'Node':
        print('Вызван __step_by_step_to_node')
        current_node = self.head
        for _ in range(index):
            current_node = current_node.next
        return current_node

    def __reversed__(self):
        for elem in self[::-1]:
            yield elem

    def append(self, value: Any):
        """Добавление элемента в конец связного списка"""
        append_node = self.Node(value)
        if self.head is None:
            self.head = append_node
            self.tail = append_node
        else:
            # ToDo Завести атрибут self.tail, который будет хранить последний узел
            self.__linked_nodes(self.tail, append_node)
            self.tail = append_node
        self._len += 1

    @staticmethod
    def __linked_nodes(left: Node, right: Optional[Node]) -> None:
        left.next = right

    def to_list(self) -> list:
        return [value for value in self]

    def insert(self, index: int, value: Any) -> None:
        if index == 0:
            first_node = self.Node(value)
            self.__linked_nodes(first_node, self.head)
            self.head = first_node
            self._len += 1
        elif 0 < index < (self._len - 1):
            insert_node = self.Node(value)
            prev_node = self._step_by_step_to_node(index - 1)
            next_node = prev_node.next
            self.__linked_nodes(prev_node, insert_node)
            self.__linked_nodes(insert_node, next_node)
            self._len += 1
        elif index >= self._len:
            self.append(value)

    def clear(self) -> None:
        self.head = None

    def index(self, value: Any) -> int:
        current_node = self.head
        for i in range(self._len):
            if current_node.value == value:
                return i
            else:
                current_node = current_node.next
        raise ValueError(f'{value} not in {self.__class__.__name__}')

    def remove(self, value: Any) -> None:
        current_node = self.head
        search_result = False
        for i in range(self._len):
            if current_node.value == value:
                left_node = self._step_by_step_to_node(i - 1)
                next_node = current_node.next
                current_node.value = None
                self.__linked_nodes(left_node, next_node)
                self._len -= 1
                search_result = True
                break
            else:
                current_node = current_node.next
        if not search_result:
            raise ValueError(f'{value} not in list')

    def sort(self) -> None:
        correct_compare = True
        while correct_compare:
            correct_compare = False
            current_elem = self.head
            for i in range(self._len - 1):
                if current_elem.value > current_elem.next.value:
                    current_elem.value, current_elem.next.value = current_elem.next.value, current_elem.value
                    correct_compare = True
                current_elem = current_elem.next

    @staticmethod
    def is_iterable(data) -> bool:
        """Метод для проверки является ли объект итерируемым"""
        if hasattr(data, '__iter__'):
            return True
        raise AttributeError(f'{data.__class__.__name__} is not iterable')


class DoubleLinkedList(LinkedList):
    class DoubleLinkedNode(LinkedList.Node):
        def __init__(self, value: Any,
                     next_: Optional['Node'] = None,
                     prev: Optional['Node'] = None):
            # ToDo расширить возможности базового конструтора с учетом особенностей двусвязного списка
            super().__init__(value, next_)
            self.prev = prev

        @property
        def prev(self):
            return self.__prev

        @prev.setter
        def prev(self, prev_node: Optional['Node']):
            self._check_node(prev_node)
            self.__prev = prev_node

        def __repr__(self) -> str:
            """Метод должен возвращать строку, показывающую, как может быть создан экземпляр."""
            # ToDo перегрузить метод
            return f'Node({self.value}, next_={None}, prev={None})'

    def __init__(self, data: Sequence = None):
        """Конструктор двусвязного списка"""
        super().__init__(data)

    @staticmethod
    def __linked_nodes(left: DoubleLinkedNode, right: Optional[DoubleLinkedNode]) -> None:
        left.next = right
        right.prev = left

    def append(self, value: Any):
        append_node = self.DoubleLinkedNode(value)
        if self.head is None:
            self.head = append_node
            self.tail = append_node
        else:
            self.__linked_nodes(self.tail, append_node)
            self.tail = append_node
        self._len += 1

    def insert(self, index: int, value: Any):
        insert_node = self.DoubleLinkedNode(value)
        if index == 0:
            self.__linked_nodes(insert_node, self.head)
            self.head = insert_node
            self._len += 1
        elif 0 < index < self._len:
            next_node = self._step_by_step_to_node(index)
            prev_node = next_node.prev
            self.__linked_nodes(prev_node, insert_node)
            self.__linked_nodes(insert_node, next_node)
            self._len += 1
        elif index >= self._len:
            self.append(value)

    def remove(self, value: Any) -> None:
        remove_node = self.head
        search_result = False
        for i in range(self._len):
            if value == remove_node.value:
                prev_node = remove_node.prev
                next_node = remove_node.next
                self.__linked_nodes(prev_node, next_node)
                self._len -= 1
                search_result = True
                break
            else:
                remove_node = remove_node.next
        if not search_result:
            raise ValueError(f'{value} not in list')



if __name__ == '__main__':
    ll = LinkedList('abcd')
    iter(ll)
    # ll.insert(2,'ww')
    print(ll[1])




