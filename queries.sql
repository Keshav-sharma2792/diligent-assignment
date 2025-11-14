-- Consolidated customer order report
SELECT
    c.full_name AS customer_name,
    o.order_id,
    p.product_name,
    oi.quantity,
    p.price,
    oi.quantity * p.price AS total_amount
FROM customers AS c
JOIN orders AS o
    ON o.customer_id = c.customer_id
JOIN order_items AS oi
    ON oi.order_id = o.order_id
JOIN products AS p
    ON p.product_id = oi.product_id
LEFT JOIN payments AS pay
    ON pay.order_id = o.order_id
ORDER BY
    c.full_name,
    o.order_id;

