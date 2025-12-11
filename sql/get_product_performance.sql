SELECT
    p.category,
    SUM(oi.quantity) AS total_sales_volume,
    AVG(r.rating) AS average_customer_rating
FROM Products as p
JOIN Order_Items as oi ON p.product_id = oi.product_id
JOIN Orders as o ON oi.order_id = o.order_id
JOIN Customers as c ON o.customer_id = c.customer_id
JOIN Reviews as r ON oi.order_id = r.order_id
WHERE (? IS NULL OR c.country = ?)
GROUP BY p.category
ORDER BY total_sales_volume DESC;