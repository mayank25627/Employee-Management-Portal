from flask import Flask, render_template, request, redirect,  session, jsonify
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


def get_unassigned_employees_with_skills():
    con = create_connection()
    if con is None:
        return []
    cursor = con.cursor(dictionary=True)
    try:
        cursor.execute("""
            SELECT e.employee_id, e.first_name, e.last_name,
                   GROUP_CONCAT(s.skill_name SEPARATOR ', ') AS skills
            FROM Employee e
            LEFT JOIN employeeskills s ON e.employee_id = s.employee_id
            WHERE e.employee_id NOT IN (SELECT employee_id FROM EmployeeProject)
            GROUP BY e.employee_id, e.first_name, e.last_name
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


def get_managers():
    connection = create_connection()
    if connection is None:
        print("Failed to connect to the database")
        return []

    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT manager_id, first_name, last_name FROM manager")
        managers = cursor.fetchall()
        return managers
    except Error as e:
        return []
    finally:
        cursor.close()
        connection.close()


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


def make_request(selected_employee_ids, project_id, request_text, manager_id):
    try:
        connection = create_connection()
        cursor = connection.cursor()

        insert_request_query = """
        INSERT INTO requests (manager_id, project_id, request_text, status)
        VALUES (%s, %s, %s, 'pending')
        """
        cursor.execute(insert_request_query,
                       (manager_id, project_id, request_text))
        connection.commit()

        request_id = cursor.lastrowid

        insert_request_employee_query = """
        INSERT INTO request_employees (request_id, employee_id)
        VALUES (%s, %s)
        """
        for employee_id in selected_employee_ids:
            cursor.execute(insert_request_employee_query,
                           (request_id, employee_id))

        connection.commit()

        return True

    except Error as e:
        print(f"Error: {e}")
        return False

    finally:
        cursor.close()
        connection.close()


def get_requests_data():
    try:
        # Get database connection
        connection = create_connection()
        cursor = connection.cursor(dictionary=True)

        query = """
            SELECT req.request_id, req.manager_id, req.project_id, req.request_text, req.status,
                   mgr.first_name AS manager_first_name, mgr.last_name AS manager_last_name,
                   emp.first_name AS employee_first_name, emp.last_name AS employee_last_name,
                   proj.project_name
            FROM requests req
            INNER JOIN manager mgr ON req.manager_id = mgr.manager_id
            INNER JOIN request_employees req_emp ON req.request_id = req_emp.request_id
            INNER JOIN employee emp ON req_emp.employee_id = emp.employee_id
            INNER JOIN project proj ON req.project_id = proj.project_id
            WHERE req.status = 'pending'
        """
        cursor.execute(query)
        requests_data = cursor.fetchall()

        requests = []
        for request_data in requests_data:
            request_info = {
                'request_id': request_data['request_id'],
                'manager_name': f"{request_data['manager_first_name']} {request_data['manager_last_name']}",
                'project_name': request_data['project_name'],
                'request_text': request_data['request_text'],
                'status': request_data['status'],
                'employees': [{'first_name': request_data['employee_first_name'], 'last_name': request_data['employee_last_name']}]
            }
            # Check if the request already exists in the list
            for request in requests:
                if request['request_id'] == request_info['request_id']:
                    request['employees'].append(
                        {'first_name': request_data['employee_first_name'], 'last_name': request_data['employee_last_name']})
                    break
            else:
                requests.append(request_info)

        return requests

    except Error as e:
        print(f"Error: {e}")
        return []

    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()


def approvingRequest(request_id):
    con = create_connection()
    if con is None:
        return "Connection to the database failed.", 500

    cursor = con.cursor()
    try:
        cursor.execute(
            "UPDATE requests SET status = 'approved' WHERE request_id = %s", (request_id,))
        con.commit()
        return True
    except Error as e:
        return False
    finally:
        cursor.close()
        con.close()


def rejectingRequest(request_id):
    con = create_connection()
    if con is None:
        return "Connection to the database failed.", 500

    cursor = con.cursor()
    try:
        cursor.execute(
            "UPDATE requests SET status = 'rejected' WHERE request_id = %s", (request_id,))
        con.commit()
        return True
    except Error as e:
        return False
    finally:
        cursor.close()
        con.close()


def get_request_status():
    connection = create_connection()
    if connection is None:
        return None

    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT r.request_id, r.manager_id, m.first_name, m.last_name, r.request_text, r.status FROM requests r JOIN manager m ON r.manager_id = m.manager_id")
        request = cursor.fetchall()
        return request
    except Error as e:
        return None
    finally:
        cursor.close()
        connection.close()


def get_manager_requests(manager_id):
    connection = create_connection()
    if connection is None:
        return []

    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT request_id, manager_id, request_text, status FROM requests WHERE manager_id = %s", (
                manager_id,)
        )
        requests = cursor.fetchall()
        return requests
    except Error as e:
        print(f"Error: {e}")
        return []
    finally:
        cursor.close()
        connection.close()


@app.route('/')
def index():
    return render_template('index.html')


# Admin routes --------------------------------

@app.route('/adminlogin')
def adminlogin():
    return render_template('adminlogin.html')


@app.route('/forgetPassword')
def forgotPassword():
    return render_template('forgetpassword.html')


def forgetAdminPassword(email, password):
    connection = create_connection()
    if connection is None:
        return "Password Change Failed! Please Retry"

    cursor = connection.cursor()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        cursor.execute("""
            UPDATE admin
            SET password = %s
            WHERE email = %s
        """, (hashed_password, email))
        connection.commit()
        return "Sucessfully Updated Password"
    except Error as e:
        return "Password Change Failed! Please Retry"
    finally:
        cursor.close()
        connection.close()


def forgotEmployeePassword(email, password):
    connection = create_connection()
    if connection is None:
        return "Password Change Failed! Please Retry"

    cursor = connection.cursor()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        cursor.execute("""
            UPDATE employee
            SET password = %s
            WHERE email = %s
        """, (hashed_password, email))
        connection.commit()
        return "Sucessfully Updated Password"
    except Error as e:
        return "Password Change Failed! Please Retry"
    finally:
        cursor.close()
        connection.close()


def forgotManagerPassword(email, password):
    connection = create_connection()
    if connection is None:
        return "Password Change Failed! Please Retry"

    cursor = connection.cursor()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        cursor.execute("""
            UPDATE manager
            SET password = %s
            WHERE email = %s
        """, (hashed_password, email))
        connection.commit()
        return "Sucessfully Updated Password"
    except Error as e:
        return "Password Change Failed! Please Retry"
    finally:
        cursor.close()
        connection.close()


@app.route('/forgetPasswordRoute', methods=['POST'])
def forgotPasswordRoute():
    role = request.form['option']
    email = request.form['email-id']
    password = request.form['password']
    message = "Failed to update your password"

    if role == "1":
        message = forgetAdminPassword(email, password)
        return render_template('forgetpassword.html', message=message)
    elif role == "2":
        message = forgotEmployeePassword(email, password)
        return render_template('forgetpassword.html', message=message)
    elif role == "3":
        message = forgotManagerPassword(email, password)
        return render_template('forgetpassword.html', message=message)

    return render_template('forgetpassword.html', message=message)


@ app.route('/adminpage')
def adminpage():
    return render_template('adminpage.html')


@ app.route('/adminloginprocess', methods=['POST'])
def adminloginprocess():
    email = request.form['email']
    password = request.form['password']

    output = login_admin(email, password)
    failedtext = 'Please login with correct email and password'

    if output is True:
        return render_template('adminpage.html')
    else:
        return render_template('adminlogin.html', failedtext=failedtext)


@ app.route('/addEmployeePage')
def addEmployeePage():
    managers = get_managers()
    return render_template('addemployee.html', managers=managers)


@ app.route('/addemployees', methods=['POST'])
def addemployees():
    firstname = request.form['first-name']
    lastname = request.form['last-name']
    email = request.form['email']
    phone = request.form['phone-number']
    position = request.form['position']
    address = request.form['address']
    manager_id = request.form['manager-id']
    password = request.form['password']

    print(firstname, lastname, email, phone, position, address, manager_id)
    ifAddSucess = addEmployee(
        firstname, lastname, email, phone, position, address, manager_id, password)

    if ifAddSucess:
        successMessage = f'Successfully added employee {firstname}'
        return render_template('addemployee.html', successMessage=successMessage, managers=get_managers())
    else:
        failMessage = f'Please add employee again!'
        return render_template('addemployee.html', failMessage=failMessage, managers=get_managers())


@ app.route('/addManagerPage')
def addManagerPage():
    return render_template('addmanager.html')


@ app.route('/addmanagers', methods=['GET', 'POST'])
def addmanagers():
    firstname = request.form['first-name']
    lastname = request.form['last-name']
    email = request.form['email']
    phone = request.form['phone-number']
    password = request.form['password']

    ifAddSucess = addManager(firstname, lastname, email, phone, password)

    if ifAddSucess == True:
        sucessMessage = f'Sucessfull added Manager ', firstname
        return render_template('addmanager.html', sucessMessage=sucessMessage)
    else:
        failmessage = f'Please add Manager again! '
        return render_template('addmanager.html', failmessage=failmessage)


@ app.route('/addProjectPage')
def addProjectPage():
    return render_template('addproject.html')


@ app.route('/addprojects',  methods=['GET', 'POST'])
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


@ app.route('/viewEmployeePage')
def viewEmployeePage():
    success, employees = viewEmployee()
    if success:
        return render_template('viewemployee.html', employees=employees)
    else:
        return render_template('viewemployee.html', error="No employees found or an error occurred.")


@ app.route('/updateEmployee/<int:employee_id>', methods=['GET', 'POST'])
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


@ app.route('/deleteEmployee/<int:employee_id>')
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


@ app.route('/viewProjectPage')
def viewProjectPage():
    success, project = viewProject()
    if success:
        return render_template('viewproject.html', project=project)
    else:
        return render_template('viewproject.html', error="No employees found or an error occurred.")


@ app.route('/updateProject/<int:project_id>', methods=['GET'])
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


@ app.route('/updateProject/<int:project_id>', methods=['POST'])
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


@ app.route('/deleteProject/<int:project_id>')
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


@ app.route('/viewManagers')
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


@ app.route('/updateManager/<int:manager_id>', methods=['GET', 'POST'])
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


@ app.route('/deleteManager/<int:manager_id>', methods=['POST', 'GET'])
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


@ app.route('/assignProjectPage')
def assignProjectPage():
    unassigned_employees = get_unassigned_employees()
    projects = get_all_projects()
    return render_template('assign_project.html', unassigned_employees=unassigned_employees, projects=projects)


@ app.route('/assignProject', methods=['POST'])
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


@ app.route('/unassignProjectPage')
def unassignProjectPage():
    assigned_employees = get_assigned_employees()
    return render_template('unassign_project.html', assigned_employees=assigned_employees)


@ app.route('/unassignProject', methods=['POST'])
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


@ app.route('/viewEmployeesWithProjects')
def viewEmployeesWithProjectsPage():
    success, employees = viewEmployeesWithProjects()
    if success:
        return render_template('employee_with_project.html', employees=employees)
    else:
        return render_template('employee_with_project.html', error="No employees found or an error occurred.")


@ app.route('/approveRejectManagerRequest')
def approveRejectManagerRequest():
    requests = get_requests_data()
    return render_template('approve_reject_manager_req.html', requests=requests)


@ app.route('/approveRequest/<int:request_id>')
def approveRequest(request_id):
    approvingRequest(request_id)
    requests = get_requests_data()
    return render_template('approve_reject_manager_req.html', requests=requests, message="Sucessfully Approved Request")


@ app.route('/rejectRequest/<int:request_id>')
def rejectRequest(request_id):
    success = rejectingRequest(request_id)
    requests = get_requests_data()
    return render_template('approve_reject_manager_req.html', requests=requests, message="Sucessfully Reject Request")


@ app.route('/requestStatus', methods=['GET'])
def requestStatus():
    requests = get_request_status()
    return render_template('request_history.html', requests=requests)


# Employee Routes --------------------------------


@ app.route('/emplogin')
def emplogin():
    return render_template('emplogin.html')


@ app.route('/employeeloginprocess', methods=['GET', 'POST'])
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


@ app.route('/employeepage')
def employeepage():
    employee = session.get('employee')
    if not employee:
        return redirect('/emplogin')

    return render_template('employeepage.html', employee=employee)


@ app.route('/showDetails')
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


@ app.route('/addskills', methods=['POST'])
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


@ app.route('/updateskills', methods=['GET'])
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


@ app.route('/viewEmployeePagetoEmployee')
def viewEmployeePagetoEmployee():
    success, employees = viewEmployee()
    if success:
        return render_template('viewemployeetoemployee.html', employees=employees)
    else:
        return render_template('viewemployeetoemployee.html', error="No employees found or an error occurred.")


@ app.route('/viewManagerPagetoEmployee')
def viewManagerPagetoEmployee():
    success, managers = viewManager()
    if success:
        return render_template('viewmanagertoemployee.html', managers=managers)
    else:
        return render_template('viewmanagertoemployee.html', error="No employees found or an error occurred.")


# Manager Routes --------------------------------


@ app.route('/mnglogin')
def mnglogin():
    return render_template('mnglogin.html')


@ app.route('/managerloginprocess', methods=['GET', 'POST'])
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


@ app.route('/managerpage')
def managerpage():
    manager = session.get('manager')
    if not manager:
        return redirect('/mnglogin')

    return render_template('managerpage.html', manager=manager)


@ app.route('/showManagerDetails')
def show_manager_details():
    manager = session.get('manager')
    if not manager:
        return redirect('/mnglogin')

    con = create_connection()
    if con is None:
        return render_template('showdetailsmanager.html', error="Could not connect to the database.")

    cursor = con.cursor(dictionary=True)
    try:
        # Fetch employees managed by this manager
        cursor.execute("""
            SELECT employee_id, first_name, last_name, email, phone_number, position
            FROM employee
            WHERE manager_id = %s
        """, (manager['manager_id'],))
        employees = cursor.fetchall()

        return render_template('showdetailsmanager.html', manager=manager, employees=employees)
    except Error as e:
        return render_template('showdetailsmanager.html', error="An error occurred while fetching details.")
    finally:
        cursor.close()
        con.close()


@ app.route('/viewEmployeePagetoManager')
def viewEmployeePagetoManager():
    success, employees = viewEmployee()
    if success:
        return render_template('viewemployeetomanager.html', employees=employees)
    else:
        return render_template('viewemployeetomanager.html', error="No employees found or an error occurred.")


@ app.route('/viewManagerPagetoManager')
def viewManagerPagetoManager():
    success, managers = viewManager()
    if success:
        return render_template('viewmanagertomanager.html', managers=managers)
    else:
        return render_template('viewmanagertomanager.html', error="No employees found or an error occurred.")


@ app.route('/viewProjecttoMnager')
def viewProjectToMnager():
    success, project = viewProject()
    if success:
        return render_template('viewProjecttoManager.html', project=project)
    else:
        return render_template('viewProjecttoManager.html', error="No employees found or an error occurred.")


@ app.route('/managerRequests')
def managerRequests():
    unassignEmployee = get_unassigned_employees_with_skills()
    allProjects = get_all_projects()
    return render_template('managerRequests.html', unassignEmployee=unassignEmployee, allProjects=allProjects)


@ app.route('/managerRequestRoute', methods=['POST'])
def managerRequestRoute():
    selected_employee_ids = request.form.getlist('employee_ids')
    project_id = request.form.get('project_id')
    request_text = request.form.get('request-text')
    manager_id = session['manager']['manager_id']

    sucess = make_request(selected_employee_ids,
                          project_id, request_text, manager_id)

    if sucess:
        return render_template('managerRequests.html', successMessage="Successfully Sent Request to Admin")
    else:
        return render_template('managerRequests.html', errorMessage="An error occurred while sending the request")


@ app.route('/managerRequestStatus', methods=['GET'])
def managerRequestStatus():
    manager_id = session['manager'].get('manager_id')
    requests = get_manager_requests(manager_id)
    return render_template('managerRequestStatus.html', requests=requests)


if __name__ == "__main__":
    app.run(debug=True)
