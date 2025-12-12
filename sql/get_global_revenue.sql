SELECT
        c.country,
        o.order_date,
        o.delivery_date,
        oi.quantity,
        oi.unit_price,
        o.order_id
FROM Orders AS o
JOIN Customers AS c ON o.customer_id = c.customer_id
JOIN Order_Items AS oi ON o.order_id = oi.order_id