SELECT
    c.customer_id,
    c.signup_date,
    d.age,
    d.gender,
    d.region
FROM
    customers AS c
JOIN
    customer_demographics AS d
  ON c.customer_id = d.customer_id;