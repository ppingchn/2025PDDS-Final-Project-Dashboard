SELECT 
		c.customer_id, 
		c.country,
		strftime('%Y', o.order_date) AS year, 
		strftime('%m', o.order_date) AS month, 
		SUM(oi.quantity * oi.unit_price) AS total_spent, 
		COUNT(DISTINCT o.order_id) AS total_frequency_purchase 
FROM Orders o JOIN Customers c ON o.customer_id = c.customer_id 
JOIN Order_Items oi ON o.order_id = oi.order_id 
WHERE o.order_status IN ('Pending', 'Delivered', 'Shipped') 
GROUP BY c.country, year,month