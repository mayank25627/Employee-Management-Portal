import logging

logger = logging.getLogger(__name__)


def test_index(client):
    response = client.get("/")
    assert response.status_code == 200


def test_adminlogin_route(client):
    """
    Test the admin login page rendering.
    """
    response = client.get('/adminlogin')
    logger.info("Testing the admin login route")
    assert response.status_code == 200
    assert b"Login Admin" in response.data


def test_adminloginprocess_route_success(client, mocker):
    """
    Test the admin login process with correct credentials.
    """
    mocker.patch('app.login_admin', return_value=True)

    response = client.post('/adminloginprocess', data={
        'email': 'admin@nucleusteq.com',
        'password': 'admin'
    })
    logger.info("Testing the admin login process with correct credentials")
    assert response.status_code == 200
    assert b"Admin Dashboard" in response.data


def test_adminloginprocess_route_failure(client, mocker):
    """
    Test the admin login process with incorrect credentials.
    """
    mocker.patch('app.login_admin', return_value=False)

    response = client.post('/adminloginprocess', data={
        'email': 'admin@gmail.com',
        'password': 'wrongpassword'
    })
    logger.info("Testing the admin login process with incorrect credentials")
    assert response.status_code == 200
    assert b"Please login with correct email and password" in response.data


def test_forgetpassword_route(client):
    """
    Test the forget password route.
    """
    response = client.get('/forgetPassword')
    logger.info("Testing the forget password route")
    assert response.status_code == 200
    assert b"Forget Your Password" in response.data


def test_adminpage(client):
    """
    Test the admin page
    """
    response = client.get('/adminpage')
    logger.info("Testing the admin page route")
    assert response.status_code == 200
    assert b"Welcome Admin!" in response.data


def test_addEmployeePage_route(client, mocker):
    """
    Test the addEmployeePage route.
    """
    managers = [
        {'manager_id': 1, 'first_name': 'Rahul', 'last_name': 'Khatri'},
        {'manager_id': 3, 'first_name': 'Rohan', 'last_name': 'Khatri'}
    ]
    mocker.patch('app.get_managers', return_value=managers)

    response = client.get('/addEmployeePage')
    logger.info("Testing the addEmployeePage route")

    assert response.status_code == 200
    assert b"Add Employee" in response.data
    assert b"Rahul Khatri" in response.data
    assert b"Rohan Khatri" in response.data


def test_addemployees(client, mocker):
    """
    Test addemployees api by admin
    """
    mocker.patch('app.addEmployee', return_value=True)
    mocker.patch('app.get_managers', return_value=[
        {'manager_id': 1, 'first_name': 'Rahul', 'last_name': 'Khatri'}
    ])

    response = client.post('/addemployees', data={
        'first-name': 'Mayank',
        'last-name': 'Sahu',
        'email': 'sahu25627@nucleusteq.com',
        'phone-number': '8458809510',
        'position': 'Senior Software Developer',
        'address': 'Pithampur MP',
        'manager-id': '1',
        'password': 'Mayank@123'
    })

    logger.info('Add Employee Test Success')
    assert response.status_code == 200
    assert b"Successfully added employee Mayank" in response.data


def test_addManagerPage(client):
    """
    Test for addManager page
    """

    response = client.get('/addManagerPage')
    logger.info("Testing the add manager page route route")
    assert response.status_code == 200
    assert b"Add Manager" in response.data


def test_addmanagers(client, mocker):
    """
    Test for Adding Manager page
    """
    mocker.patch('app.addManager', return_value=True)
    response = client.post('/addmanagers', data={
        'first-name': 'Rahul',
        'last-name': 'Khatri',
        'email': 'rahul_khatri@nucleusteq.com',
        'phone-number': '8458809500',
        'password': 'Rahul@123'
    })

    logger.info('Adding manager route Testing')
    assert response.status_code == 200
    assert b"Successfully added Manager Rahul" in response.data


def test_addProjectPage(client):
    """
    Test for app project page
    """
    response = client.get('/addProjectPage')
    logger.info("Testing the add project page route route")
    assert response.status_code == 200
    assert b"Add Project" in response.data


def test_addprojects(client, mocker):
    """
    Test for Adding Project
    """
    mocker.patch('app.addProjects', return_value=True)
    response = client.post('/addprojects', data={
        'project-name': 'Employee Management Portal',
        'description': 'This is the employee management system'
    })

    logger.info('Adding project route Testing')
    assert response.status_code == 200
    assert b"Successfully added Project Employee Management Portal" in response.data


def test_view_employee_page(client, mocker):
    """
    Test Updating Employees Page
    """
    mocker.patch('app.viewEmployee', return_value=(True, [
        {'employee_id': 1, 'first_name': 'Mayank',
            'last_name': 'Sahu', 'email': 'sahu25627@nucleusteq.com'}
    ]))

    response = client.get('/viewEmployeePage')
    logger.info("Testing the view employee page route route")

    assert response.status_code == 200
    assert b'View Employee' in response.data


def test_view_employee_page_no_employees(client, mocker):
    """
    Test View Employees Page
    """
    mocker.patch('app.viewEmployee', return_value=(False, []))

    response = client.get('/viewEmployeePage')
    logger.info("Testing the view employee route")
    assert response.status_code == 200
    assert b'No employees found or an error occurred.' in response.data


def test_update_employee(client, mocker):
    """
    Test Updating Employees
    """
    response = client.post('/updateEmployee/1', data={
        'first-name': 'Mayank',
        'last-name': 'Sahu',
        'email': 'sahu25627@nucleusteq.com',
        'phone-number': '8458809510',
        'position': 'Software Engineer',
        'address': 'Pithampur MP',
        'manager-id': '3'
    })
    logger.info("Testing the update employee route")
    assert response.status_code == 302
    follow_response = client.get(response.headers['Location'])
    assert follow_response.status_code == 200
    assert b'Employee List' in follow_response.data


def test_delete_employee(client):
    """
    Test Updating Employees
    """
    response = client.post('/updateEmployee/1', data={
        'first-name': 'Mayank',
        'last-name': 'Sahu',
        'email': 'sahu25627@nucleusteq.com',
        'phone-number': '8458809510',
        'position': 'Software Engineer',
        'address': 'Pithampur MP',
        'manager-id': '3'
    })
    logger.info("Testing the update employee route")
    assert response.status_code == 302
    follow_response = client.get(response.headers['Location'])
    assert follow_response.status_code == 200
    assert b'Employee List' in follow_response.data


def test_viewProjectPage(client, mocker):
    """
    Test View Project page Route
    """

    mocker.patch('app.viewProject', return_value=(True, [
        {'project_name': 'Employee Management Portal',
            'description': 'This is the employee management system '}
    ]))

    response = client.get('/viewProjectPage')
    logger.info("Testing the view Project page route")

    assert response.status_code == 200
    assert b'View Project' in response.data


def test_showUpdateProjectForm(client):
    """
    Test show Update Project Form route
    """
    response = client.get('/updateProject/8')
    logger.info("Testing the update Project route")
    assert response.status_code == 200
    assert b'Update Project' in response.data


def test_updateProject(client):
    """
    Tets Update Project route
    """
    response = client.post('/updateProject/10', data={
        'project_name': 'Accident Detection Project',
        'description': 'This project is AI based'
    })
    logger.info("Testing the update project route")
    assert response.status_code == 302
    follow_response = client.get(response.headers['Location'])
    assert follow_response.status_code == 200
    assert b'Project List' in follow_response.data


def test_deleteProject(client):
    """
    Tets Delete Project route
    """
    response = client.get('/deleteProject/11')
    logger.info("Testing the delete project route")
    assert response.status_code == 302
    follow_response = client.get(response.headers['Location'])
    assert follow_response.status_code == 200
    assert b'Project List' in follow_response.data


def test_viewManagers(client):
    """
    Test View Manager routes
    """
    response = client.get('/viewManagers')
    logger.info("Testing the view manager route")
    assert response.status_code == 200
    assert b'Managers List' in response.data


def test_updateManager(client):
    """
    Test Update Manager routes
    """
    response = client.get('/updateManager/1')
    logger.info("Testing the update manager route")
    assert response.status_code == 200
    assert b'View Manager' in response.data

    response2 = client.post('/updateManager/1', data={
        'first_name': 'Rahul',
        'last_name': 'Khatri',
        'email': 'rahul_khatri@nucleusteq.com',
        'phone_number': '8955789875'
    })

    logger.info('Testing updateManager Updates done')
    assert response2.status_code == 302
    follow_response = client.get(response2.headers['Location'])
    assert follow_response.status_code == 200
    assert b'View Manager' in follow_response.data


def test_deleteManager(client):
    """
    Tets Delete Manager route
    """
    response = client.get('/deleteManager/1')
    logger.info("Testing the delete Manager route")
    assert response.status_code == 302
    follow_response = client.get(response.headers['Location'])
    assert follow_response.status_code == 200


def test_assignProjectPage(client, mocker):
    """
    Tests Assign Project Page route
    """
    mocker.patch('app.get_unassigned_employees', return_value=[
        {'employee_id': '1', 'first_name': 'Mayank', 'last_name': 'Sahu'}
    ])

    mocker.patch('app.get_all_projects', return_value=[
        {'project_name': 'Employee Management Portal',
            'description': 'This is the employee management system '}
    ])

    response = client.get('/assignProjectPage')
    logger.info("Testing the assign project page route")

    assert response.status_code == 200
    assert b'Assign Project' in response.data


def test_assignProject(client, mocker):
    """
    Tests Assign Project route
    """
    mocker.patch('app.get_unassigned_employees', return_value=[
        {'employee_id': '1', 'first_name': 'Mayank', 'last_name': 'Sahu'}
    ])

    mocker.patch('app.get_all_projects', return_value=[
        {'project_name': 'Employee Management Portal',
            'description': 'This is the employee management system '}
    ])

    response = client.post('/assignProject', data={
        'employee_id': '1',
        'project_id': '1'
    })
    logger.info("Testing the assign project route")

    if response.status_code != 302:
        print(response.data)  # Print the response data for debugging

    assert response.status_code == 302
    follow_response = client.get(response.headers['Location'])
    assert follow_response.status_code == 200


def test_unassignProjectPage(client, mocker):
    """
    Tests Unassign Project page route
    """
    mocker.patch('app.get_assigned_employees', return_value=[
        {'employee_id': '1', 'first_name': 'Mayank', 'last_name': 'Sahu'}
    ])

    response = client.get('/unassignProjectPage')
    logger.info("Testing the unassignassign project page route")

    assert response.status_code == 200
    assert b'Unassign Project' in response.data


def test_unassignProject(client, mocker):
    """
     Tests Unassign Project route
    """

    mocker.patch('app.get_assigned_employees', return_value=[
        {'employee_id': '1', 'first_name': 'Mayank', 'last_name': 'Sahu'}
    ])

    response = client.post('/unassignProject', data={
        'employee_id': '1'
    })
    logger.info("Testing the unassign employee route")
    assert response.status_code == 302
    follow_response = client.get(response.headers['Location'])
    assert follow_response.status_code == 200


def test_viewEmployeesWithProjects(client, mocker):
    mocker.patch('app.viewEmployeesWithProjects', return_value=[True, {
        'employee_id': '20',
        'first_name':   'Satyam',
        'last_name': 'Rajput',
        'project_name': 'Employee Management Portal'
    }])

    response = client.get('/viewEmployeesWithProjects')
    logger.info('Test viewEmployeesWithProjects route')
    assert response.status_code == 200
    assert b'Employees and Their Projects' in response.data


def test_approveRejectManagerRequest(client, mocker):
    mocker.patch('app.approveRejectManagerRequest', return_value={
        'request_id': 1,
        'manager_id': 1,
        'project_id': 10,
        'request_text': 'PLease Put all those employeees on this project',
        'status': 'pending',
        'manager_first_name': 'Rahul',
        'manager_last_name': 'Khatri',
        'employee_first_name': 'Mayank',
        'employee_last_name': 'Sahu',
        'project_name': 'Employee Management Portal'
    }
    )

    response = client.get('/approveRejectManagerRequest')
    logger.info('Test approveRejectManagerRequest route')
    assert response.status_code == 200


def test_approveRequest(client, mocker):
    """
    Test approve Manager request routes
    """

    mocker.patch('app.approvingRequest', return_value=True)
    mocker.patch('app.get_requests_data', return_value={
        'request_id': 1,
        'manager_id': 1,
        'project_id': 10,
        'request_text': 'PLease Put all those employeees on this project',
        'status': 'pending',
        'manager_first_name': 'Rahul',
        'manager_last_name': 'Khatri',
        'employee_first_name': 'Mayank',
        'employee_last_name': 'Sahu',
        'project_name': 'Employee Management Portal'
    }
    )

    response = client.get('/approveRequest/20')
    logger.info("Testing the approve reject manager request route")
    assert response.status_code == 200
    assert b'Pending Requests' in response.data


def test_rejectRequest(client, mocker):
    """
        Test reject Manager request routes
    """
    mocker.patch('app.rejectingRequest', return_value=True)
    mocker.patch('app.get_requests_data', return_value={
        'request_id': 1,
        'manager_id': 1,
        'project_id': 10,
        'request_text': 'PLease Put all those employeees on this project',
        'status': 'pending',
        'manager_first_name': 'Rahul',
        'manager_last_name': 'Khatri',
        'employee_first_name': 'Mayank',
        'employee_last_name': 'Sahu',
        'project_name': 'Employee Management Portal'
    }
    )

    response = client.get('/rejectRequest/20')
    logger.info("Testing the reject manager request route")
    assert response.status_code == 200
    assert b'Pending Requests' in response.data


def test_requestStatus(client, mocker):
    mocker.patch('app.get_request_status', return_value={
        'request_id': 20,
        'manager_id': 3,
        'first_name': 'Rohan',
        'last_name':  'Khatri',
        'request_text': 'Please assing this employee on project',
        'status': 'pending'
    })

    response = client.get('/requestStatus')
    logger.info("Testing the manager request status route")
    assert response.status_code == 200
    assert b'View Requests' in response.data


# NoW Testing the employee functionalities

def test_emplogin(client):
    """
    Test Emplooyee login route
    """
    response = client.get('/emplogin')
    logger.info("Testing the employee login route")
    assert response.status_code == 200
    assert b'Welcome Employee' in response.data


def test_employeeloginprocess(client, mocker):
    mocker.patch('app.login_employee', return_value=[True, {
        'first_name': 'Mayank',
        'last_name': 'Sahu'
    }])

    response = client.post('/employeeloginprocess', data={
        'email': 'sahu25627@nucleusteq.com',
        'password': 'Mayank@123'
    })
    logger.info("Testing the employee login process with correct credentials")
    assert response.status_code == 302


def test_showDetails(client):
    """
    Test the showDetails routes
    """
    with client.session_transaction() as sess:
        sess['employee'] = {'employee_id': 1, 'manager_id': 1,
                            'first_name': 'Mayank', 'last_name': 'Sahu'}

    response = client.get('/showDetails')
    logger.info("Testing the show details route")
    assert response.status_code == 200


def test_addskills(client, mocker):
    """
    Test the showDetails routes
    """
    with client.session_transaction() as sess:
        sess['employee'] = {'employee_id': 1, 'manager_id': 1,
                            'first_name': 'Mayank', 'last_name': 'Sahu'}

    response = client.post('/addskills', data={
        'skill_name': 'Java',
        'proficiency_level': 'Intermediate'
    })

    logger.info("Testing the ADD Skills route")
    assert response.status_code == 302


def test_updateskills(client):
    """
    Test the Update skills routes
    """
    with client.session_transaction() as sess:
        sess['employee'] = {'employee_id': 1, 'manager_id': 1,
                            'first_name': 'Mayank', 'last_name': 'Sahu'}

    response = client.get('/updateskills')
    logger.info("Testing the ADD Skills route")
    assert response.status_code == 200
    assert b'Update Skills' in response.data


def test_viewEmployeePagetoEmployee(client, mocker):
    """
    Test the viewEmployeePagetoEmployee route
    """

    mocker.patch('app.viewEmployee', return_value=[True, {
        'first_name': 'Mayank',
        'last_name': 'Sahu',
        'email': 'sahu25627@nucleusteq.com',
        'phone': '8458809510',
        'position': 'Senio Software engineer',
        'address': 'Pithampur MP'
    }])

    response = client.get('/viewEmployeePagetoEmployee')
    logger.info("Testing the View Employee route")
    assert response.status_code == 200


def test_viewManagerPagetoEmployee(client, mocker):
    """
    Test the viewManager route
    """
    mocker.patch('app.viewManager', return_value=[True, {
        'first_name': 'Rahul',
        'last_name': 'Khatri',
        'email': 'rahul_khatri@nucleusteq.com',
        'phone_number': '7895478998'
    }])

    response = client.get('/viewManagerPagetoEmployee')
    logger.info("Testing the View Manager route")
    assert response.status_code == 200
    assert b'Manager List' in response.data


def test_mnglogin(client):
    """
    Test Manager Login route
    """
    response = client.get('/mnglogin')
    logger.info("Testing the manager Login route")
    assert response.status_code == 200
    assert b'Welcome Manager' in response.data


def test_managerloginprocess(client, mocker):
    """
    Test Manager Login process route
    """

    mocker.patch('app.login_manager', return_value=[True, {
        'first_name': 'Rohan',
        'last_name': 'Khatri',
        'email': 'rohan_khatri@nucleusteq.com'
    }])

    response = client.post('/managerloginprocess', data={
        'email': 'rohan_khatri@nucleusteq.com',
        'password': 'Rohan@123'
    })
    logger.info("Testing the manager login page route")
    assert response.status_code == 200
    assert b'Welcome' in response.data


def test_managerpage(client, mocker):
    """
    Test Manager Page route that return to the home page of manager login
    """

    with client.session_transaction() as sess:
        sess['manager'] = {'manager_id': 1,
                           'first_name': 'Rahul', 'last_name': 'Khatri'}

    response = client.get('/managerpage')
    logger.info("Testing the manager page route")
    assert response.status_code is 200
    assert b'Welcome' in response.data


def test_showManagerDetails(client):
    """
    Test show Manager Page details route
    """

    with client.session_transaction() as sess:
        sess['manager'] = {'manager_id': 1,
                           'first_name': 'Rahul', 'last_name': 'Khatri'}

    response = client.get('/showManagerDetails')
    logger.info("Testing the Show Manager page route")
    assert response.status_code is 200
    assert b'Manager Details' in response.data


def test_viewEmployeePagetoManager(client, mocker):
    """
    Test the viewEmployeePagetoManager route
    """

    mocker.patch('app.viewEmployee', return_value=[True, {
        'first_name': 'Mayank',
        'last_name': 'Sahu',
        'email': 'sahu25627@nucleusteq.com',
        'phone': '8458809510',
        'position': 'Senio Software engineer',
        'address': 'Pithampur MP'
    }])

    response = client.get('/viewEmployeePagetoManager', follow_redirects=True)
    logger.info("Testing the view Employee page route")
    assert response.status_code is 200
    assert b'Employee List' in response.data


def test_viewManagerPagetoManager(client, mocker):
    """
    Test the viewManagerPagetoManager route
    """

    mocker.patch('app.viewManager', return_value=[True, {
        'first_name': 'Rahul',
        'last_name': 'Khatri',
        'email': 'rahul_khatri@nucleusteq.com',
        'phone_number': '7895478998'
    }])

    response = client.get('/viewManagerPagetoManager', follow_redirects=True)
    logger.info("Testing the view manager page route")
    assert response.status_code is 200
    assert b'Manager List' in response.data


def test_viewProjecttoMnager(client, mocker):
    """
    Test the viewProjecttoMnager route
    """

    mocker.patch('app.viewProject', return_value=(True, [
        {'project_name': 'Employee Management Portal',
            'description': 'This is the employee management system '}
    ]))

    response = client.get('/viewManagerPagetoManager', follow_redirects=True)
    logger.info("Testing the view Project page route")
    assert response.status_code is 200
