CREATE database employeemanagement;

USE employeemanagement;

CREATE TABLE admin (
  id INT NOT NULL AUTO_INCREMENT,
  username VARCHAR(50) NOT NULL,
  name VARCHAR(50) NOT NULL,
  email VARCHAR(100) NOT NULL,
  password VARCHAR(255) NOT NULL,
  PRIMARY KEY (id),
  UNIQUE (username),
  UNIQUE (email)
);

CREATE TABLE employee (
  employee_id INT AUTO_INCREMENT PRIMARY KEY,
  first_name VARCHAR(50) NOT NULL,
  last_name VARCHAR(50) NOT NULL,
  email VARCHAR(100) NOT NULL UNIQUE,
  phone_number VARCHAR(20),
  position VARCHAR(100),
  address VARCHAR(255),
  manager_id INT,
  password VARCHAR(255),
  FOREIGN KEY (manager_id) REFERENCES manager(manager_id) ON DELETE SET NULL
);

CREATE TABLE manager(
    manager_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    email VARCHAR(100) UNIQUE,
    phone_number VARCHAR(15),
    password VARCHAR(255)
);

CREATE TABLE project (
    project_id INT AUTO_INCREMENT PRIMARY KEY,
    project_name VARCHAR(255) NOT NULL,
    description TEXT
);


CREATE TABLE employeeproject (
    employee_id INT,
    project_id INT,
    PRIMARY KEY (employee_id),
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id) ON DELETE CASCADE,
    FOREIGN KEY (project_id) REFERENCES project(project_id) ON DELETE CASCADE
);

CREATE TABLE employeeskills (
    skill_id INT AUTO_INCREMENT PRIMARY KEY,
    employee_id INT,
    skill_name VARCHAR(255) NOT NULL,
    proficiency_level VARCHAR(50),
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id) ON DELETE CASCADE
);

CREATE TABLE requests (
    request_id INT AUTO_INCREMENT PRIMARY KEY,
    manager_id INT,
    project_id INT,
    request_text TEXT,
    status ENUM('pending', 'approved', 'rejected'),
    FOREIGN KEY (manager_id) REFERENCES manager(manager_id) ON DELETE CASCADE,
    FOREIGN KEY (project_id) REFERENCES project(project_id) ON DELETE CASCADE
);

CREATE TABLE request_employees (
    request_employee_id INT AUTO_INCREMENT PRIMARY KEY,
    request_id INT,
    employee_id INT,
    FOREIGN KEY (request_id) REFERENCES requests(request_id) ON DELETE CASCADE,
    FOREIGN KEY (employee_id) REFERENCES employee(employee_id) ON DELETE CASCADE
);


