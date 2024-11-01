def exercitiul_1(a, b):
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
            reunion.append(i) 
            a_b.append(i)
    for i in b:
        reunion.append(i)
        notInIntersection = True
        for j in intersection:
            if i == j:
                notInIntersection = False
                break
        if notInIntersection == True:
            b_a.append(i)
    print("Ex.1: Result for a=[1, 2, 3, 5, 6, 7] and b=[3, 5, 6, 12]")
    print(f"Intersection: {intersection}")
    print(f"Reunion: {reunion}")
    print(f"b-a: {b_a}")
    print(f"a-b: {a_b}")
# a=list(map(int,input("Enter numbers in list a: ").split()))
# b=list(map(int,input("Enter numbers in list b: ").split()))
# exercitiul_1(a,b)
exercitiul_1([1, 2, 3, 5, 6, 7], [3, 5, 6, 12])

def exercitiul_2(s):
    symbols= {}
    for ch in s:
        if ch in symbols:
            symbols[ch] += 1
        else:
            symbols[ch] = 1
    print(f"Ex.2: Result for Ana has apples: {symbols}")
exercitiul_2("Ana has apples.")

def exercitiul_3(d1, d2):
    if not isinstance(d1, dict) and not isinstance(d2, dict):
        return False
    if len(d1) != len(d2):
        return False
    for key in d1:
        if key not in d2:
            return False
        val1 = d1[key]
        val2 = d2[key]
        if isinstance(val1, dict) and isinstance(val2, dict):
            if not exercitiul_3(val1, val2):
                return False
        elif isinstance(val1, list) and isinstance(val2, list):
            if len(val1) != len(val2):
                return False
            for i in range(len(val1)):
                if val1[i] != val2[i]:
                    return False
        elif isinstance(val1, tuple) and isinstance(val2, tuple):
            if len(val1) != len(val2):
                return False
            for i in range(len(val1)):
                if val1[i] != val2[i]:
                    return False
        elif val1!=val2:
            return False
    return True
d1 = {
    'nume': 'Teodora',
    'varsta': 20,
    'adresa': {
        'city': 'Iasi',
        'zipcode': 10001
    },
    'animale': ('Lux', 'Aripa', 'Hiro'),
}
d2 = d1
d3 = {
    'nume': 'Teodora',
    'varsta': 20,
    'adresa': {
        'city': 'Iasi',
        'zipcode': 10002 #aici
    },
    'animale': ('Lux', 'Aripa', 'Hiro'),
}
if exercitiul_3(d1, d3): print("Ex.3: d1 and d2 are identical dictionaries.")
else: print("Ex.3: d1 and d2 are NOT identical dictionaries.")

def exercitiul_4(tag, content, **key_value):
    string = f"<{tag}"
    for key, value in key_value.items():
        string += f' {key} = \"{value}\"'
    string += f"> {content} </{tag}>"
    print(f"Ex.4: {string}")
exercitiul_4("a", "Hello there", href =" http://python.org ", _class =" my-link ", id= " someid ")

def exercitiul_5(rules, d):
    for key, prefix, middle, sufix in rules:
        if key not in d:
            return False
        val = d[key]
        if not val.startswith(prefix):
            return False
        if not val.endswith(sufix):
            return False
        middle_index = val.find(middle)
        if middle_index == -1 or middle_index == 0 or middle_index + len(middle) == len(val):
            return False
    return True

rules = {
    ("name", "Dr.", "ohn", "Doe"),
    ("title", "Prof", "esso", "r"),
}

dictionary = {
    "name": "Dr. John Doe",
    "title": "Professor"
}

result = exercitiul_5(rules, dictionary)
print("Ex.5: ", result)

dictionary_invalid = {
    "name": "John Doe", 
    "title": "Professor"
}

result = exercitiul_5(rules, dictionary_invalid)
print(result)

def exercitiul_6(lst):
    unique_elements = set(lst)
    total_elements = len(lst)
    unique_count = len(unique_elements)
    duplicate_count = total_elements - unique_count
    
    return unique_count, duplicate_count

lst = [1, 2, 2, 3, 4, 4, 5]
result = exercitiul_6(lst)
print("Ex.6: ", result)

def exercitiul_7(a, b):
    dict = {}
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
            reunion.append(i) 
            a_b.append(i)
    for i in b:
        reunion.append(i)
        notInIntersection = True
        for j in intersection:
            if i == j:
                notInIntersection = False
                break
        if notInIntersection == True:
            b_a.append(i)
    print("Ex.7: Result for a=[1, 2, 3, 5, 6, 7] and b=[3, 5, 6, 12]")
    dict[f"{a} | {b}"] = reunion
    dict[f"{a} & {b}"] = intersection
    dict[f"{a} - {b}"] = a_b
    dict[f"{b} - {a}"] = b_a
    print(dict)
# a=list(map(int,input("Enter numbers in list a: ").split()))
# b=list(map(int,input("Enter numbers in list b: ").split()))
# exercitiul_7(a,b)
exercitiul_7([1, 2, 3, 5, 6, 7], [3, 5, 6, 12])

def exercitiul_8(dict):
    visited = {} 
    for item in dict:
        visited[item] = 0
    current = "start"
    visited[current] = 1
    lst = []
    current = dict[current]
    while visited[current] != 1:
        lst.append(current)
        visited[current] = 1
        current = dict[current]
    return lst
result = exercitiul_8({'start': 'a', 'b': 'a', 'a': '6', '6': 'z', 'x': '2', 'z': '2', '2': '2', 'y': 'start'})
print(f"Ex.8: {result}")

def exercitiul_9(*args, **equals):
    count = 0
    equals_values = set(equals.values())
    for arg in args:
        if arg in equals_values:
            count += 1
    return count
print(f"Ex.9: {exercitiul_9(1, 2, 3, 4, x=1, y=2, z=3, w=5)}")