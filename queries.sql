-- Monthly revenue
SELECT strftime('%Y-%m', "Order Date") AS Month,
       SUM(Sales) AS Revenue
FROM orders
GROUP BY Month
ORDER BY Month;

-- Top 5 customers
SELECT "Customer Name", SUM(Sales) AS Revenue
FROM orders
GROUP BY "Customer Name"
ORDER BY Revenue DESC
LIMIT 5;

-- Sales by category
SELECT Category, SUM(Sales) AS TotalSales
FROM orders
GROUP BY Category
ORDER BY TotalSales DESC;
