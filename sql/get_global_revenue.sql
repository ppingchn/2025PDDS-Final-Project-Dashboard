SELECT
    c.country,
    SUM(oi.quantity * oi.unit_price) AS total_revenue,
    ROUND(AVG(JULIANDAY(o.delivery_date) - JULIANDAY(o.order_date)), 1) AS avg_delivery_time,
    ROUND(SUM(oi.quantity * oi.unit_price) / COUNT(DISTINCT o.order_id), 0) AS avg_basket_size

FROM Orders AS o
JOIN Customers AS c ON o.customer_id = c.customer_id
JOIN Order_Items AS oi ON o.order_id = oi.order_id
GROUP BY 
    c.country;