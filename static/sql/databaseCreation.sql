DROP DATABASE grocery;

CREATE DATABASE grocery;

USE grocery;

CREATE TABLE customers(
    name VARCHAR(20) NOT NULL, 
    id INT PRIMARY KEY AUTO_INCREMENT, 
    sex VARCHAR(1) NOT NULL, 
    dob DATE NOT NULL, 
    email VARCHAR(30) NOT NULL UNIQUE, 
    tel VARCHAR(10) NOT NULL, 
    pwd VARCHAR(20) NOT NULL, 
    doj DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT customers_check_name CHECK (name REGEXP '^([A-Za-z][A-Za-z[[:blank:]]]*)+$'),
    CONSTRAINT customers_check_sex CHECK (sex IN ('M', 'F', 'O')),
    CONSTRAINT customers_check_tel CHECK (tel REGEXP '^[1-9][0-9]{9}$'),
    CONSTRAINT customers_check_pwd CHECK (pwd REGEXP'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$')
);

CREATE TABLE deliveryMen(
    id INT PRIMARY KEY AUTO_INCREMENT, 
    name VARCHAR(20) NOT NULL, 
    sex VARCHAR(1) NOT NULL, 
    dob DATE NOT NULL, 
    email VARCHAR(30) NOT NULL UNIQUE, 
    tel VARCHAR(10) NOT NULL, 
    pwd VARCHAR(20) NOT NULL, 
    doj DATETIME DEFAULT CURRENT_TIMESTAMP NOT NULL,
    CONSTRAINT deliveryMen_check_sex CHECK (sex IN ('M', 'F', 'O')),
    CONSTRAINT deliveryMen_check_name CHECK (name REGEXP '^([A-Za-z][A-Za-z[[:blank:]]]*)+$'),
    CONSTRAINT deliveryMen_check_tel CHECK (tel REGEXP '^[1-9][0-9]{9}$'),
    CONSTRAINT deliveryMen_check_pwd CHECK (pwd REGEXP'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$')
);

CREATE TABLE states(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(25) NOT NULL UNIQUE
);

CREATE TABLE cities(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(25) NOT NULL,
    state INT NOT NULL,
    FOREIGN KEY(state) REFERENCES states(id)
);

CREATE TABLE addresses(
    id INT PRIMARY KEY AUTO_INCREMENT,
    label VARCHAR(25) NOT NULL,
    customer INT NOT NULL,
    houseinfo VARCHAR(50) NOT NULL,
    city INT NOT NULL,
    pin VARCHAR(6) NOT NULL,
    FOREIGN KEY(customer) REFERENCES customers(id),
    FOREIGN KEY(city) REFERENCES cities(id),
    CONSTRAINT check_pin CHECK (pin REGEXP ('^[1-9][0-9]{5}$'))
);

CREATE TABLE orders(
    id INT PRIMARY KEY AUTO_INCREMENT,
    customer INT NOT NULL,
    placedOn DATE NOT NULL,
    deliveryMan INT,
    FOREIGN KEY(customer) REFERENCES customers(id),
    FOREIGN KEY(deliveryMan) REFERENCES deliveryMen(id)
);

CREATE TABLE offers(
    id INT PRIMARY KEY AUTO_INCREMENT,
    code VARCHAR(10) UNIQUE NOT NULL,
    startDate DATE NOT NULL, 
    endDate DATE NOT NULL,
    discount FLOAT NOT NULL
);


CREATE TABLE categories(
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(10) NOT NULL,
    offer INT,
    FOREIGN KEY(offer) REFERENCES offers(id)
);

CREATE TABLE products(
    id INT PRIMARY KEY AUTO_INCREMENT, 
    image VARCHAR(50) NOT NULL,
    name VARCHAR(20) NOT NULL,
    description VARCHAR(100),
    costPrice INT NOT NULL, 
    sellingPrice INT NOT NULL, 
    quantity FLOAT NOT NULL,
    unit VARCHAR(5) NOT NULL, 
    category INT NOT NULL, 
    stock INT NOT NULL,
    FOREIGN KEY(category) REFERENCES categories(id)
);

CREATE TABLE packages(
    product INT NOT NULL,
    _order INT NOT NULL, 
    count INT NOT NULL,
    stars INT,
    review VARCHAR(50),
    FOREIGN KEY(_order) REFERENCES orders(id),
    FOREIGN KEY(product) REFERENCES products(id),
    CONSTRAINT id PRIMARY KEY(_order, product)
);

INSERT INTO states(name) VALUES 
    ('Uttar Pradesh'), 
    ('Punjab'), 
    ('Maharashtra'), 
    ('Tamil Nadu'), 
    ('West Bengal');

INSERT INTO cities(name, state) VALUES 
    ('Kanpur', 1), 
    ('Lucknow', 1), 
    ('Amritsar', 2), 
    ('Ludhiana', 2), 
    ('Chennai', 4), 
    ('Tanjore', 4), 
    ('Mumbai', 3), 
    ('Nagpur', 3), 
    ('Kolkata', 5), 
    ('Siliguri', 5);

INSERT INTO customers (name, sex, dob, email, tel, pwd) VALUES ("Tejashwa Agarwal", 'M', "2002-09-10", "tejawal78dfA@gmail.com", '6392959065', "vashsu09V*"), ("Gauri Singh", 'F', "2003-01-04", "gauri@gmail.com", "6392959060", "gauri1*G");

INSERT INTO deliveryMen (name, sex, dob, email, tel, pwd) VALUES ("Rajesh Sihha", 'M', "1980-10-10", "r.sinha@gmail.com", '6092959065', "rajeshR*1");

INSERT INTO addresses (label, customer, houseinfo, city, pin) VALUES ("Home", 1, "C-1/55, Gulmohar Vihar, Keshav Nagar", 1, '208011'), ("Office", 2, "1283, Y Block, Kidwai Nagar", 7, '108011')

INSERT INTO offers (code, startDate, endDate, discount) VALUES ('SUMMER-10%', '2022-06-01', '2022-06-30', '10'), ('SUMMER-7%', '2022-05-05', '2022-07-30', '7');

INSERT INTO categories (name, offer) VALUES ('Fruits', '1'), ('Vegetables', NULL), ('Spices', '2'), ('Dairy', NULL), ('Beverages', 1);

INSERT INTO products (image, name, description, costPrice, sellingPrice, quantity, unit, category, stock) VALUES ('394525a.jpg', 'Kiwi', 'Fresh Indian Kiwis, Vitamin C, Seasonal', 100, 125, '500', 'g', 6, 50), ('364304a.jpg', 'Sweet Lime', 'Sweet, Citrus, Vitamin C', 80, 84, '500', 'g', 6, 12);
