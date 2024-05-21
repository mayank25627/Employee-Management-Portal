from flask import Flask, render_template, request, redirect,  session
import bcrypt
import mysql.connector
from mysql.connector import Error
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)


def create_connection():
    """ Create a database connection """
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Mayank@123",
            database="employeeManagement"
        )
        return connection
    except Error as e:
        return None


def login_admin(email, password):
    con = create_connection()
    cursor = con.cursor()
    try:
        cursor.execute(
            "SELECT password FROM admin WHERE email = %s", (email,))
        result = cursor.fetchone()
        if result is None:
            return False

        stored_password = result[0].encode('utf-8')

        if bcrypt.checkpw(password.encode('utf-8'), stored_password):
            return True
        else:
            return False
    except Error as e:
        return False
    finally:
        cursor.close()
        con.close()


def login_employee(email, password):
    con = create_connection()
    if con is None:
        return False, None

    cursor = con.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT * FROM employee WHERE email = %s", (email,))
        result = cursor.fetchone()
        if result is None:
            return False, None

        stored_password = result['password'].encode('utf-8')

        if bcrypt.checkpw(password.encode('utf-8'), stored_password):
            return True, result
        else:
            return False, None
    except Error as e:
        return False, None
    finally:
        cursor.close()
        con.close()


def login_manager(email, password):
    con = create_connection()
    if con is None:
        return False, None

    cursor = con.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT * FROM manager WHERE email = %s", (email,))
        result = cursor.fetchone()
        if result is None:
            return False, None

        stored_password = result['password'].encode('utf-8')

        if bcrypt.checkpw(password.encode('utf-8'), stored_password):
            return True, result
        else:
            return False, None
    except Error as e:
        return False, None
    finally:
        cursor.close()
        con.close()


def addEmployee(first_name, last_name, email, phone_number, position, address, manager_id, password):
    connection = create_connection()
    if connection is None:
        return False

    cursor = connection.cursor()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        cursor.execute("""
            INSERT INTO employee (first_name, last_name, email, phone_number, position, address, manager_id, password)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (first_name, last_name, email, phone_number, position, address, manager_id, hashed_password))
        connection.commit()
        return True
    except Error as e:
        return False
    finally:
        cursor.close()
        connection.close()


def addManager(first_name, last_name, email, phone_number, password):
    connection = create_connection()
    if connection is None:
        return False

    cursor = connection.cursor()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        cursor.execute("""
            INSERT INTO manager (first_name, last_name, email, phone_number, password)
            VALUES (%s, %s, %s, %s, %s)
        """, (first_name, last_name, email, phone_number, hashed_password))
        connection.commit()
        return True
    except Error as e:
        return False
    finally:
        cursor.close()
        connection.close()


def addProjects(project_name, description):
    connection = create_connection()
    if connection is None:
        return False

    cursor = connection.cursor()

    try:
        cursor.execute("""
            INSERT INTO project (project_name, description)
            VALUES (%s, %s)
        """, (project_name, description))
        connection.commit()
        return True
    except Error as e:
        return False
    finally:
        cursor.close()
        connection.close()


def viewEmployee():
    con = create_connection()
    if con is None:
        return False, None

    cursor = con.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM employee")
        result = cursor.fetchall()
        if not result:
            return False, None
        else:
            return True, result
    except Error as e:
        return False, None
    finally:
        cursor.close()
        con.close()


def viewManager():
    con = create_connection()
    if con is None:
        return False, None

    cursor = con.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM manager")
        result = cursor.fetchall()
        if not result:
            return False, None
        else:
            return True, result
    except Error as e:
        return False, None
    finally:
        cursor.close()
        con.close()


def viewProject():
    con = create_connection()
    if con is None:
        return False, None

    cursor = con.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM project")
        result = cursor.fetchall()
        if not result:
            return False, None
        else:
            return True, result
    except Error as e:
        return False, None
    finally:
        cursor.close()
        con.close()


def get_unassigned_employees():
    con = create_connection()
    if con is None:
        return []
    cursor = con.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT employee_id, first_name, last_name 
            FROM Employee 
            WHERE employee_id NOT IN (SELECT employee_id FROM EmployeeProject)
        """)
        return cursor.fetchall()
    except Error as e:
        return []
    finally:
        cursor.close()
        con.close()


def get_assigned_employees():
    con = create_connection()
    if con is None:
        return []
    cursor = con.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT e.employee_id, e.first_name, e.last_name, p.project_id, p.project_name 
            FROM Employee e 
            JOIN EmployeeProject ep ON e.employee_id = ep.employee_id 
            JOIN Project p ON ep.project_id = p.project_id
        """)
        return cursor.fetchall()
    except Error as e:
        return []
    finally:
        cursor.close()
        con.close()


def get_all_projects():
    con = create_connection()
    if con is None:
        return []
    cursor = con.cursor(dictionary=True)
    try:
        cursor.execute("SELECT project_id, project_name FROM Project")
        return cursor.fetchall()
    except Error as e:
        return []
    finally:
        cursor.close()
        con.close()


def viewEmployeesWithProjects():
    con = create_connection()
    if con is None:
        return False, None

    cursor = con.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT e.employee_id, e.first_name, e.last_name, p.project_name
            FROM Employee e
            LEFT JOIN EmployeeProject ep ON e.employee_id = ep.employee_id
            LEFT JOIN Project p ON ep.project_id = p.project_id
        """)
        result = cursor.fetchall()
        if not result:
            return False, None
        else:
            return True, result
    except Error as e:
        return False, None
    finally:
        cursor.close()
        con.close()


@app.route('/')
def index():
    return render_template('index.html')


# Admin routes --------------------------------

@app.route('/adminlogin')
def adminlogin():
    return render_template('adminlogin.html')


@app.route('/adminpage')
def adminpage():
    return render_template('adminpage.html')


@app.route('/adminloginprocess', methods=['POST'])
def adminloginprocess():
    email = request.form['email']
    password = request.form['password']

    output = login_admin(email, password)
    failedtext = 'Please login with correct email and password'

    if output is True:
        return render_template('adminpage.html')
    else:
        return render_template('adminlogin.html', failedtext=failedtext)


@app.route('/addEmployeePage')
def addEmployeePage():
    return render_template('addemployee.html')


@app.route('/addemployees', methods=['GET', 'POST'])
def addemployees():
    firstname = request.form['first-name']
    lastname = request.form['last-name']
    email = request.form['email']
    phone = request.form['phone-number']
    position = request.form['position']
    address = request.form['address']
    manager = request.form['manager-id']
    password = request.form['password']

    ifAddSucess = addEmployee(firstname, lastname, email, phone,
                              position, address, manager, password)

    if ifAddSucess == True:
        sucessMessage = 'Sucessfull added employee', firstname
        return render_template('addemployee.html', sucessMessage=sucessMessage)
    else:
        failmessage = 'Please add employee again!'
        return render_template('addemployee.html', failmessage=failmessage)


@app.route('/addManagerPage')
def addManagerPage():
    return render_template('addmanager.html')


@app.route('/addmanagers', methods=['GET', 'POST'])
def addmanagers():
    firstname = request.form['first-name']
    lastname = request.form['last-name']
    email = request.form['email']
    phone = request.form['phone-number']
    password = request.form['password']

    ifAddSucess = addManager(firstname, lastname, email, phone, password)

    if ifAddSucess == True:
        sucessMessage = 'Sucessfull added Manager ', firstname
        return render_template('addmanager.html', sucessMessage=sucessMessage)
    else:
        failmessage = 'Please add Manager again! '
        return render_template('addmanager.html', failmessage=failmessage)


@app.route('/addProjectPage')
def addProjectPage():
    return render_template('addproject.html')


@app.route('/addprojects',  methods=['GET', 'POST'])
def addprojects():
    project_name = request.form['project-name']
    description = request.form['description']

    ifAddSucess = addProjects(project_name, description)

    if ifAddSucess == True:
        sucessMessage = 'Sucessfull added Project ', project_name
        return render_template('addproject.html', sucessMessage=sucessMessage)
    else:
        failmessage = 'Error Please add Project again! '
        return render_template('addproject.html', failmessage=failmessage)


@app.route('/viewEmployeePage')
def viewEmployeePage():
    success, employees = viewEmployee()
    if success:
        return render_template('viewemployee.html', employees=employees)
    else:
        return render_template('viewemployee.html', error="No employees found or an error occurred.")


@app.route('/updateEmployee/<int:employee_id>', methods=['GET', 'POST'])
def update_employee(employee_id):
    con = create_connection()
    if con is None:
        return "Connection to the database failed.", 500

    cursor = con.cursor(dictionary=True)
    if request.method == 'POST':
        first_name = request.form['first-name']
        last_name = request.form['last-name']
        email = request.form['email']
        phone_number = request.form['phone-number']
        position = request.form['position']
        address = request.form['address']
        manager_id = request.form['manager-id']

        try:
            cursor.execute("""
                UPDATE employee 
                SET first_name = %s, last_name = %s, email = %s, phone_number = %s, position = %s, address = %s, manager_id = %s
                WHERE employee_id = %s
            """, (first_name, last_name, email, phone_number, position, address, manager_id, employee_id))
            con.commit()
            return redirect('/viewEmployeePage')
        except Error as e:
            return "Update failed.", 500
        finally:
            cursor.close()
            con.close()
    else:
        cursor.execute(
            "SELECT * FROM employee WHERE employee_id = %s", (employee_id,))
        employee = cursor.fetchone()
        if employee is None:
            return "Employee not found.", 404
        return render_template('update_employee.html', employee=employee)


@app.route('/deleteEmployee/<int:employee_id>')
def delete_employee(employee_id):
    con = create_connection()
    if con is None:
        return "Connection to the database failed.", 500

    cursor = con.cursor()
    try:
        cursor.execute(
            "DELETE FROM employee WHERE employee_id = %s", (employee_id,))
        con.commit()
        return redirect('/viewEmployeePage')
    except Error as e:
        return "Delete failed.", 500
    finally:
        cursor.close()
        con.close()


@app.route('/viewProjectPage')
def viewProjectPage():
    success, project = viewProject()
    if success:
        return render_template('viewproject.html', project=project)
    else:
        return render_template('viewproject.html', error="No employees found or an error occurred.")


@app.route('/updateProject/<int:project_id>', methods=['GET'])
def showUpdateProjectForm(project_id):
    con = create_connection()
    if con is None:
        return render_template('update_project.html', error="Could not connect to the database.")

    cursor = con.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT * FROM project WHERE project_id = %s", (project_id,))
        project = cursor.fetchone()
        if project is None:
            return render_template('update_project.html', error="Project not found.")
        else:
            return render_template('update_project.html', project=project)
    except Error as e:
        return render_template('update_project.html', error="An error occurred.")
    finally:
        cursor.close()
        con.close()


@app.route('/updateProject/<int:project_id>', methods=['POST'])
def updateProject(project_id):
    project_name = request.form['project_name']
    description = request.form['description']

    con = create_connection()
    if con is None:
        return render_template('update_project.html', error="Could not connect to the database.")

    cursor = con.cursor()
    try:
        cursor.execute(
            "UPDATE project SET project_name = %s, description = %s WHERE project_id = %s",
            (project_name, description, project_id)
        )
        con.commit()
        return redirect('/viewProjectPage')
    except Error as e:
        return render_template('update_project.html', error="An error occurred while updating the project.", project={"project_id": project_id, "project_name": project_name, "description": description})
    finally:
        cursor.close()
        con.close()


@app.route('/deleteProject/<int:project_id>')
def delete_project(project_id):
    con = create_connection()
    if con is None:
        return "Connection to the database failed.", 500

    cursor = con.cursor()
    try:
        cursor.execute(
            "DELETE FROM project WHERE project_id = %s", (project_id,))
        con.commit()
        return redirect('/viewProjectPage')
    except Error as e:
        return "Delete failed.", 500
    finally:
        cursor.close()
        con.close()


@app.route('/viewManagers')
def view_managers():
    con = create_connection()
    if con is None:
        return render_template('viewmanagers.html', error="Could not connect to the database.")

    cursor = con.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM manager")
        managers = cursor.fetchall()
        return render_template('viewmanagers.html', managers=managers)
    except Error as e:
        return render_template('viewmanagers.html', error="An error occurred while fetching managers.")
    finally:
        cursor.close()
        con.close()


@app.route('/updateManager/<int:manager_id>', methods=['GET', 'POST'])
def update_manager(manager_id):
    if request.method == 'GET':
        con = create_connection()
        if con is None:
            return render_template('updatemanager.html', error="Could not connect to the database.")

        cursor = con.cursor(dictionary=True)
        try:
            cursor.execute(
                "SELECT * FROM manager WHERE manager_id = %s", (manager_id,))
            manager = cursor.fetchone()
            if not manager:
                return render_template('updatemanager.html', error="Manager not found.")
            return render_template('updatemanager.html', manager=manager)
        except Error as e:
            return render_template('updatemanager.html', error="An error occurred while fetching the manager.")
        finally:
            cursor.close()
            con.close()
    else:
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        phone_number = request.form['phone_number']

        con = create_connection()
        if con is None:
            return render_template('updatemanager.html', error="Could not connect to the database.")

        cursor = con.cursor()
        try:
            cursor.execute("""
                UPDATE manager 
                SET first_name = %s, last_name = %s, email = %s, phone_number = %s
                WHERE manager_id = %s
            """, (first_name, last_name, email, phone_number, manager_id))
            con.commit()
            return redirect('/viewManagers')
        except Error as e:
            return render_template('updatemanager.html', error="An error occurred while updating the manager.")
        finally:
            cursor.close()
            con.close()


@app.route('/deleteManager/<int:manager_id>', methods=['POST', 'GET'])
def delete_manager(manager_id):
    con = create_connection()
    if con is None:
        return redirect('/viewManagers', error="Could not connect to the database.")

    cursor = con.cursor()
    try:
        cursor.execute(
            "DELETE FROM manager WHERE manager_id = %s", (manager_id,))
        con.commit()
        return redirect('/viewManagers')
    except Error as e:
        return redirect('/viewManagers', error="An error occurred while deleting the manager.")
    finally:
        cursor.close()
        con.close()


@app.route('/assignProjectPage')
def assignProjectPage():
    unassigned_employees = get_unassigned_employees()
    projects = get_all_projects()
    return render_template('assign_project.html', unassigned_employees=unassigned_employees, projects=projects)


@app.route('/assignProject', methods=['POST'])
def assignProject():
    employee_id = request.form['employee_id']
    project_id = request.form['project_id']

    con = create_connection()
    if con is None:
        return render_template('assign_project.html', error="Could not connect to the database.", unassigned_employees=get_unassigned_employees(), projects=get_all_projects())

    cursor = con.cursor()
    try:
        cursor.execute(
            "INSERT INTO EmployeeProject (employee_id, project_id) VALUES (%s, %s)", (employee_id, project_id))
        con.commit()
        return redirect('/assignProjectPage')
    except Error as e:
        return render_template('assign_project.html', error="An error occurred while assigning the project.", unassigned_employees=get_unassigned_employees(), projects=get_all_projects())
    finally:
        cursor.close()
        con.close()


@app.route('/unassignProjectPage')
def unassignProjectPage():
    assigned_employees = get_assigned_employees()
    return render_template('unassign_project.html', assigned_employees=assigned_employees)


@app.route('/unassignProject', methods=['POST'])
def unassignProject():
    employee_id = request.form['employee_id']

    con = create_connection()
    if con is None:
        return render_template('unassign_project.html', error="Could not connect to the database.", assigned_employees=get_assigned_employees())

    cursor = con.cursor()
    try:
        cursor.execute(
            "DELETE FROM EmployeeProject WHERE employee_id = %s", (employee_id,))
        con.commit()
        return redirect('/unassignProjectPage')
    except Error as e:
        return render_template('unassign_project.html', error="An error occurred while unassigning the project.", assigned_employees=get_assigned_employees())
    finally:
        cursor.close()
        con.close()


@app.route('/viewEmployeesWithProjects')
def viewEmployeesWithProjectsPage():
    success, employees = viewEmployeesWithProjects()
    if success:
        return render_template('employee_with_project.html', employees=employees)
    else:
        return render_template('employee_with_project.html', error="No employees found or an error occurred.")


# Employee Routes --------------------------------

@app.route('/emplogin')
def emplogin():
    return render_template('emplogin.html')


@app.route('/employeeloginprocess', methods=['GET', 'POST'])
def employeeloginprocess():
    email = request.form['email']
    password = request.form['password']

    is_authenticated, employee_data = login_employee(email, password)
    failedtext = 'Please login with correct email and password'

    if is_authenticated:
        session['employee'] = employee_data
        return redirect('/employeepage')
    else:
        return render_template('emplogin.html', failedtext=failedtext)


@app.route('/employeepage')
def employeepage():
    employee = session.get('employee')
    if not employee:
        return redirect('/emplogin')

    return render_template('employeepage.html', employee=employee)


@app.route('/showDetails')
def show_details():
    employee = session.get('employee')
    if not employee:
        return redirect('/emplogin')

    con = create_connection()
    if con is None:
        return render_template('showdetails.html', error="Could not connect to the database.")

    cursor = con.cursor(dictionary=True)
    try:
        # Fetch assigned project details
        cursor.execute("""
            SELECT project.project_id, project.project_name
            FROM EmployeeProject
            JOIN project ON EmployeeProject.project_id = project.project_id
            WHERE EmployeeProject.employee_id = %s
        """, (employee['employee_id'],))
        project = cursor.fetchone()

        # Fetch assigned manager details
        cursor.execute("""
            SELECT first_name, last_name
            FROM manager
            WHERE manager_id = %s
        """, (employee['manager_id'],))
        manager = cursor.fetchone()

        return render_template('showdetails.html', employee=employee, project=project, manager=manager)
    except Error as e:
        return render_template('showdetails.html', error="An error occurred while fetching details.")
    finally:
        cursor.close()
        con.close()

# @app.route('/showDetails')
# def show_details():
    employee = session.get('employee')
    if not employee:
        return redirect('/emplogin')

    con = create_connection()
    if con is None:
        return render_template('showdetails.html', error="Could not connect to the database.")

    cursor = con.cursor(dictionary=True)
    try:
        # Fetch assigned project details
        cursor.execute("""
            SELECT project.project_id, project.project_name
            FROM EmployeeProject
            JOIN project ON EmployeeProject.project_id = project.project_id
            WHERE EmployeeProject.employee_id = %s
        """, (employee['employee_id'],))
        project = cursor.fetchone()

        # Fetch assigned manager details
        cursor.execute("""
            SELECT first_name, last_name
            FROM manager
            WHERE manager_id = %s
        """, (employee['manager_id'],))
        manager = cursor.fetchone()

        return render_template('showdetails.html', employee=employee, project=project, manager=manager)
    except Error as e:
        return render_template('showdetails.html', error="An error occurred while fetching details.")
    finally:
        cursor.close()
        con.close()


@app.route('/addskills', methods=['POST'])
def addskills():
    employee = session.get('employee')
    if not employee:
        return redirect('/emplogin')

    skill_name = request.form['skill_name']
    proficiency_level = request.form['proficiency_level']

    con = create_connection()
    if con is None:
        return render_template('updateskills.html', error="Could not connect to the database.")

    cursor = con.cursor()
    try:
        cursor.execute("INSERT INTO employeeskills (employee_id, skill_name, proficiency_level) VALUES (%s, %s, %s)",
                       (employee['employee_id'], skill_name, proficiency_level))
        con.commit()
        return redirect('/updateskills')
    except Error as e:
        return render_template('updateskills.html', error="An error occurred while adding the skill.")
    finally:
        cursor.close()
        con.close()


@app.route('/updateskills', methods=['GET'])
def updateskills():
    employee = session.get('employee')
    if not employee:
        return redirect('/emplogin')

    con = create_connection()
    if con is None:
        return render_template('updateskills.html', error="Could not connect to the database.")

    cursor = con.cursor(dictionary=True)
    try:
        cursor.execute(
            "SELECT * FROM employeeskills WHERE employee_id = %s", (employee['employee_id'],))
        skills = cursor.fetchall()
        return render_template('updateskills.html', skills=skills)
    except Error as e:
        return render_template('updateskills.html', error="An error occurred while fetching skills.")
    finally:
        cursor.close()
        con.close()


@app.route('/viewEmployeePagetoEmployee')
def viewEmployeePagetoEmployee():
    success, employees = viewEmployee()
    if success:
        return render_template('viewemployeetoemployee.html', employees=employees)
    else:
        return render_template('viewemployeetoemployee.html', error="No employees found or an error occurred.")


@app.route('/viewManagerPagetoEmployee')
def viewManagerPagetoEmployee():
    success, managers = viewManager()
    if success:
        return render_template('viewmanagertoemployee.html', managers=managers)
    else:
        return render_template('viewmanagertoemployee.html', error="No employees found or an error occurred.")


# Manager Routes --------------------------------


@app.route('/mnglogin')
def mnglogin():
    return render_template('mnglogin.html')


@app.route('/managerloginprocess', methods=['GET', 'POST'])
def manager_page():
    email = request.form['email']
    password = request.form['password']

    is_authenticated, manager_data = login_manager(email, password)
    failedtext = 'Please login with correct email and password'

    if is_authenticated:
        session['manager'] = manager_data
        manager = session['manager']

        return render_template('managerpage.html', manager=manager)
    else:
        return render_template('mnglogin.html', failedtext=failedtext)


if __name__ == "__main__":
    app.run(debug=True)
