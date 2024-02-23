from itertools import permutations

def set_partitions(collection):
    """Function gifted by a wise wizard."""
    if len(collection) == 1:
        yield [collection]
        return
    
    first = collection[0]
    for smaller in set_partitions(collection[1:]):
        for n, subset in enumerate(smaller):
            yield smaller[:n] + [[ first ] + subset]  + smaller[n+1:]
        yield [[first]] + smaller


def organize(cars, students):
    if len(students) > len(cars) * 4:
        return False
    
    def filter_students_sets(students_set):
        if len(students_set) > len(cars):
            return False
        for students in students_set:
            if len(students) > 4:
                return False
        return True
    
    def fix_students_sets(student_set):
        if len(student_set) < len(cars):
            for _ in range(len(cars) - len(student_set)):
                student_set.append([])
        return student_set
  
    students_partitons_sets = list(map(fix_students_sets,filter(filter_students_sets, set_partitions(students))))
    
    for car_permutation in permutations(cars):
        for students_permutation in students_partitons_sets:
            for car, students_set in zip(car_permutation, students_permutation):
                for student in students_set:
                    car.add_student(student)
            if all(student.is_comfy() for student in students):
                return True
            for car, students_set in zip(car_permutation, students_permutation):
                for student in students_set:
                    car.remove_student(student)
    return False
