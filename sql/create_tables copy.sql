CREATE TABLE IF NOT EXISTS users (
        user_id INT NOT NULL AUTO_INCREMENT,
        first_name VARCHAR(100) NOT NULL,
        last_name VARCHAR(100) NOT NULL,
        email VARCHAR(100) NOT NULL UNIQUE,
        gender varchar(10) NOT NULL DEFAULT "unknown",
        age int NOT NULL DEFAULT 0,
        phone varchar(20) NOT NULL DEFAULT 0,
        address_1 varchar(200) NOT NULL DEFAULT "unknown",
        address_2 varchar(200) NULL,
        city varchar(100) NOT NULL DEFAULT "unknown",
        country varchar(100) NOT NULL DEFAULT "unknown",
        pincode  INT NOT NULL DEFAULT 0,
        password VARCHAR(255) NOT NULL,
        profile_completion boolean default FALSE,
        date_registered TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (user_id)
    );

CREATE TABLE IF NOT EXISTS food_listings (
        listing_id INT NOT NULL AUTO_INCREMENT,
        food_type VARCHAR(100) NOT NULL,
        quantity INT NOT NULL,
        expiration_date DATE NOT NULL,
        location VARCHAR(255) NOT NULL,
        pincode VARCHAR(10) NOT NULL,
        user_id INT NOT NULL,
        date_listed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (listing_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id)
    );

CREATE TABLE food_listings_2 (
    listing_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    food_name VARCHAR(255) NOT NULL,
    category VARCHAR(255) NOT NULL,
    quantity VARCHAR(255) NOT NULL,
    serving_size VARCHAR(255),
    prepared_date DATE,
    expiration_date DATE NOT NULL,
    pincode VARCHAR(10) NOT NULL, 
    description TEXT NOT NULL,
    special_notes TEXT,
    is_available BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) 
    );

CREATE TABLE IF NOT EXISTS pickups (
        pickup_id INT NOT NULL AUTO_INCREMENT,
        user_id INT NOT NULL,
        listing_id INT NOT NULL,
        pickup_time VARCHAR(100) NOT NULL,
        status ENUM('pending', 'approved', 'rejected') DEFAULT 'pending',
        date_scheduled TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (pickup_id),
        FOREIGN KEY (user_id) REFERENCES users(user_id),
        FOREIGN KEY (listing_id) REFERENCES food_listings(listing_id)
    );

CREATE TABLE IF NOT EXISTS reports (
        report_id INT NOT NULL AUTO_INCREMENT,
        report_name VARCHAR(100),
        generated_by INT NOT NULL,
        date_generated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (report_id),
        FOREIGN KEY (generated_by) REFERENCES users(user_id)
    );