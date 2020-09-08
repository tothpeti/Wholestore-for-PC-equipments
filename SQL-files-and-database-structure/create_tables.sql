use Raktarozo

GO

ALTER TABLE Products DROP CONSTRAINT fk_prod_supplier_id;
ALTER TABLE Suppliers DROP CONSTRAINT fk_sup_user_id;
ALTER TABLE Orders DROP CONSTRAINT fk_orders_product_id, fk_orders_customer_id;
ALTER TABLE Customers DROP CONSTRAINT fk_customers_user_id;

DROP TABLE IF EXISTS Products;
DROP TABLE IF EXISTS Suppliers;
DROP TABLE IF EXISTS Orders;
DROP TABLE IF EXISTS Customers;
DROP TABLE IF EXISTS Users

CREATE TABLE Users (
    [id] TINYINT IDENTITY (1, 1) PRIMARY KEY NOT NULL,
    [account_name] NVARCHAR(20) UNIQUE NOT NULL ,
    [password] NVARCHAR(25) UNIQUE NOT NULL,
	account_type nvarchar(15) NOT NULL
);

CREATE TABLE Suppliers (
    [id] TINYINT IDENTITY (1, 1) PRIMARY KEY NOT NULL,
    [name] NVARCHAR(70) UNIQUE NOT NULL,
    [userId] TINYINT NOT NULL,
    CONSTRAINT fk_sup_user_id FOREIGN KEY (userId) REFERENCES Users(id) ON DELETE CASCADE
);

CREATE TABLE Products (
    [id] INT IDENTITY (1, 1) PRIMARY KEY NOT NULL,
    [name] NVARCHAR(70) UNIQUE NOT NULL,
	[type] NVARCHAR(30) NOT NULL,
    [quantity] TINYINT NOT NULL,
    [price] MONEY NOT NULL,
    [supplierId] TINYINT NOT NULL,
    CONSTRAINT fk_prod_supplier_id FOREIGN KEY (supplierId) REFERENCES Suppliers(id) ON DELETE CASCADE
);

CREATE TABLE Customers (
    [id] TINYINT IDENTITY (1, 1) PRIMARY KEY NOT NULL,
    [first_name] NVARCHAR(50) NOT NULL,
    [last_name] NVARCHAR(50) NOT NULL,
    [balance] MONEY NOT NULL,
    [userId] TINYINT NOT NULL ,
    CONSTRAINT fk_customers_user_id FOREIGN KEY (userId) REFERENCES Users(id) ON DELETE CASCADE
);

CREATE TABLE Orders (
    [id] INT IDENTITY (1, 1) PRIMARY KEY NOT NULL,
    [total_quantity] TINYINT NOT NULL,
    [total_price] INT NOT NULL,
    [date] DATETIME NOT NULL,
    [productId] INT NOT NULL,
    [customerId] TINYINT NOT NULL,
	[status] INT NOT NULL DEFAULT 0,
    CONSTRAINT fk_orders_product_id FOREIGN KEY (productId) REFERENCES Products(id) ON DELETE CASCADE,
    CONSTRAINT fk_orders_customer_id FOREIGN KEY (customerId) REFERENCES Customers(id)
);

GO