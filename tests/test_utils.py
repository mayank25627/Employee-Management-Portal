import pytest
from app import create_connection, login_admin, login_employee, login_manager, addEmployee, addManager, addProjects, viewEmployee, viewManager, viewProject, get_unassigned_employees, get_unassigned_employees_with_skills, get_assigned_employees, get_all_projects, get_managers, viewEmployeesWithProjects, make_request, approvingRequest, rejectingRequest, get_request_status, get_manager_requests, forgetAdminPassword, forgotEmployeePassword, forgotManagerPassword

from mysql.connector import Error
import bcrypt
import logging

logger = logging.getLogger(__name__)


def test_create_connection_success(mocker):
    """
    Test create_connection function for a successful connection
    """
    mock_connection = mocker.Mock()
    mocker.patch('mysql.connector.connect', return_value=mock_connection)
    connection = create_connection()

    logger.info("Testing the connection success")
    assert connection is not None


def test_create_connection_failure(mocker):
    """
    Test create_connection function for a failed connection
    """
    mocker.patch('mysql.connector.connect',
                 side_effect=Error("Connection Error"))
    connection = create_connection()

    logger.info("Testing the connection failure")
    assert connection is None


def test_login_admin_success(mocker):
    """
    Test login_admin function for successful login
    """
    mock_connection = mocker.Mock()
    mock_cursor = mocker.Mock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = ['hashed_password']

    mocker.patch('app.create_connection', return_value=mock_connection)
    mocker.patch('bcrypt.checkpw', return_value=True)

    logger.info("Testing the admin login sucessfully")

    assert login_admin('admin@nucleusteq.com', 'Admin@123')


def test_login_admin_failure_wrong_password(mocker):
    """
    Test login_admin function when password is incorrect
    """
    mock_connection = mocker.Mock()
    mock_cursor = mocker.Mock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = ['hashed_password']

    mocker.patch('app.create_connection', return_value=mock_connection)
    mocker.patch('bcrypt.checkpw', return_value=False)

    assert not login_admin('admin@nucleusteq.com', 'Admin@123')


def test_login_employee(mocker):
    """
    Test login_employee function for sucessfully login`
    """
    mock_connection = mocker.Mock()
    mock_cursor = mocker.Mock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = {'password': 'hashed_password'}

    mocker.patch('app.create_connection', return_value=mock_connection)
    mocker.patch('bcrypt.checkpw', return_value=True)

    logger.info("Testing the Employee login sucessfully")

    assert login_employee('sahu25627@nucleusteq.com', 'Mayank@123')


def test_login_manager(mocker):
    """
    Test login_MANAGER function for sucessfully login`
    """
    mock_connection = mocker.Mock()
    mock_cursor = mocker.Mock()
    mock_connection.cursor.return_value = mock_cursor
    mock_cursor.fetchone.return_value = {'password': 'hashed_password'}

    mocker.patch('app.create_connection', return_value=mock_connection)
    mocker.patch('bcrypt.checkpw', return_value=True)

    logger.info("Testing the Manager login sucessfully")

    assert login_manager('rahul_khatri@nucleusteq.com', 'Rahul@123')


def test_addEmployee(mocker):
    """
      Test function for addEmployee by admin`
    """

    mocker.patch('app.create_connection', return_value=mocker.MagicMock())
    mocker.patch.object(bcrypt, 'hashpw', return_value=b'hashed_password')

    logger.info("Testing the add employee sucessfully")

    assert addEmployee('Mayank', 'Sahu', 'sahu25627@nucleusteq.com',
                       '8458809510', 'Senior Software Engineer', 'Pithampur Mp', 20, 'Mayank@123')


def test_addManager(mocker):
    """
    Test function for addManager by admin
    """

    mocker.patch('app.create_connection')
    mocker.patch.object(bcrypt, 'hashpw', return_value=b'hashed_password')

    logger.info("Testing the add manager sucessfully")
    assert addManager('Rahul', 'Khatri', 'Rahul_khatri@nucleusteq.com',
                      '7455899668', 'Mayank@123')


def test_addProjects(mocker):
    """
      Test function for add projects by admin`
    """

    mocker.patch('app.create_connection')
    logger.info("Testing the add projects sucessfully")
    assert addProjects('Student Management System',
                       'This is a student management project')


def test_viewEmployee(mocker):
    """
    Test view employee for successful
    """
    mock_connection = mocker.Mock()
    mock_cursor = mocker.Mock()
    mock_cursor.fetchall.return_value = [
        {'first_name': 'Mayank', 'last_name': 'Sahu',
            'email': 'sahu25627@nucleusteq.com', 'phone_number': '8458809510', 'position': 'Software Developer', 'address': 'Pithampur', 'manager_id': '20'}
    ]

    mocker.patch('app.create_connection')

    logger.info("Testing the view employee sucessfully")

    assert viewEmployee()


def test_viewManager(mocker):
    """
    Test view manager function for successful
    """
    mock_connection = mocker.Mock()
    mock_cursor = mocker.Mock()
    mock_cursor.fetchall.return_value = [
        {'first_name': 'Rahul', 'last_name': 'Khatri',
            'email': 'rahul_khatri@nucleusteq.com', 'phone_number': '75889548759'}
    ]

    mocker.patch('app.create_connection')

    logger.info("Testing the view manager sucessfully")

    assert viewManager()


def test_viewProject(mocker):
    """
    Test view project function for successful
    """
    mock_connection = mocker.Mock()
    mock_cursor = mocker.Mock()
    mock_cursor.fetchall.return_value = [
        {'project_name': 'Employee Management System',
            'description': 'This is a employee management system'}
    ]

    mocker.patch('app.create_connection')

    logger.info("Testing the view project sucessfully")

    assert viewProject()


def test_get_unassigned_employees(mocker):
    """
    Test get unassigned employees who have no project till now function for successful
    """
    mock_connection = mocker.Mock()
    mock_cursor = mocker.Mock()
    mock_cursor.fetchall.return_value = [
        {'employee_id': '1',
            'first_name': 'Mayank', 'last_name': 'Sahu'}
    ]

    mocker.patch('app.create_connection')

    logger.info(
        "Testing get unassigned employees who have no project till now sucessfully")

    assert get_unassigned_employees()


def test_get_unassigned_employees_with_skills(mocker):
    """
    Testing get unassigned employees with skills who have no project till now sucessfully
    """
    mock_connection = mocker.Mock()
    mock_cursor = mocker.Mock()
    mock_cursor.fetchall.return_value = [
        {'employee_id': '1',
            'first_name': 'Mayank', 'last_name': 'Sahu', 'skill_name': 'Java'}
    ]

    mocker.patch('app.create_connection')

    logger.info(
        "Testing get unassigned employees with skills who have no project till now sucessfully")

    assert get_unassigned_employees_with_skills()


def test_get_assigned_employees(mocker):
    """
    Test get assigned employees who have 1 project till now function for successful
    """
    mock_connection = mocker.Mock()
    mock_cursor = mocker.Mock()
    mock_cursor.fetchall.return_value = [
        {'employee_id': '1',
            'first_name': 'Mayank', 'last_name': 'Sahu', 'project_id': '1', 'project_name': 'Student Management'}
    ]

    mocker.patch('app.create_connection')

    logger.info(
        "Testing get assigned employees who have a project till now sucessfully")

    assert get_assigned_employees()


def test_get_all_projects(mocker):
    """
    Test get all project function for successful
    """
    mock_connection = mocker.Mock()
    mock_cursor = mocker.Mock()
    mock_cursor.fetchall.return_value = [
        {'project_id': '1',
            'project_name': 'Student Management'}
    ]

    mocker.patch('app.create_connection')

    logger.info(
        "Testing get all projects sucessfully")

    assert get_all_projects()


def test_get_managers(mocker):
    """
    Test get all manager function for successful
    """
    mock_connection = mocker.Mock()
    mock_cursor = mocker.Mock()
    mock_cursor.fetchall.return_value = [
        {'manager_id': '20',
            'first_name': 'Rahul', 'last_name': 'Khatri'}
    ]

    mocker.patch('app.create_connection')

    logger.info(
        "Testing get all manager sucessfully")

    assert get_managers()


def test_viewEmployeesWithProjects(mocker):
    """
    Test get all employee with thier projects function for successful
    """
    mock_connection = mocker.Mock()
    mock_cursor = mocker.Mock()
    mock_cursor.fetchall.return_value = [
        {'employee_id': '1',
            'first_name': 'Mayank', 'last_name': 'Sahu', 'project_name': 'Student Management'}
    ]

    mocker.patch('app.create_connection')

    logger.info(
        "Testing get all employee with thier projects sucessfully")

    assert viewEmployeesWithProjects()


def test_make_request(mocker):
    """
    Test function for make request by manager
    """

    mocker.patch('app.create_connection')

    logger.info("Testing the make request by manager")
    assert make_request(['1', '3'], 'project_id',
                        'Please add those employee in this project', '20')


def test_approvingRequest(mocker):
    """
    Test function for approving Request by admin
    """

    mocker.patch('app.create_connection')
    logger.info("Testing the approve request by admin sucessfully")
    assert approvingRequest('1')


def test_rejectingRequest(mocker):
    """
    Test function for Rejecting Request by admin
    """

    mocker.patch('app.create_connection')
    logger.info("Testing the reject request by admin sucessfully")
    assert rejectingRequest('1')


def test_get_request_status(mocker):
    """
    Test get all request status successful
    """
    mock_connection = mocker.Mock()
    mock_cursor = mocker.Mock()
    mock_cursor.fetchall.return_value = [
        {'request_id': '1', 'manager_id': '20',
            'first_name': 'Rohan', 'last_name': 'Khatri', 'request_text': 'Assing this project', 'status': 'approved'}
    ]

    mocker.patch('app.create_connection')

    logger.info(
        "Test get all request status successful")

    assert get_request_status()


def test_get_manager_requests(mocker):
    """
    Test get all request of manager successful
    """
    mock_connection = mocker.Mock()
    mock_cursor = mocker.Mock()
    mock_cursor.fetchall.return_value = [
        {'request_id': '1', 'manager_id': '20',
         'request_text': 'Assing this project', 'status': 'approved'}
    ]

    mocker.patch('app.create_connection')

    logger.info(
        "Test get all request of manager successful")

    assert get_manager_requests('20')


def test_forgetAdminPassword(mocker):
    """
    Test function for forget admin password sucess
    """

    mocker.patch('app.create_connection')
    mocker.patch.object(bcrypt, 'hashpw', return_value=b'hashed_password')

    logger.info("Testing the forget admin password sucessfully")
    assert forgetAdminPassword('admin@nucleusteq.com',
                               'Admin@123')


def test_forgotEmployeePassword(mocker):
    """
    Test function for forget employee password sucess
    """

    mocker.patch('app.create_connection')
    mocker.patch.object(bcrypt, 'hashpw', return_value=b'hashed_password')

    logger.info("Testing the forget employee password sucessfully")
    assert forgotEmployeePassword('sahu25627@nucleusteq.com',
                                  'Mayank@123')


def test_forgotManagerPassword(mocker):
    """
    Test function for forget manager password sucess
    """

    mocker.patch('app.create_connection')
    mocker.patch.object(bcrypt, 'hashpw', return_value=b'hashed_password')

    logger.info("Testing the forget manager password sucessfully")
    assert forgotEmployeePassword('rohan_khatri@nucleusteq.com',
                                  'Rohan@123')
