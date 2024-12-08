INSERT INTO users (first_name, last_name, email, gender, age, phone, address_1, address_2, city, country, pincode, password, profile_completion) 
VALUES 
('John', 'Doe', 'john.doe@example.com', 'male', 30, '1234567890', '123 Street', 'Apt 4B', 'New York', 'USA', '10001', 'hashed_password1', TRUE),
('Jane', 'Smith', 'jane.smith@example.com', 'female', 25, '9876543210', '456 Avenue', NULL, 'Los Angeles', 'USA', '90001', 'hashed_password2', TRUE),
('Alice', 'Johnson', 'alice.johnson@example.com', 'female', 35, '1122334455', '789 Road', NULL, 'Chicago', 'USA', '60601', 'hashed_password3', FALSE),
('Bob', 'Brown', 'bob.brown@example.com', 'male', 40, '6677889900', '101 Circle', 'Suite 2A', 'Houston', 'USA', '77001', 'hashed_password4', TRUE),
('Charlie', 'Davis', 'nbrohit@gmail.com', 'other', 28, '4433221100', '202 Square', NULL, 'San Francisco', 'USA', '94101', 'hashed_password5', FALSE);

INSERT INTO food_listings (food_type, quantity, expiration_date, location, pincode, user_id)
VALUES 
    -- Duplicate records across multiple ZIP codes
    ('Apples', 10, '2024-12-31', '123 Main Street', '10001', 1),
    ('Apples', 10, '2024-12-31', '123 Main Street', '10002', 1),
    ('Apples', 10, '2024-12-31', '123 Main Street', '10003', 1),

    ('Bananas', 20, '2024-12-25', '456 Market Street', '10001', 2),
    ('Bananas', 20, '2024-12-25', '456 Market Street', '10002', 2),
    ('Bananas', 20, '2024-12-25', '456 Market Street', '10004', 2),

    ('Oranges', 15, '2024-12-29', '789 Orchard Lane', '10003', 3),
    ('Oranges', 15, '2024-12-29', '789 Orchard Lane', '10005', 3),

    ('Carrots', 12, '2024-12-28', '234 Vegetable Road', '10004', 4),
    ('Carrots', 12, '2024-12-28', '234 Vegetable Road', '10006', 4),

    ('Tomatoes', 25, '2024-12-27', '567 Garden Way', '10001', 5),
    ('Tomatoes', 25, '2024-12-27', '567 Garden Way', '10002', 5),

    ('Lettuce', 18, '2024-12-26', '678 Green Street', '10003', 6),
    ('Lettuce', 18, '2024-12-26', '678 Green Street', '10004', 6),

    ('Broccoli', 22, '2024-12-24', '789 Fresh Lane', '10005', 7),
    ('Broccoli', 22, '2024-12-24', '789 Fresh Lane', '10006', 7),

    ('Peppers', 16, '2024-12-31', '890 Spicy Blvd', '10001', 8),
    ('Peppers', 16, '2024-12-31', '890 Spicy Blvd', '10002', 8),

    ('Mangoes', 10, '2024-12-31', '101 Mango Avenue', '10003', 9),
    ('Mangoes', 10, '2024-12-31', '101 Mango Avenue', '10004', 9),

    ('Strawberries', 12, '2024-12-25', '202 Berry Drive', '10001', 10),
    ('Strawberries', 12, '2024-12-25', '202 Berry Drive', '10005', 10),

    ('Blueberries', 8, '2024-12-27', '303 Blue Street', '10006', 11),
    ('Blueberries', 8, '2024-12-27', '303 Blue Street', '10002', 11),

    ('Peaches', 14, '2024-12-26', '404 Peach Road', '10003', 12),
    ('Peaches', 14, '2024-12-26', '404 Peach Road', '10001', 12),

    ('Plums', 10, '2024-12-28', '505 Plum Alley', '10004', 13),
    ('Plums', 10, '2024-12-28', '505 Plum Alley', '10002', 13),

    ('Cherries', 20, '2024-12-24', '606 Cherry Blvd', '10003', 14),
    ('Cherries', 20, '2024-12-24', '606 Cherry Blvd', '10005', 14),

    ('Kale', 18, '2024-12-29', '707 Kale Street', '10006', 15),
    ('Kale', 18, '2024-12-29', '707 Kale Street', '10004', 15),

    ('Spinach', 22, '2024-12-31', '808 Spinach Road', '10002', 16),
    ('Spinach', 22, '2024-12-31', '808 Spinach Road', '10001', 16),

    ('Milk', 30, '2024-12-27', '909 Dairy Lane', '10001', 17),
    ('Milk', 30, '2024-12-27', '909 Dairy Lane', '10005', 17),

    ('Eggs', 40, '2024-12-26', '123 Egg Blvd', '10003', 18),
    ('Eggs', 40, '2024-12-26', '123 Egg Blvd', '10004', 18),

    ('Cheese', 25, '2024-12-28', '234 Cheese Way', '10002', 19),
    ('Cheese', 25, '2024-12-28', '234 Cheese Way', '10003', 19),

    ('Chicken', 10, '2024-12-31', '456 Poultry Lane', '10001', 20),
    ('Chicken', 10, '2024-12-31', '456 Poultry Lane', '10002', 20);

INSERT INTO food_listings_2 (user_id, food_name, category, quantity, serving_size, prepared_date, expiration_date, pincode, description, special_notes) 
VALUES 
(1, 'Apples', 'Fruits', '5 lbs', '1 serving', '2024-12-06', '2024-12-12', '10001', 'Fresh apples from a local farm.', 'Keep refrigerated.'),
(2, 'Milk', 'Dairy', '2 gallons', '1 serving', '2024-12-05', '2024-12-10', '90001', 'Whole milk in sealed containers.', 'Store in a cool place.'),
(3, 'Bread', 'Grains', '3 loaves', '1 serving', '2024-12-06', '2024-12-15', '60601', 'Homemade bread.', 'Best when toasted.'),
(4, 'Chicken Curry', 'Prepared Meals', '4 containers', '1 serving', '2024-12-06', '2024-12-08', '77001', 'Spicy chicken curry.', 'Consume within 2 days.'),
(5, 'Cookies', 'Snacks', '20 pieces', '1 serving', '2024-12-05', '2024-12-15', '94101', 'Chocolate chip cookies.', 'Store in an airtight container.');

INSERT INTO pickups (user_id, listing_id, pickup_time, status) 
VALUES 
(1, 1, '2024-12-07 10:00:00', 'pending'),
(2, 2, '2024-12-07 12:00:00', 'approved'),
(3, 3, '2024-12-08 14:00:00', 'rejected'),
(4, 4, '2024-12-09 16:00:00', 'pending'),
(5, 5, '2024-12-10 18:00:00', 'approved');

INSERT INTO reports (report_name, generated_by) 
VALUES 
('Monthly Activity Report', 1),
('User Engagement Report', 2),
('Inventory Summary', 3),
('Pickup Status Report', 4),
('Food Waste Reduction', 5);