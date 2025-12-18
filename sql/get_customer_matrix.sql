SELECT 
    c.country,
    STRFTIME('%Y-%m-01', o.order_date) as full_date,
    SUM(oi.quantity * oi.unit_price) as total_spent
FROM Orders o 
JOIN Customers c ON o.customer_id = c.customer_id 
JOIN Order_Items oi ON o.order_id = oi.order_id 
WHERE 
    o.order_status IN ('Pending', 'Delivered', 'Shipped')
    AND (? IS NULL OR STRFTIME('%Y', o.order_date) = ?)
    AND (? IS NULL OR c.country = ?)
GROUP BY 
    c.country, full_date
ORDER BY 
    full_date;