from employee import Employee
import sqlite3


def insert_data(emp):
    if allowed_emp_id(emp.emp_id) is None:

        with conn:
            c.execute("INSERT INTO employee VALUES(:emp_id,:name,:lname,:age,:salary,:position,:email)"
                      , {"emp_id": emp.emp_id, "name": emp.name, "lname": emp.lname, "age": emp.age,
                         "salary": emp.salary, "position": emp.position, "email": emp.email})
            conn.commit()
        return 1, f"New employee has been added successfully with Employee ID:<b style='color:#32CD32'> {emp.emp_id} </b>"
    else:
        return 0, "Employee ID already exists"
        
        
def allowed_emp_id(emp_id):
    c.execute("SELECT * FROM employee WHERE emp_id=:emp_id", {"emp_id": emp_id})
    return c.fetchone()


def create_employee_object(emp_id, emp_name, emp_lname, emp_age, emp_salary, emp_pos, emp_email):
    e = Employee(emp_id, emp_name, emp_lname, emp_age, emp_salary, emp_pos, emp_email)
    return e


def fake_data(): 
    import random
    e = Employee(str(random.choice(range(100,999)))+'An'+str(random.choice(range(100,999)))+'Do'+str(random.choice(range(10,99))), 'Andy', 'Doe', 25, 10000, 'Manager', 'Andy.Doe.manager@gmail.com')
    insert_data(e)
    names = ["Andy", "Robert", "William", "Linda", "Christopher", "Betty", "Julie", "Frank", "Gary", "Paul",
             "Donald", "Jessica", "Andrew", "Megan", "Elizabeth", "Andres", "John", "Judy", "Mary", "Michael",
             "Sara", "Penny", "Andrew", "Mike", "Suzan", "Henry", "Shiva", "Evelyn", "Gloria", "Joe", "Billy", "Albert",
             "Rose", "Charlotte", "Bobby", "Johnny", "Eugene", "Diana"]
    lnames = ["Doe", "Jackson", "Anderson", "Silva", "Henderson", 'Defoe', "Terry",
              "Miller", "Hamilton", "Kennedy", "Owen", "Hazard", "Hernandez",
              "Davis", "Puma", "Page", "Robertson", "Martin", "Anderson", "Lee", "Lewis", "Wright",
              "Green", "Carter", "Flores", "Hill", "Walker", "Young", "King", "White", "Moore", "Gonzalez", "Smith"]
    positions = ["Employee", "Seller", 'Supervisor']

    for i in range(2, 41):
        pos = random.choices(positions, weights=[0.9, 0.1, 0.1])[0]
        name = random.choice(names)
        lname = random.choice(lnames)
        if pos == "Supervisor":
            e = Employee(str(random.choice(range(100,999)))+name[:2]+str(random.choice(range(100,999)))+lname[:2]+str(random.choice(range(10,99))), name, lname, random.choice(range(18, 65)), random.choice(range(5000, 7000)), pos,
                         f"{name}.{lname}@email.com")
            insert_data(e)
        else:
            e = Employee(str(random.choice(range(100,999)))+name[:2]+str(random.choice(range(100,999)))+lname[:2]+str(random.choice(range(10,99))), name, lname, random.choice(range(18, 65)), random.choice(range(500, 1500)),
                         pos, f"{name}.{lname}@email.com")
            insert_data(e)
        

def display_table():
    c.execute("SELECT * FROM employee")
    return c.fetchall()


def search_employee(search, search_field='name'):
    # print(search_field,search)
    c.execute("""SELECT * FROM employee WHERE ({}) LIKE ('%' || ? || '%') """.format(search_field), (search,))
    
    return c.fetchall()


def total_salary():
    c.execute("""SELECT position,SUM(salary) FROM employee GROUP BY position """)
    return c.fetchall()


def number_of_employee():
    c.execute("""SELECT position,COUNT(position) FROM employee GROUP BY position """)
    return c.fetchall()


def avg_salary_per_pos():
    c.execute("""SELECT position,ROUND(AVG(salary),2) FROM employee GROUP BY position """)
    return c.fetchall()


def update_employee(changing_field, new_value, emp_id):
    """
    update a field by a new value 
    example: update_employee('name','Helen',0)
    """
    # print(changing_field,new_value,emp_id)
    with conn:
        c.execute("""UPDATE employee set ({})=?  WHERE emp_id=? """.format(changing_field), (new_value, emp_id))
    conn.commit()


def delete_employee(del_value, del_field='emp_id'):
    """
    update a field by a new value 
    example: delete_employee(0)
    or delete_employee('Doe','lname')
    """
    with conn:
        c.execute("""DELETE FROM employee WHERE ({})=? """.format(del_field), (del_value,))
        conn.commit()


conn = sqlite3.connect(':memory:')
c = conn.cursor()

c.execute(""" CREATE TABLE employee(
emp_id PRIMARY KEY,
name VARCHAR(50),
lname VARCHAR(50),
age INTEGER,
salary INTEGER,
position VARCHAR(50),
email VARCHAR(100)
)
""")

# fake_data()
# print(display_table())
# print(allowed_emp_id(45) is  None)
# update_employee('emp_id',2,1)


if __name__ == "__main__":
    conn.close()
