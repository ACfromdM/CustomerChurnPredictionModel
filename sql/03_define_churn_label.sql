-- Defines churn flag: churned = 1 if no activity in the last 90 days

WITH last_tx AS (
  SELECT
    customer_id,
    MAX(transaction_date) AS last_transaction_date
  FROM
    transactions
  GROUP BY
    customer_id
)

SELECT
    customer_id,
    CASE
      WHEN DATEDIFF(day, last_transaction_date, CURRENT_DATE) > 90 THEN 1
      ELSE 0
    END AS churned
FROM
    last_tx;