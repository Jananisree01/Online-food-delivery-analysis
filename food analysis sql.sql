CREATE DATABASE food_delivery_db;
USE food_delivery_db;
 Top 10 spending customers

SELECT customer_id,
       SUM(order_value) AS total_spent
FROM orders
GROUP BY customer_id
ORDER BY total_spent DESC
LIMIT 10;

 Age Group vs Order Value

SELECT age_group,
   AVG(order_value) AS avg_order_value
FROM orders
GROUP BY age_group;

Weekend vs Weekday Orders
SELECT day_type,
       COUNT(*) AS total_orders
FROM orders
GROUP BY day_type;

Monthly Revenue Trend
SELECT order_month,
       SUM(order_value) AS monthly_revenue
FROM orders
GROUP BY order_month
ORDER BY order_month;

Profit Margin %
SELECT 
    CASE 
        WHEN discount > 0 THEN 'With Discount'
        ELSE 'No Discount'
    END AS discount_type,
    AVG(profit) AS avg_profit
FROM orders
GROUP BY discount_type;


6.High Revenue Cities
SELECT city,
       SUM(order_value) AS total_revenue
FROM orders
GROUP BY city
ORDER BY total_revenue DESC;

7.Average Delivery Time by City
SELECT city,
       AVG(delivery_time) AS avg_delivery_time
FROM orders
GROUP BY city;

8.Distance vs Delivery Delay
SELECT 
    CASE 
        WHEN distance < 5 THEN 'Short'
        WHEN distance BETWEEN 5 AND 10 THEN 'Medium'
        ELSE 'Long'
    END AS distance_category,
    AVG(delivery_time) AS avg_delivery_time
FROM orders
GROUP BY distance_category;

9.Top Rated Restaurants
SELECT restaurant_name,
       AVG(customer_rating) AS avg_rating
FROM orders
GROUP BY restaurant_name
ORDER BY avg_rating DESC
LIMIT 10;

10.Cancellation Rate by Restaurant
SELECT restaurant_name,
       SUM(CASE WHEN order_status='Cancelled' THEN 1 ELSE 0 END) 
       / COUNT(*) * 100 AS cancellation_rate
FROM orders
GROUP BY restaurant_name
ORDER BY cancellation_rate DESC;

11.Peak Hour Demand
SELECT peak_hour,
       COUNT(*) AS total_orders
FROM orders
GROUP BY peak_hour;

12.Payment Mode Preference
SELECT payment_mode,
       COUNT(*) AS total_orders
FROM orders
GROUP BY payment_mode
ORDER BY total_orders DESC;

13.Cancellation Reason Analysis
SELECT cancellation_reason,
       COUNT(*) AS total_count
FROM orders
WHERE order_status = 'Cancelled'
GROUP BY cancellation_reason
ORDER BY total_count DESC;

14.Revenue by Cuisine
`SELECT cuisine,
       COUNT(*) AS total_orders,
       SUM(order_value) AS total_revenue,
       AVG(customer_rating) AS avg_rating
FROM orders
GROUP BY cuisine
ORDER BY total_revenue DESC;

15.DELIVERY RATING vs DELIVERY TIME
SELECT 
    CASE
        WHEN delivery_time <= 30 THEN 'Fast (<=30 mins)'
        WHEN delivery_time BETWEEN 31 AND 45 THEN 'Medium (31-45 mins)'
        ELSE 'Slow (>45 mins)'
    END AS delivery_speed,
    AVG(customer_rating) AS avg_rating
FROM orders
GROUP BY delivery_speed;

DESCRIBE orders;

USE food_delivery_db;

CUISINE-WISE PERFORMANCE

SELECT cuisine_type,
       COUNT(*) AS total_orders,
       SUM(order_value) AS total_revenue,
       AVG(restaurant_rating) AS avg_restaurant_rating
FROM orders
GROUP BY cuisine_type
ORDER BY total_revenue DESC;

DELIVERY RATING vs DELIVERY TIME
SELECT 
    CASE
        WHEN delivery_time_min <= 30 THEN 'Fast (<=30 mins)'
        WHEN delivery_time_min BETWEEN 31 AND 45 THEN 'Medium (31-45 mins)'
        ELSE 'Slow (>45 mins)'
    END AS delivery_speed_category,
    AVG(delivery_rating) AS avg_delivery_rating
FROM orders
GROUP BY delivery_speed_category;

IMPACT OF DISCOUNTS ON PROFIT
SELECT 
    CASE 
        WHEN discount_applied > 0 THEN 'With Discount'
        ELSE 'No Discount'
    END AS discount_type,
    AVG(profit_margin) AS avg_profit_margin
FROM orders
GROUP BY discount_type;

Discount Level vs Profit Margin
SELECT 
    ROUND(discount_applied, 0) AS discount_value,
    AVG(profit_margin) AS avg_profit_margin
FROM orders
GROUP BY discount_value
ORDER BY discount_value;

Average Delivery Time by City
SELECT city,
       AVG(delivery_time_min) AS avg_delivery_time
FROM orders
GROUP BY city
ORDER BY avg_delivery_time;

Distance vs Delivery Time
SELECT 
    CASE 
        WHEN distance_km < 5 THEN 'Short Distance'
        WHEN distance_km BETWEEN 5 AND 10 THEN 'Medium Distance'
        ELSE 'Long Distance'
    END AS distance_category,
    AVG(delivery_time_min) AS avg_delivery_time
FROM orders
GROUP BY distance_category;








