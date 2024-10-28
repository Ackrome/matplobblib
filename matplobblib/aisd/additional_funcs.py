text3 ='''
# Функция двойного хэширования
def double_hash_function(self, key):
    return 1 + (hash(key) % (self.size-2))
''' + 'abracadabrabibidi' + '''
# Функция для нахождения первого четного элемента в стеке
def find_first_even(stack):
    current = stack.head
    while current:
        if current.data % 2 == 0:
            return current.data
        current = current.next
    return None
''' + 'abracadabrabibidi' + '''
# Альтернативная функция для нахождения первого четного элемента в стеке
def find_first_even(stack):
    temp_stack = Stack()
    even = None

    while not stack.is_empty():
        item = stack.pop()
        temp_stack.push(item)
        if item % 2 == 0:
            even = item
            break

    while not temp_stack.is_empty():
        stack.push(temp_stack.pop())

    return even
''' + 'abracadabrabibidi' + '''
# Функция для добавления нового элемента в стек после первого нечетного элемента
def add_after_first_odd(stack, item):
    current = stack.head
    while current:
        if current.data % 2 != 0:
            new_node = Node(item)
            new_node.next = current.next
            current.next = new_node
            return
        current = current.next
    stack.push(item)
''' + 'abracadabrabibidi' + '''
# Функция для проверки сбалансированности скобок в математическом выражении
def is_balanced(expr):
    stack = Stack()
    for char in expr:
        if char in "({[":
            stack.push(char)
        elif char in ")}]":
            if stack.is_empty():
                return False
            elif char == ")" and stack.peek() == "(":
                stack.pop()
            elif char == "}" and stack.peek() == "{":
                stack.pop()
            elif char == "]" and stack.peek() == "[":
                stack.pop()
            else:
                return False
    return stack.is_empty()
''' + 'abracadabrabibidi' + '''
# Функция для вычисления математических выражений в обратной польской нотации
def evaluate(expression):
    stack = Stack()
    for token in expression:
        if token.isdigit():
            stack.push(int(token))
        else:
            operand_2 = stack.pop()
            operand_1 = stack.pop()
            if token == '+':
                result = operand_1 + operand_2
            elif token == '-':
                result = operand_1 - operand_2
            elif token == '*':
                result = operand_1 * operand_2
            elif token == '/':
                result = operand_1 / operand_2
            stack.push(result)
    return stack.pop()
''' + 'abracadabrabibidi' + '''
# Функция для нахождения первого нечетного элемента очереди
def find_first_odd(queue):
    current = queue.head
    while current:
        if current.data % 2 != 0:
            return current.data
        current = current.next
    return None
''' + 'abracadabrabibidi' + '''
# Функция для добавления нового элемента в очередь перед первым четным элементом
def add_before_first_even(queue, item):
    new_node = Node(item)
    if not queue.head:
        queue.head = new_node
        queue.tail = new_node
    elif queue.head.data % 2 == 0:
        new_node.next = queue.head
        queue.head = new_node
    else:
        prev_node = queue.head
        current = prev_node.next
        while current:
            if current.data % 2 == 0:
                prev_node.next = new_node
                new_node.next = current
                return
            prev_node = current
            current = current.next
        queue.tail.next = new_node
        queue.tail = new_node
''' + 'abracadabrabibidi' + '''
# Альтернативная функция для добавления нового элемента в очередь перед первым четным элементом
def add_before_first_even(queue, data):
    temp_queue = Queue()
    even_found = False

    while not queue.is_empty():
        item = queue.dequeue()
        if item % 2 == 0 and not even_found:
            temp_queue.enqueue(data)
            even_found = True
        temp_queue.enqueue(item)

    while not temp_queue.is_empty():
        queue.enqueue(temp_queue.dequeue())
''' + 'abracadabrabibidi' + '''
# Функция для удвоения каждого четного элемента двусвязного списка
def double_even_nodes(dllist):
    current_node = dllist.head
    while current_node:
        if current_node.data % 2 == 0:
            new_node = Node(current_node.data)
            new_node.next = current_node.next
            new_node.prev = current_node
            if current_node.next:
                current_node.next.prev = new_node
            current_node.next = new_node
            current_node = new_node.next
        else:
            current_node = current_node.next
''' + 'abracadabrabibidi' + '''
# Функция для удаления всех отрицательных элементов из двусвязного списка
def delete_negative_nodes(dllist):
    current_node = dllist.head
    while current_node:
        if current_node.data < 0:
            if current_node.prev:
                current_node.prev.next = current_node.next
            else:
                dllist.head = current_node.next
            if current_node.next:
                current_node.next.prev = current_node.prev
        current_node = current_node.next
''' + 'abracadabrabibidi' + '''
# Функция, возводящая в квадрат все отрицательные элементы в циклическом двусвязном списке
def square_negative_values(cdllist):
    current_node = cdllist.head
    while current_node:
        if current_node.data < 0:
            current_node.data = current_node.data ** 2
        current_node = current_node.next
        if current_node == cdllist.head:
            break
''' + 'abracadabrabibidi' + '''
# Функция для удаления всех элементов из циклического двусвязного списка, кратных 5
def delete_multiples_of_5(cdllist):
    current_node = cdllist.head
    while current_node:
        if current_node.data % 5 == 0:
            cdllist.delete(current_node.data)
        current_node = current_node.next
        if current_node == cdllist.head:
            break
''' + 'abracadabrabibidi' + '''
# Функция для создания случайного дерева заданной глубины (каждый узел имеет два дочерних узла)
def create_tree(levels):
    tree = Tree()
    nodes = 2**(levels+1) - 1
    values = list(range(1,nodes+1))
    shuffle(values)

    for i in range(nodes):
        value = values[i]
        if i == 0:
            tree.add_node(value)
        else:
            parent_index = (i-1)//2
            parent_value = values[parent_index]
            tree.add_node(value, parent_value)

    return tree
''' + 'abracadabrabibidi' + '''
# Функция для замены каждого числа в дереве на сумму чисел всех его потомков
def replace_with_sum_of_children(tree, node=None):
    if node is None:
        node = tree.root
    if not node.children:
        return node.value
    else:
        sum_of_children = 0
        for child in node.children:
            sum_of_children += replace_with_sum_of_children(tree, child)
        node.value = sum_of_children
        return sum_of_children
''' + 'abracadabrabibidi' + '''
# Функция, удваивающая каждое нечетное число в дереве
def double_odd_values(tree, node=None):
    if node is None:
        node = tree.root
    if node.value % 2 == 1:
        node.value *= 2
    for child in node.children:
        double_odd_values(tree, child)
    return tree
''' + 'abracadabrabibidi' + '''
# Функция для определения листьев дерева
def find_leaves(tree, node=None, leaves=None):
    if leaves is None:
        leaves = []
    if node is None:
        node = tree.root
    if len(node.children) == 0:
        leaves.append(node.value)
    else:
        for child in node.children:
            find_leaves(tree, child, leaves)
    return leaves
''' + 'abracadabrabibidi' + '''
# Функция для нахождения количества узлов в бинарном дереве
def count_nodes(node):
    if node is None:
        return 0
    return 1 + count_nodes(node.left) + count_nodes(node.right)
''' + 'abracadabrabibidi' + '''
# Функция для нахождения всех узлов, которые являются родительскими для заданного узла в бинарном дереве
def find_parents(node, target_node):
    if node is None:
        return []
    if node.left == target_node or node.right == target_node:
        return [node.data]
    left = find_parents(node.left, target_node)
    right = find_parents(node.right, target_node)
    if left:
        return [node.data] + left
    elif right:
        return [node.data] + right
    else:
        return []
''' + 'abracadabrabibidi' + '''
# Функция для нахождения всех узлов, которые имеют значение больше или равно заданному значению в бинарном дереве
def find_nodes(node, value):
    if node is None:
        return []
    result = []
    if node.data >= value:
        result.append(node.data)
    result += find_nodes(node.left, value)
    result += find_nodes(node.right, value)
    return result
''' + 'abracadabrabibidi' + '''
# Функция для нахождения наиболее часто встречающегося значения в хеш-таблице (по полю species)
def most_common_species(hash_table):
    species_count = {}
    for slot in hash_table.table:
        for _, animal in slot:
            if animal.species in species_count:
                species_count[animal.species] += 1
            else:
                species_count[animal.species] = 1
    return max(species_count, key=species_count.get)
'''
