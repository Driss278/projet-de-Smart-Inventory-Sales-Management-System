USE shema;

INSERT INTO saleapp_product (name, category, price, quantity_in_stock)
VALUES
('IPHONE 17 PRO', 'phone', 15000.00, 15),
('Laptop HP', 'informatique', 7500.50, 10),
('Souris Logitech', 'accessoires', 150.00, 50),
('Clavier mécanique', 'accessoires', 450.99, 20),
('Écran Samsung 24"', 'informatique', 1800.00, 15);
INSERT INTO saleapp_order (order_date, customer_id)
VALUES
(NOW(), 1),
(NOW(), 2);
INSERT INTO saleapp_customer (name, email)
VALUES ('Ali Benali','ali@gmail.com'),
       ('Sara El Amrani','sara@gmail.com');
INSERT INTO saleapp_orderitem (quantity, order_id, product_id)
VALUES (1, 1, 1),
       (2, 1, 2),
       (1, 2, 2);
UPDATE productmanagement.saleapp_orderitem oi
JOIN productmanagement.saleapp_product p
  ON p.id = oi.product_id
SET oi.unit_price = p.price;