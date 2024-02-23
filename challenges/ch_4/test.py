

class Car:
    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity
        self.students = []

    def add_student(self, student):
        if len(self.students) < self.capacity:
            self.students.append(student)
        else:
            raise Exception("Car is full")
    
    def remove_student(self, student):
        if student in self.students:
            self.students.remove(student)
        else:
            raise Exception("Student not in car")

    def __str__(self):
        return f"{self.name}: {', '.join(self.students)}"
    
class Student:
    def __init__(self, name):
        self.name = name
        self.car = None
    
    def __str__(self):
        return self.name

    def is_comfy(self):
        return True
    


organize([Car("A", 2), Car("B", 2), Car("C", 2)], [Student("A"), Student("B"), Student("C"), Student("D"), Student("E"), Student("F")])