create database amazon_project;
use amazon_project;
CREATE TABLE amazon_data (
    user_id VARCHAR(20),
    product_id VARCHAR(20),
    category VARCHAR(50),
    subcategory VARCHAR(50),
    brand VARCHAR(50),
    price DECIMAL(10,2),
    discount DECIMAL(5,2),
    final_price DECIMAL(10,2),
    rating DECIMAL(2,1),
    review_count INT,
    stock INT,
    seller_id VARCHAR(20),
    seller_rating DECIMAL(2,1),
    purchase_date DATE,
    shipping_time_days INT,
    location VARCHAR(50),
    device VARCHAR(20),
    payment_method VARCHAR(50),
    is_returned VARCHAR(10),
    delivery_status VARCHAR(50)
);
SHOW VARIABLES LIKE 'secure_file_priv';
LOAD DATA INFILE 'C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/amazon_data.csv'
INTO TABLE amazon_data
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
 select * from amazon_data;
 SELECT 
    COUNT(*) AS total_rows,
    COUNT(DISTINCT user_id) AS unique_users
FROM amazon_data;
SELECT 
    COUNT(*) AS total_orders,
    SUM(final_price) AS total_revenue
FROM amazon_data;
SELECT 
    category,
    COUNT(*) AS total_orders,
    SUM(final_price) AS revenue
FROM amazon_data
GROUP BY category
ORDER BY revenue DESC;

SELECT 
    subcategory,
    COUNT(*) AS total_orders,
    SUM(final_price) AS revenue
FROM amazon_data
GROUP BY subcategory
ORDER BY revenue DESC
LIMIT 10;

SELECT 
    is_returned,
    COUNT(*) AS total_orders
FROM amazon_data
GROUP BY is_returned;

SELECT 
    category,
    AVG(rating) AS avg_rating
FROM amazon_data
GROUP BY category
ORDER BY avg_rating DESC;

SELECT 
    delivery_status,
    COUNT(*) AS total_orders,
    AVG(shipping_time_days) AS avg_delivery_days
FROM amazon_data
GROUP BY delivery_status;

SELECT 
    payment_method,
    COUNT(*) AS total_orders
FROM amazon_data
GROUP BY payment_method
ORDER BY total_orders DESC;

SELECT 
    location,
    COUNT(*) AS total_orders,
    SUM(final_price) AS revenue
FROM amazon_data
GROUP BY location
ORDER BY revenue DESC
LIMIT 5;
