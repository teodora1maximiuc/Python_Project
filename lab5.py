#exercitiul 1
class Stack:
    def __init__(s):
        s._items = []
    def push(s, item):
        s._items.append(item)
    def pop(s):
        if s._items:
            return s._items.pop()
        else: return None
    def peek(s):
        if s._items:
            return s._items[-1]
        else: return None
    def size(s):
        return len(s._items)
    def isEmpty(s):
        if s._items:
            return False
        else: return True
stack = Stack()
stack.push(10)
stack.push(20)
stack.push(30)
print(f"Peek stack: {stack.peek()}")
print(f"Pop stack: {stack.pop()}")
print(f"Peek stack: {stack.peek()}")
print(f"Size stack: {stack.size()}")

#exercitiul 2
class Queue:
    def __init__(q):
        q._items = []
    def push(q, item):
        q._items.append(item)
    def pop(q):
        if q._items:
            return q._items.pop(0)
        else: return None
    def peek(q):
        if q._items:
            return q._items[0]
        else: return None
    def size(q):
        return len(q._items)
    def isEmpty(q):
        if q._items:
            return False
        else: return True
queue = Queue()
queue.push(10)
queue.push(20)
queue.push(30)
print(f"Peek queue: {queue.peek()}")
print(f"Pop queue: {queue.pop()}")
print(f"Peek queue: {queue.peek()}")
print(f"Size queue: {queue.size()}")

#exercitiul 3
class Matrix:
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.data = [[0 for _ in range(m)] for _ in range(n)]
    def get(self, i, j):
        return self.data[i][j]
    def set(self, i, j, value):
        self.data[i][j] = value
    def transpose(self):
        transposed = Matrix(self.n, self.m)
        for i in range(self.n):
            for j in range(self.m):
                transposed.set(j, i, self.get(i, j))
        return transposed
    def multiply(self, other):
        multiplied = Matrix(self.n, self.m)
        for i in range(self.n):
            for j in range(other.m):
                multiplied.set(i, j, sum(self.get(i, k) * other.get(k, j) for k in range(self.m)))
        return multiplied
    def apply(self, func):
        for i in range(self.n):
            for j in range(self.m):
                self.data[i][j] = func(self.data[i][j])
    def __str__(self):
        return '\n'.join([' '.join(map(str, row)) for row in self.data])

matrix = Matrix(3, 3)
matrix.set(0, 0, 1)
matrix.set(1, 2, 2)
matrix.set(2, 2, 3)
print("Matrix:")
print(matrix)

transpose_matrix = matrix.transpose()
print("\nTranspose:")
print(transpose_matrix)

product_matrix = matrix.multiply(transpose_matrix)
print("\nProduct:")
print(product_matrix)

matrix.apply(lambda x: x * 2)
print("\nLambda function (x * 2):")
print(matrix)
