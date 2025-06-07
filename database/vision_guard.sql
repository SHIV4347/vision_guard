CREATE DATABASE vision_guard;


-- Table: users
CREATE TABLE users (
    id INT PRIMARY KEY IDENTITY(1,1),
    name NVARCHAR(100),
    email NVARCHAR(100) UNIQUE,
    password NVARCHAR(100)
);

-- Table: criminals
CREATE TABLE criminals (
    id INT PRIMARY KEY IDENTITY(1,1),
    name NVARCHAR(100),
    age INT,
    address NVARCHAR(255),
    crimes NVARCHAR(MAX),
    image_path NVARCHAR(255) -- Stores file path like 'static/criminal_images/john_doe.jpg'
);

-- Table: security_personnel
CREATE TABLE security_personnel (
    id INT PRIMARY KEY IDENTITY(1,1),
    name NVARCHAR(100),
    email NVARCHAR(100),
    chat_id NVARCHAR(20)
);

CREATE TABLE cameras (
    id INT IDENTITY PRIMARY KEY,
    url VARCHAR(255) NOT NULL,
    location VARCHAR(100) NOT NULL
);


select * from users
select * from security_personnel
select * from criminals
select * from cameras

ALTER TABLE Criminals ADD face_id VARCHAR(255)

DELETE FROM criminals;

