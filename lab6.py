import math
# Exercitiul 1
class Forma:
    def area(self):
        pass
    def perimeter(self):
        pass
class Square(Forma):
    def __init__(self, l):
        self.l = l
    def area(self):
        return self.l*self.l
    def perimeter(self):
        return self.l*4
class Circle(Forma):
    def __init__(self, radius):
        self.radius = radius
    def area(self):
        return math.pi * (self.radius ** 2)
    def perimeter(self):
        return 2 * math.pi * self.radius
class Rectangle(Forma):
    def __init__(self, l1, l2):
        self.l1 = l1
        self.l2 = l2
    def area(self):
        return self.l1*self.l2
    def perimeter(self):
        return self.l1 * 2 + self.l2 * 2

print("----Exercitiul 1:")
rectangle = Rectangle(4, 5)
print(f"Area of rectangle: {rectangle.area()}")
print(f"Perimeter of rectangle: {rectangle.perimeter()}")

circle = Circle(5)
print(f"Area of circle: {circle.area()}")
print(f"Perimeter of circle: {circle.perimeter()}")

# Exercitiul 2
class Account:
    def __init__(self, balance = 0):
        self.balance = balance
        self.transaction_history = []
    def deposit(self, amount): 
        if amount < 0:
            print("Amount must be positive")
        else: 
            self.balance += amount
            self.transaction_history.append(f"Deposited ${amount}")
    def withdrawal(self, amount):
        if amount > self.balance:
            print("Not enough funds")
            return False
        self.balance -= amount
        self.transaction_history.append(f"Withdrew ${amount}")
        print(f"Withdrew ${amount}. New balance: ${self.balance}")
        return True
class SavingAccount(Account):
    def __init__(self, balance=0, interest_rate=0.02):
        super().__init__( balance)
        self.interest_rate = interest_rate
    def calculate_interest(self):
        interest = self.balance * self.interest_rate
        print(f"Interest: ${interest}")
        self.deposit(interest)
        return interest
class CheckingAccount(Account):
    def __init__(self, balance=0, overdraft_limit=100):
        super().__init__(balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if amount > self.balance + self.overdraft_limit:
            print("Overdraft over limit!")
            return False
        self.balance -= amount
        print(f"Withdrew ${amount}. New balance: ${self.balance}")
        return True
print("----Exercitiul 2:")
savingA = SavingAccount(1056, 0.03)
savingA.calculate_interest()
checkingA = CheckingAccount(1000)
checkingA.withdraw(1020)
checkingA.withdraw(150)

# Exercitiul 3 
class Vehicle:
    def __init__(self, make, model, year):
        self.make = make
        self.model = model
        self.year = year
        self.maintenance_history = []

class Car(Vehicle):
    def __init__(self, make, model, year, mileage = 0):
        super().__init__(make, model, year)
        self.mileage = mileage
    def drive(self, km):
        self.mileage += km
    def get_mileage(self):
        print(f"Mileage: {self.mileage}")

class Motocycle(Vehicle):
    def __init__(self, make, model, year, mileage = 0):
        super().__init__(make, model, year)
        self.mileage = mileage
        self.isDriving = 0
    def drive(self, km):
        self.mileage += km
    def get_mileage(self):
        print(f"Mileage: {self.mileage}")

class Truck(Vehicle):
    def __init__(self, make, model, year, towing_capacity):
        super().__init__(make, model, year)
        self.towing_capacity = towing_capacity

    def load_weight(self, load_weight):
        if load_weight > self.towing_capacity:
            print(f"Over capacity: {self.towing_capacity} lbs.")
            return False
        print("Weight approved.")
        self.maintenance_history.append(f"Loaded {load_weight} lbs")
        return True
    def get_maintenance_history(self):
        return self.maintenance_history
print("----Exercitiul 3:")
car = Car("Dacia", "Logan", 2004)
motorcycle = Motocycle("Yamaha", "MT-09", 2021)
truck = Truck("Ford", "F-150", 2019, towing_capacity=10000)

car.drive(150)
car.get_mileage()

motorcycle.drive(75)
motorcycle.get_mileage()

truck.load_weight(8000)
truck.load_weight(12000)
print(truck.get_maintenance_history())

# Exercitiul 4
class Employee:
    def __init__(self, name, employee_id, salary):
        self.name = name
        self.employee_id = employee_id
        self.salary = salary

    def get_details(self):
        return f"Employee: {self.name}, ID: {self.employee_id}, Salary: ${self.salary}"

class Manager(Employee):
    def __init__(self, name, employee_id, salary, team_members=None):
        super().__init__(name, employee_id, salary)
        self.team_members = team_members if team_members else []

    def add_team_member(self, employee):
        self.team_members.append(employee)
        print(f"{self.name} added {employee.name} to their team.")

    def get_team(self):
        team_list = ", ".join([member.name for member in self.team_members])
        return f"Team of {self.name}: {team_list}"

class Engineer(Employee):
    def __init__(self, name, employee_id, salary, skills=None):
        super().__init__(name, employee_id, salary)
        self.skills = skills if skills else []

    def add_skill(self, skill):
        self.skills.append(skill)
        print(f"{self.name} knows this: {skill}.")
    def solve_problem(self, language):
        if language in self.skills:
            print(f"Problem in {language} solved.")
        else:
            print(f"{self.name} can't solve problems in {language}")

class Salesperson(Employee):
    def __init__(self, name, employee_id, salary, commission_rate=0.05):
        super().__init__(name, employee_id, salary)
        self.commission_rate = commission_rate

    def calculate_commission(self, sales_amount):
        commission = sales_amount * self.commission_rate
        print(f"{self.name} earned a commission of ${commission:.2f} from ${sales_amount} in sales.")
        return commission

    def annual_bonus(self, sales_amount):
        commission = self.calculate_commission(sales_amount)
        bonus = commission * 0.1
        print(f"{self.name} receives an annual bonus of ${bonus:.2f}.")
        return bonus

print("----Exercitiul 4:")
manager = Manager("Alice", 101, 95000)
engineer = Engineer("Bob", 102, 80000, ["Python"])
salesperson = Salesperson("Charlie", 103, 60000, commission_rate=0.07)

print(manager.get_details())
manager.add_team_member(engineer)
print(manager.get_team())

print(engineer.get_details())
engineer.add_skill("java")
engineer.solve_problem("c")
engineer.solve_problem("java")

print(salesperson.get_details())
salesperson.calculate_commission(20000)
salesperson.annual_bonus(20000)

# Exercitiul 5

class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def make_sound(self):
        return "The animal makes a sound."

    def eat(self):
        return f"{self.name} is eating."

    def sleep(self):
        return f"{self.name} is sleeping."

    def move(self):
        return f"{self.name} is moving around."

    def show_age(self):
        return f"{self.name} is {self.age} years old."

class Mammal(Animal):
    def __init__(self, name, age, fur_type):
        super().__init__(name, age)
        self.fur_type = fur_type 

    def groom(self):
        return f"{self.name} is grooming its fur."
    
    def make_sound(self):
        return f"{self.name} makes a mammal sound."

class Bird(Animal):
    def __init__(self, name, age, wing_span):
        super().__init__(name, age)
        self.wing_span = wing_span
    
    def fly(self):
        return f"{self.name} is flying."
    
    def make_sound(self):
        return f"{self.name} chirps."
    
    def nest(self):
        return f"{self.name} is building a nest."
    def calculate_speed(self):
        speed = self.wing_span * 1.5
        return f"{self.name}'s flying speed is {speed} km/h."

class Fish(Animal):
    def __init__(self, name, age, scale_type):
        super().__init__(name, age)
        self.scale_type = scale_type
    
    def swim(self):
        return f"{self.name} is swimming."
    
    def make_sound(self):
        return f"{self.name} says 'blop blop'."

print("----Exercitiul 5:")
leo = Mammal("Leo", 5, "short")
pigeon = Bird("Pigeon", 2, 30)
golden_fish = Fish("Golden Fish", 1, "smooth")

print(leo.eat())
print(leo.groom())
print(leo.make_sound())
print(leo.sleep())
print(leo.move())
print(leo.show_age())

print(pigeon.fly())
print(pigeon.make_sound())
print(pigeon.nest())
print(pigeon.calculate_speed())

print(golden_fish.swim())
print(golden_fish.make_sound())
print(golden_fish.sleep())

#Exercitiul 6

class LibraryItem:
    def __init__(self, title, creator, item_type):
        self.title = title
        self.creator = creator
        self.item_type = item_type
    
    def display_info(self):
        return f"Title: {self.title}\nCreator: {self.creator}\nType: {self.item_type}"

class Book(LibraryItem):
    def __init__(self, title, author):
        super().__init__(title, author, "Book")

    def display_info(self):
        basic_info = super().display_info()
        return f"{basic_info}\n"

class DVD(LibraryItem):
    def __init__(self, title, director, duration):
        super().__init__(title, director, "DVD")
        self.duration = duration
    
    def display_info(self):
        basic_info = super().display_info()
        return f"{basic_info}\nDuration: {self.duration} minutes"

class Magazine(LibraryItem):
    def __init__(self, title, editor, issue_number):
        super().__init__(title, editor, "Magazine")
        self.issue_number = issue_number
    
    def display_info(self):
        basic_info = super().display_info()
        return f"{basic_info}\nIssue Number: {self.issue_number}"

class Library:
    def __init__(self):
        self.items = []
        self.checked_out_items = {}

    def add_item(self, item):
        self.items.append(item)

    def check_out(self, item, borrower):
        if item not in self.checked_out_items:
            self.checked_out_items[item] = borrower
            return f"{borrower} has checked out {item.title}."
        else:
            return f"{item.title} is already checked out by {self.checked_out_items[item]}."
    
    def return_item(self, item):
        if item in self.checked_out_items:
            borrower = self.checked_out_items.pop(item)
            return f"{borrower} has returned {item.title}."
        else:
            return f"{item.title} was not checked out."

    def display_all_items(self):
        for item in self.items:
            print(item.display_info())
    
    def display_checked_out_items(self):
        if not self.checked_out_items:
            return "No items are currently checked out."
        for item, borrower in self.checked_out_items.items():
            print(f"{item.title} is checked out by {borrower}")

print("----Exercitiul 6:")
library = Library()

book1 = Book("And then there were none", "Agatha Christie")
dvd1 = DVD("Inception", "Christopher Nolan", 148)
magazine1 = Magazine("National Geographic", "Susan Goldberg", 789)

library.add_item(book1)
library.add_item(dvd1)
library.add_item(magazine1)

library.display_all_items()

print(library.check_out(book1, "Teodora"))
print(library.check_out(dvd1, "Maria"))
print(library.check_out(book1, "Stefania"))

print("\nChecked Out Items:")
library.display_checked_out_items()

print(library.return_item(book1))
print(library.return_item(book1))

print("\nChecked Out Items After Return:")
library.display_checked_out_items()