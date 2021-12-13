from typing import Optional


class Node:
    def __init__(self, value: int, next: Optional['Node'] = None):
        self.value = value
        self.next = next


class LinkedList:

    def __init__(self, node):
        self.head = node if node else None

    def reverse(self, node: Node) -> Node:
        # исходный объект
        # Node(1, Node(2, Node(3, None)))
        # результирующий объект
        # Node(3, Node(2, Node(1, None)))

        # без списка и нового объекта
        node_values = []

        while node.next:
            # можно ток по ссылкам идти и не трогать значения, а я в значения полез(
            node_values.append(node.value)
            node = node.next

        node_prev = None

        for i in range(len(node_values)):
            # вот этот не создавать
            new_node = Node(node_values[-i], node_prev)
            node_prev = new_node

        return new_node

    # !рабочий способ с инета)
    def reverse_res(self) -> Node:
        # Python program to reverse a linked list
        # Time Complexity : O(n)
        # Space Complexity : O(n) as 'next'
        # variable is getting created in each loop.

        prev = None
        current = self.head

        # идем по связанному списку, меняя ссылки в обратную сторону
        # и даже не трогаем значения)
        while current is not None:
            # пузырьком меняем ссылки, сохраняя предыдущую ссылку и записываю новую в текущую
            next = current.next
            current.next = prev
            prev = current

            current = next

        # вот тут записываем пересобранный связанный список в поле объекта
        self.head = prev

        return self.head


if __name__ == '__main__':
    node = Node(3, Node(2, Node(1, None)))

    llist = LinkedList(node)

    llist.reverse()

    # print(reverse(node))
    # reverse_new(node)
    # node = reverse_3(node)

    # while node.next:
    #     print(node.value)
    #     node = node.next
