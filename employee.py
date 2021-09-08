class Employee:
    
    def __init__(self, emp_id, name, lname, age, salary, position, email):
        self.emp_id = emp_id
        self.name = name
        self.lname = lname
        self.age = self.validate_age(age)
        self.salary = salary
        self.position = position
        self.email = email

    def validate_age(self, age):
        if age < 18 or age > 70:
            raise TypeError("The age is not appropriate\n18<Age<70")
        return age
        
    def __repr__(self):
        return f"{self.name} {self.lname}"


if __name__ == "__main__":
    print(__file__)