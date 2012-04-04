INSERT INTO CommerceUser (email, password, first_name, last_name) VALUES ('dan@denimgroup.com', 'mypassword', 'Dan', 'Cornell')
SELECT * FROM CommerceUser WHERE email = 'dan@denimgroup.com' AND password = 'mypassword'
INSERT INTO CreditCard (type, number, expiration, CVV) VALUES ('VISA', '41111111111111111111', '0315', '123')
INSERT INTO Order (user_id, creditcard_id, tax, shipping, total) VALUES (1, 1, 2.0, 10.0, 27.0)
INSERT INTO OrderItem (order_id, product_id, product_name, quantity, price) VALUES (1, 1, 'Extra Large Paperclips', 2, 7.5)
SELECT * FROM Product
SELECT date, total FROM Order WHERE user_id = 1
SELECT date, tax, shipping, total WHERE order_id = 1
SELECT product_id, product_name, quantity, price FROM OrderItem WHERE order_id = 1
