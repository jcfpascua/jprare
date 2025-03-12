CREATE DATABASE IF NOT EXISTS jprare_database;
USE jprare_database;

CREATE TABLE IF NOT EXISTS City (
    cityID INT AUTO_INCREMENT PRIMARY KEY,
    cityName VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS Barangay (
    barangayID INT AUTO_INCREMENT PRIMARY KEY,
    barangayName VARCHAR(100) NOT NULL,
    cityID INT,
    FOREIGN KEY (cityID) REFERENCES City(cityID)
);

CREATE TABLE IF NOT EXISTS Street (
    streetID INT AUTO_INCREMENT PRIMARY KEY,
    streetname VARCHAR(100) NOT NULL,
    barangayID INT,
    FOREIGN KEY (barangayID) REFERENCES Barangay(barangayID)
);

CREATE TABLE IF NOT EXISTS Address (
    addressID INT AUTO_INCREMENT PRIMARY KEY,
    description VARCHAR(255),
    line VARCHAR(100),
    streetID INT,
    FOREIGN KEY (streetID) REFERENCES Street(streetID)
);

CREATE TABLE IF NOT EXISTS Customer (
    customerID INT AUTO_INCREMENT PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    addressID INT,
    FOREIGN KEY (addressID) REFERENCES Address(addressID)
);

CREATE TABLE IF NOT EXISTS Merchant (
    merchantID INT AUTO_INCREMENT PRIMARY KEY,
    merchant_name VARCHAR(100) NOT NULL,
    addressID INT,
    FOREIGN KEY (addressID) REFERENCES Address(addressID)
);

CREATE TABLE IF NOT EXISTS Item (
    itemID INT AUTO_INCREMENT PRIMARY KEY,
    item_name VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS Customer_Order (
    customer_orderID INT AUTO_INCREMENT PRIMARY KEY,
    customerID INT,
    order_date DATE NOT NULL,
    merchantID INT,
    FOREIGN KEY (customerID) REFERENCES Customer(customerID),
    FOREIGN KEY (merchantID) REFERENCES Merchant(merchantID)
);

CREATE TABLE IF NOT EXISTS Customer_Order_Details (
    customer_order_detailsID INT AUTO_INCREMENT PRIMARY KEY,
    customer_orderID INT,
    item_id INT,
    quantity INT NOT NULL,
    total DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (customer_orderID) REFERENCES Customer_Order(customer_orderID),
    FOREIGN KEY (item_id) REFERENCES Item(itemID)
);

CREATE TABLE IF NOT EXISTS Merchant_Order (
    merchant_orderID INT AUTO_INCREMENT PRIMARY KEY,
    merchantID INT,
    merchant_name VARCHAR(100),
    itemID INT,
    FOREIGN KEY (merchantID) REFERENCES Merchant(merchantID),
    FOREIGN KEY (itemID) REFERENCES Item(itemID)
);

CREATE TABLE IF NOT EXISTS Merchant_Order_Details (
    merchant_order_detailsID INT AUTO_INCREMENT PRIMARY KEY,
    merchant_orderID INT,
    quantity INT NOT NULL,
    details TEXT,
    FOREIGN KEY (merchant_orderID) REFERENCES Merchant_Order(merchant_orderID)
);

CREATE TABLE IF NOT EXISTS Expense_Type (
    expense_typeID INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS Expense (
    expenseID INT AUTO_INCREMENT PRIMARY KEY,
    expense_date DATE NOT NULL,
    total DECIMAL(10, 2) NOT NULL,
    merchantID INT,
    qty INT,
    title VARCHAR(100),
    FOREIGN KEY (merchantID) REFERENCES Merchant(merchantID)
);

CREATE TABLE IF NOT EXISTS Expense_Details (
    expenseID INT,
    expense_typeID INT,
    amount DECIMAL(10, 2) NOT NULL,
    PRIMARY KEY (expenseID, expense_typeID),
    FOREIGN KEY (expenseID) REFERENCES Expense(expenseID),
    FOREIGN KEY (expense_typeID) REFERENCES Expense_Type(expense_typeID)
);

CREATE TABLE IF NOT EXISTS Contact_Type (
    contact_typeID INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS Contact_Details (
    contactID INT AUTO_INCREMENT PRIMARY KEY,
    customerID INT,
    value VARCHAR(255) NOT NULL,
    FOREIGN KEY (customerID) REFERENCES Customer(customerID)
);

CREATE TABLE IF NOT EXISTS Supplier (
    supplierID INT AUTO_INCREMENT PRIMARY KEY,
    supplier_name VARCHAR(100) NOT NULL,
    contact VARCHAR(100),
    addressID INT,
    FOREIGN KEY (addressID) REFERENCES Address(addressID)
);

INSERT INTO City (cityName) VALUES 
('Manila'), ('Quezon City'), ('Cebu City'), ('Davao City');

INSERT INTO Barangay (barangayName, cityID) VALUES 
('Poblacion', 1), ('Malate', 1), ('Diliman', 2), ('Cubao', 2);

INSERT INTO Street (streetname, barangayID) VALUES 
('Rizal Avenue', 1), ('Taft Avenue', 2), ('Commonwealth Avenue', 3), ('EDSA', 4);

INSERT INTO Address (description, line, streetID) VALUES 
('Near Park', 'Building A', 1), ('Corner Mall', 'Unit 101', 2), 
('Business District', 'Tower 1', 3), ('Residential Area', 'House 5', 4);

INSERT INTO Customer (customer_name, addressID) VALUES 
('John Doe', 1), ('Jane Smith', 2), ('Robert Johnson', 3);

INSERT INTO Merchant (merchant_name, addressID) VALUES 
('ABC Store', 1), ('XYZ Shop', 2), ('123 Mart', 3);

INSERT INTO Item (item_name) VALUES 
('Laptop'), ('Smartphone'), ('Tablet'), ('Headphones'), ('Monitor');

INSERT INTO Contact_Type (title) VALUES 
('Email'), ('Phone'), ('Mobile'), ('Fax');

INSERT INTO Expense_Type (title) VALUES 
('Utilities'), ('Rent'), ('Salary'), ('Supplies'), ('Miscellaneous');

INSERT INTO Supplier (supplier_name, contact, addressID) VALUES 
('Tech Supplies Inc.', '123-456-7890', 1), 
('Office Essentials', '987-654-3210', 2), 
('Hardware Plus', '555-123-4567', 3);
