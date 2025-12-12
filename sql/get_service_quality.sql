SELECT
    STRFTIME('%Y-%m-01', o.order_date) AS month,
    AVG(julianday(o.delivery_date) - julianday(o.order_date)) AS avg_shipping_days,
    AVG(r.rating) AS avg_review_score
FROM
    Orders o
LEFT JOIN
    Reviews r
ON
    o.order_id = r.order_id
WHERE
    o.delivery_date IS NOT NULL
    AND (? IS NULL OR o.country = ?)
GROUP BY
    STRFTIME('%Y-%m-01', o.order_date)
ORDER BY
    month;