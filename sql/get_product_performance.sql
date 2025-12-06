SELECT
p.category,
SUM(oi.quantity) AS total_sales_volume,
AVG(r.rating) AS average_customer_rating
FROM Products as p
JOIN Order_Items as oi ON p.product_id = oi.product_id
JOIN Reviews as r on oi.order_id = r.order_id
GROUP BY p.category
ORDER BY total_sales_volume DESC;