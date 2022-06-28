getStates = """ SELECT * FROM states """ ;

getCities = """ SELECT id, name FROM cities where state = {} """

addUser = """ INSERT INTO customers(name, sex, dob, email, tel, pwd) VALUES ('{name}', '{sex}', '{dob}', '{email}', '{tel}', '{pwd}') """

addAddress = """ INSERT INTO address(label, customer, houseInfo, city, pincode) VALUES ('{label}', {customer_id}, '{address}', {city}, '{pin}') """

doesExist = """ SELECT COUNT(email) as found FROM customers WHERE email LIKE '{}' """

checkIfPwdIsForEmail = """ SELECT EXISTS (SELECT * FROM customers WHERE email = '{email}' AND pwd = '{pwd}' ) AS matched """

getProducts = """ SELECT * FROM products """

getId = """ SELECT id AS id FROM customers WHERE email like '{email}' """