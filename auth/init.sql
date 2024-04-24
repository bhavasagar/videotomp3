CREATE USER 'auth_user'@'localhost' IDENTIFIED BY 'Auth@123';

CREATE DATABASE auth;

GRANT ALL PRIVILEGES ON auth.* TO 'auth_user'@'localhost';

USE auth;

CREATE TABLE User (
    id INT NOT NULL PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255) NOT NULL
);

INSERT INTO User (email, password) VALUES ("bhavasagar09@gmail.com", "Test@user@123")