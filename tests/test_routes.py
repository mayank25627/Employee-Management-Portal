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
