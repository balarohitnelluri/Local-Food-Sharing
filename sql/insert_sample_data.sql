INSERT INTO users (first_name, last_name, email, password)
                VALUES 
                ('John', 'Doe', 'nbrohit@gmail.com', SHA2('AbcD$545', 256)),
                ('Jane', 'Smith', 'jane.smith@example.com', SHA2('mypassword', 256));

INSERT INTO food_listings (food_type, quantity, expiration_date, location, pincode, user_id)
                VALUES 
                ('Apples', 10, '2024-12-31', '123 Main Street', '10001', 1),
                ('Bananas', 20, '2024-12-25', '456 Market Street', '10002', 2);

INSERT INTO pickups (user_id, listing_id, pickup_time, status)
                VALUES 
                (1, 1, '2024-11-25 10:00', 'pending'),
                (2, 2, '2024-11-26 14:00', 'approved');

INSERT INTO reports (report_name, generated_by)
                VALUES 
                ('Monthly Report - November', 1),
                ('Yearly Summary - 2024', 2);