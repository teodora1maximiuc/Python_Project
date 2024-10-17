def exercitiul_1(n):
    fibonacci = []
    if n >= 1:
        fibonacci.append(1)
    if n >= 2:
        fibonacci.append(1)
    for i in range(2, n):
        fibonacci.append(fibonacci[-1]+fibonacci[-2])
    return fibonacci
# n = int(input("First n fibonacci numbers. n = "))
# print(f"Result: {exercitiul_1(n)}")
print(f"Ex.1: Result for n=8: {exercitiul_1(8)}")

def exercitiul_2(numbers):
    primeNumbers = []
    for i in numbers:
        flag = True
        if i == 0 and i == 1: flag = False
        for j in range(2, int(i**0.5) + 1):
            if i%j == 0: flag = False
        if flag == True:
            primeNumbers.append(i)
    return primeNumbers
# numbers=list(map(int,input("Enter numbers to check for prime numbers: ").split()))
# print(f"Result: {exercitiul_2(numbers)}")
print(f"Ex.2: Result for [21, 7, 17, 5, 25, 18]: {exercitiul_2([21, 7, 17, 5, 25, 18])}")

def exercitiul_3(a, b):
    intersection = []
    reunion = []
    b_a = []
    a_b = []
    for i in a:
        for j in b:
            if i == j:
                intersection.append(i)
    for i in a: 
        notInIntersection = True
        for j in intersection:
            if i == j: 
                notInIntersection = False
                break
        if notInIntersection == True:
            #all numbers in a except the ones in b
            reunion.append(i) 
            a_b.append(i)
    for i in b:
        reunion.append(i) #the rest of the numbers (b)
        notInIntersection = True
        for j in intersection:
            if i == j:
                notInIntersection = False
                break
        if notInIntersection == True:
            b_a.append(i)
    print("Ex.3: Result for a=[1, 2, 3, 5, 6, 7] and b=[3, 5, 6, 12]")
    print(f"Intersection: {intersection}")
    print(f"Reunion: {reunion}")
    print(f"b-a: {b_a}")
    print(f"a-b: {a_b}")
# a=list(map(int,input("Enter numbers in list a: ").split()))
# b=list(map(int,input("Enter numbers in list b: ").split()))
# exercitiul_3(a,b)
exercitiul_3([1, 2, 3, 5, 6, 7], [3, 5, 6, 12])

def exercitiul_4(notes, moves, start_pos):
    song = []  
    current_pos = start_pos
    
    for move in moves:
        song.append(notes[current_pos])
        current_pos = (current_pos + move) % len(notes)
    
    song.append(notes[current_pos])
    return song

notes = ["do", "re", "mi", "fa", "sol"]
moves = [1, -3, 4, 2]
start_pos = 2
result = exercitiul_4(notes, moves, start_pos)
print(f"Ex.4: Result: {result}")

def exercitiul_5(rows, columns, matrix):
    for i in range(rows):
        for j in range(columns):
            if i > j:
                matrix[i][j] = 0
    return matrix
rows = 4
columns = 4
matrix = [[1, 2, 3, 4],
          [2, 3, 3, 2],
          [1, 1, 1, 1],
          [2, 9, 9, 9]]
print(f"Ex.5: Initial matrix: {matrix}")
print(f"Modified: {exercitiul_5(rows, columns, matrix)}")

def exercitiul_6(x, *lists):
    counts = {}

    for lst in lists:
        for item in lst:
            if item in counts:
                counts[item] += 1
            else:
                counts[item] = 1
    result = []
    for item, count in counts.items():
        if count == x:
            result.append(item)
    return result

result = exercitiul_6(2, [1, 2, 3], [2, 3, 4], [2, 5, 6])
print(f"Ex.6: Result for 2, [1, 2, 3], [2, 3, 4], [2, 5, 6]: {result}")

def exercitiul_7(numbers):
    count = 0
    maxi = 0
    for number in numbers:
        if number%10 == 0 and number != 0:
            continue
        if number < 10:
            count += 1
            if number > maxi: maxi = number
            continue
        copy = number
        palindrom = 0
        while copy != 0:
            c = copy%10
            palindrom = palindrom * 10 + c
            copy //= 10
        if palindrom == number:
            count += 1
            if number > maxi: maxi = number
    print(f"Ex.7: In [12, 565, 11, 89, 4] -> number of palindroms: {count}; greatest palindrom: {maxi}")
# numbers=list(map(int,input("Enter numbers to check palindroms: ").split()))
# exercitiul_7(numbers)
exercitiul_7([12, 565, 11, 89, 4])

def exercitiul_8(x=1, list=[], flag=True):
    result = []
    for string in list:
        divisible = []
        for ch in string:
            ascii_val = ord(ch)
            if flag == True:
                if ascii_val % x == 0:
                    divisible.append(ch)
            else:
                if ascii_val % x != 0:
                    divisible.append(ch)
        result.append(divisible)
    print(f"Ex.8: Result for x=2, [test, hello, lab002], flag=False: {result}")
exercitiul_8(2, ["test", "hello", "lab002"], False)

def exercitiul_9(seats):
    blocked = []
    for row in range(1,len(seats)):
        for column in range(len(seats[row])):
            for i in range(row):
                if seats[row][column] <= seats[i][column]:
                    blocked.append((row, column))
                    break
    print(f"Ex.9: Result: {blocked}")
exercitiul_9([
 [1, 2, 3, 2, 1, 1],
 [2, 4, 4, 3, 7, 2],
 [5, 5, 2, 5, 6, 4],
 [6, 6, 7, 6, 7, 5]])

def exercitiul_10(*lists):
    result = []
    max_length = max(len(lst) for lst in lists)
    for pos in range(max_length):
        tuple_elements = []
        for list in lists:
            if pos < len(list):
                tuple_elements.append(list[pos])
            else:
                tuple_elements.append(None)
        result.append(tuple(tuple_elements))
    print(f"Ex.10: Result: {result}")
exercitiul_10([1,2,3], [5,6,7], ["a", "b", "c", "d"])

def exercitiul_11(tuples):
    result = sorted(tuples, key=lambda x: x[1][2])
    print(f"Ex.11: Result: {result}")
exercitiul_11([('abc', 'bcd'), ('abc', 'zza')])

def exercitiul_12(words):
    result = []
    rhymed = {}
    for word in words:
        rhymed[word] = 0
    for i in range(len(words)-1):
        if rhymed[words[i]] == 1: continue
        rhymed[words[i]] = 1
        rhyme = []
        rhyme.append(words[i])
        for j in range(i+1, len(words)):
            if rhymed[words[j]] == 0:
                if words[i][-2:-1] == words[j][-2:-1]:
                    rhyme.append(words[j])
                    rhymed[words[j]] = 1
        result.append(rhyme)
    print(f"Ex.12: Result: {result}")
exercitiul_12(['ana', 'banana', 'carte', 'arme', 'parte'])