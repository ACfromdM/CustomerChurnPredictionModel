WITH recent_tx AS (
  SELECT
    customer_id,
    transaction_date,
    amount
  FROM
    transactions
  WHERE
    transaction_date >= DATEADD(year, -1, CURRENT_DATE)
)

SELECT
    customer_id,
    COUNT(*)                            AS num_transactions,
    SUM(amount)                         AS total_spend,
    MAX(transaction_date)               AS last_transaction_date,
    DATEDIFF(day, MAX(transaction_date), CURRENT_DATE) AS days_since_last
FROM
    recent_tx
GROUP BY
    customer_id;