# exercitiul 1
def cmmdc(a,b):
    while b>0:
        r=a%b
        a=b
        b=r
    return a
def exercitiul_1(numbers):
    cmmdc_curent = numbers[0]
    for num in numbers[1:]:
        cmmdc_curent = cmmdc(cmmdc_curent, num)
    return cmmdc_curent
numbers=list(map(int,input("Enter numbers for cmmdc:").split()))
cmmdc_rezultat=exercitiul_1(numbers)
print(f"Answer: {cmmdc_rezultat}")

# exercitiul 2
def isVowel(ch): 
    vowels = "aeiouAEIOU"
    return ch in vowels
def exercitiul_2(s):
    count = 0
    for ch in s:
        if isVowel(ch)==1:
            count+=1
    return count
s=input("Enter a string to count vowels: ")

print(f"{exercitiul_2(s)}")

# exercitiul 3
first_string = input("Enter the substring to count: ")
second_string = input("Enter where to search: ")
def exercitiul_3(first_string, second_string):
    occurrences = second_string.count(first_string)
    return occurrences
print(f"The string '{first_string}' occurs {exercitiul_3(first_string, second_string)} times in '{second_string}'.")

#exercitiul 4
s = input("Enter an UpperCamelCase string: ")
def exercitiul_4(s):
    s = s.replace(s[0], s[0].lower(), 1)
    for ch in s[1:]: 
        if ch.isupper():
            s = s.replace(ch, f"_{ch.lower()}", 1) 
    return s
print(f"{exercitiul_4(s)}")

# exercitiul 5
def exercitiul_5(number):
    if number%10 == 0 and number != 0:
        return 0
    if number < 10:
        return 1
    copy = number
    palindrom = 0
    while copy != 0:
        c = copy%10
        palindrom = palindrom * 10 + c
        copy //= 10
    if palindrom == number:
        return 1
    else:
        return 0    
number=int(input("Enter number to check if it's palindrom: "))
if exercitiul_5(number) == 1:
    print("Number is palindrom")
else:
    print("Number isn't palindrom")

# exercitiul 6
s=input("Enter string to find the first number: ")
def exercitiul_6(s):
    found = 0
    numberString = []
    for ch in s:
        if ch.isnumeric():
            numberString.append(ch)
            found = 1
        else:
            if found == 1:
                break
    numberString = ''.join(numberString)
    return numberString
print(f"{exercitiul_6(s)}")

# exercitiul 7
number=int(input("Enter number to count the '1' bytes: "))
def exercitiul_7(number):
    count = 0
    while number !=0:
        if number % 2 == 1: 
            count+=1
        number //= 2
    return count
print(f"Answer: {exercitiul_7(number)}")

# exercitiul 8
def exercitiul_8(text):
    words = text.strip().split(' ')
    word_count = len([word for word in words if word])
    return word_count

text = input("Enter text to count words: ")
result = exercitiul_8(text)
print(f"Answer: {result}")
