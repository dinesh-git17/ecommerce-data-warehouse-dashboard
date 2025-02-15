WITH product_sales AS (
    SELECT 
        p.product_id,
        p.name,
        SUM(od.quantity * od.price_at_order) AS total_sales
    FROM products p
    JOIN order_details od ON p.product_id = od.product_id
    GROUP BY p.product_id, p.name
)
SELECT *
FROM product_sales
ORDER BY total_sales DESC
LIMIT 10;
