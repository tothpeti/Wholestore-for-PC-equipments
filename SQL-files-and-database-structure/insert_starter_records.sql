USE Raktarozo

GO
INSERT INTO Users(account_name, password, account_type)
    VALUES
           ('cseri', 'cseri123', 'customer'),
           ('kovi', 'kovi123', 'customer'),
           ('jobs', 'jobs123', 'customer'),
           ('gates', 'gates123', 'customer'),
           ('logi', 'logi123', 'supplier'),
           ('giga', 'giga123', 'supplier')


INSERT INTO Suppliers(name, userId)
    VALUES
           ('Logitech', 5),
           ('Gigabyte', 6)

INSERT INTO Products(name, type, quantity, price, supplierId)
    VALUES
           ('Logitech MX Master 3', 'mouse',10, 30000, 1),
           ('Logitech MX Vertical', 'mouse', 10, 25000, 1),
           ('Logitech Mouse M100', 'mouse', 20, 9000, 1),
           ('Logitech MX Keys', 'keyboard', 15, 32000, 1),
           ('Logitech Ergo K860', 'keyboard', 5, 40000, 1),
           ('Gigabyte GTX 1660 Super OC 6GB', 'gpu', 15, 89000, 2),
           ('Gigabyte Aorus CV27Q-EK', 'monitor', 10, 165000, 2),
           ('Gigabyte Force K81', 'keyboard', 3, 18000, 2),
           ('Gigabyte Aorus B450 Pro', 'motherboard', 1, 36500, 2),
           ('Gigabyte Z390 Gaming X', 'motherboard', 4, 47000, 2)

INSERT INTO Customers(first_name, last_name, userId, balance)
    VALUES
           ('Virag', 'Cserepes', 1, 150000),
           ('Jozsef', 'Kovacs', 2, 50000),
           ('Steve', 'Jobs', 3, 1000000),
           ('Bill', 'Gates', 4, 1000000)
GO