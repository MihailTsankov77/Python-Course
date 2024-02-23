import unittest
from car_bubble_sort import organize

class Named:
    """Assign a name to instances of child classes."""

    _instances = {}

    def __new__(cls, *args, **kwargs):
        """Store numbers instances and assign names based on it."""
        instance = super().__new__(cls)
        cls._instances[cls] = cls._instances.setdefault(cls, 0) + 1
        instance.name = f'{cls.__name__} {cls._instances[cls]}'
        return instance


class Car(Named):
    """A car for the task."""

    CAPACITY = 4

    def __init__(self, cold=None):
        """Initializator."""
        self.cold = cold
        self.students = set()

    def add_student(self, student):
        """Add a student to a car and set the current car in student's fields."""
        if len(self.students) == self.CAPACITY:
            raise EnvironmentError('Car is full')
        # print(f'Putting {student} in {self}')
        self.students.add(student)
        student.set_car(self)

    def remove_student(self, student):
        """Remove a student from a car and unset the current car in student's fields."""
        if student not in self.students:
            raise EnvironmentError('Student is not in the car.')
        # print(f'Removing {student} from {self}')
        self.students.remove(student)
        student.unset_car()

    def __repr__(self):
        """Pretty print."""
        return self.name + " in " + str(len(self.students))


class Student(Named):
    """Student for the task."""

    def __init__(self, smoke=None, chalga=None, cold=None):
        """Initializator."""
        self.smoke = smoke
        self.chalga = chalga
        self.cold = cold
        self.car = None

    def set_car(self, car):
        """Set a car for this student."""
        self.car = car

    def unset_car(self):
        """Unset a car for this student."""
        self.car = None

    def is_comfy(self):
        """Check if student is comfy in their current car."""
        if self.car is None:
            return None
        if self.car.cold and self.cold is False:
            return False
        for student in self.car.students:
            if student is self:
                continue
            if student.smoke and self.smoke is False:
                return False
            if student.chalga and self.chalga is False:
                return False
        return True

    def __repr__(self):
        """Pretty print."""
        return self.name

class OrganizeTest(unittest.TestCase):
    def test_more_people_than_cars(self):
        cars = [Car()]
        students = [Student(), Student(), Student(), Student(), Student()]
        self.assertFalse(organize(cars, students))

    
    def test_possible_configuration(self):
        cars = [Car(True), Car()]
        students = [Student(True, True, True), Student(True, True, True), Student(), Student()]
        self.assertTrue(organize(cars, students))

    
    def test_possible_configuration_2(self):
        cars = [Car(), Car()]
        students = [Student(), Student(), Student(), Student(), Student(), Student()]
        self.assertTrue(organize(cars, students))


    def test_possible_configuration_3(self):
        cars1 = [Car(True), Car(True),  Car(True),  Car(),  Car()]
        cars2 = [Car(True), Car(),  Car(True),  Car(),  Car(True)]
        cars3 = [Car(), Car(True),  Car(True),  Car(True),  Car()]
        cars4 = [Car(True), Car(True),  Car(),  Car(True),  Car()]

#smoke chalga cold
        students = [Student(True, True, False), 
                    Student(True, True, False), 
                    Student(True, True, False), 
                    Student(True, True, False), 
                    Student(True, True, False), 
                    Student(True, True, False), 
                    Student(True, True, False)]
        
        self.assertTrue(organize(cars1, students))
        self.assertTrue(organize(cars2, students))
        self.assertTrue(organize(cars3, students))
        self.assertTrue(organize(cars4, students))

    
    def test_possible_configuration_4(self):
        cars1 = [Car(False), Car(False),  Car(False),  Car(True),  Car(False)]

        students = [Student(True, True, True), 
                    Student(True, True, False), 
                    Student(True, False, False), 
                    Student(False, True, False), 
                    Student(False, False, False)]
        
        self.assertTrue(organize(cars1, students))


    def test_possible_configuration_5(self):
        cars = [Car(), Car()]
        students = [Student(), Student(), Student(), Student(), Student(), Student(), Student(), Student()]	
        self.assertTrue(organize(cars, students))


    def test_possible_configuration_6(self):
        cars = [Car(False), Car(True)]
        students = [Student(True, True, False), 
                    Student(False, True, True), 
                    Student(True, True, False), 
                    Student(False, True, True), 
                    Student(True, True, False), 
                    Student(False, True, True), 
                    Student(False, True, True), 
                    Student(True, True, False)]	
        self.assertTrue(organize(cars, students))

    
    def test_impossible_configuration(self):
        cars = [Car(), Car()]
        students = [Student(True), 
                    Student(True), 
                    Student(True), 
                    Student(True), 
                    Student(True), 
                    Student(False), 
                    Student(False), 
                    Student(False)]
        self.assertFalse(organize(cars, students))
    
    def test_impossible_configuration_2(self):
        cars = [Car(True), Car(True)]
        students = [Student(True, True, False), 
                    Student(True, True, False), 
                    Student(True, True, False), 
                    Student(True, True, False), 
                    Student(True, True, False), 
                    Student(True, True, False), 
                    Student(True, True, False), 
                    Student(True, True, False)]
        self.assertFalse(organize(cars, students))
    
    def test_impossible_configuration_3(self):
        cars = [Car(True), Car()]
        students = [Student(True, True, False), 
                    Student(False, True, True), 
                    Student(True, True, False), 
                    Student(False, True, True), 
                    Student(True, True, False), 
                    Student(False, True, True), 
                    Student(False, False, True), 
                    Student(True, True, False)]
        self.assertFalse(organize(cars, students))

    def test_impossible_configuration_4(self):
        cars = [Car(True), Car(True), Car(True), Car()]
        students = [Student(True, True, False), 
                    Student(True, True, False), 
                    Student(True, True, False), 
                    Student(True, True, False), 
                    Student(True, True, False)]
        self.assertFalse(organize(cars, students))
    
    def test_impossible_configuration_5(self):
        cars = [Car(True), Car()]
        students = [Student(True, True, True), 
                    Student(True, True, True),
                    Student(True, False, False), 
                    Student(True, False, True), 
                    Student(True, False, True), 
                    Student(True, True, True), 
                    Student(True, True, True), 
                    Student(True, True, True)]
        self.assertFalse(organize(cars, students))
   
