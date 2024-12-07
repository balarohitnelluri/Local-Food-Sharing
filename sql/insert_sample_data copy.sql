INSERT INTO users (first_name, last_name, email, gender, age, phone, address_1, address_2, city, country, pincode, password, profile_completion) 
VALUES 
('John', 'Doe', 'john.doe@example.com', 'male', 30, '1234567890', '123 Street', 'Apt 4B', 'New York', 'USA', '10001', 'hashed_password1', TRUE),
('Jane', 'Smith', 'jane.smith@example.com', 'female', 25, '9876543210', '456 Avenue', NULL, 'Los Angeles', 'USA', '90001', 'hashed_password2', TRUE),
('Alice', 'Johnson', 'alice.johnson@example.com', 'female', 35, '1122334455', '789 Road', NULL, 'Chicago', 'USA', '60601', 'hashed_password3', FALSE),
('Bob', 'Brown', 'bob.brown@example.com', 'male', 40, '6677889900', '101 Circle', 'Suite 2A', 'Houston', 'USA', '77001', 'hashed_password4', TRUE),
('Charlie', 'Davis', 'nbrohit@gmail.com', 'other', 28, '4433221100', '202 Square', NULL, 'San Francisco', 'USA', '94101', 'hashed_password5', FALSE);

 INSERT INTO food_listings (food_type, quantity, expiration_date, location, pincode, user_id)
                VALUES 
                ('Apples', 10, '2024-12-31', '123 Main Street', '10001', 1),
                ('Bananas', 20, '2024-12-25', '456 Market Street', '10002', 2);

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