SELECT 
    o.order_id,
    o.customer_id,
    o.order_date,
    o.total_amount,
    SUM(o.total_amount) OVER (PARTITION BY o.customer_id ORDER BY o.order_date) AS running_total
FROM orders o
ORDER BY o.customer_id, o.order_date;
