/*1. What are the top 5 brands by receipts scanned for most recent month?*/

SELECT b.name AS brandName, COUNT(r.receipt_id) AS receipt_count FROM Brands b
INNER JOIN Receipts r ON b.brand_id = r.brand_id 
WHERE r.purchaseDate >= DATE_SUB(DATE_FORMAT(CURRENT_DATE, '%Y-%m-01'), INTERVAL 1 MONTH) AND r.purchaseDate < DATE_FORMAT(CURRENT_DATE, '%Y-%m-01')
GROUP BY b.name 
ORDER BY receipt_count DESC LIMIT 5;

/*2.How does the ranking of the top 5 brands by receipts scanned for the recent month compare to the ranking for the previous month?*/

WITH recent_month AS (
    SELECT b.name AS brandName, COUNT(r.receipt_id) AS receipt_count FROM Brands b
    INNER JOIN Receipts r ON b.brand_id = r.brand_id
    WHERE r.purchaseDate >= DATE_SUB(DATE_FORMAT(CURRENT_DATE, '%Y-%m-01'), INTERVAL 1 MONTH) AND r.purchaseDate < DATE_FORMAT(CURRENT_DATE, '%Y-%m-01')
    GROUP BY b.name
    ORDER BY receipt_count DESC LIMIT 5
),
previous_month AS (
    SELECT b.name AS brandName, COUNT(r.receipt_id) AS receipt_count FROM Brands b
    INNER JOIN Receipts r ON b.brand_id = r.brand_id
    WHERE r.purchaseDate >= DATE_SUB(DATE_FORMAT(CURRENT_DATE, '%Y-%m-01'), INTERVAL 2 MONTH) AND r.purchaseDate < DATE_SUB(DATE_FORMAT(CURRENT_DATE, '%Y-%m-01'), INTERVAL 1 MONTH)
    GROUP BY b.name
    ORDER BY receipt_count DESC LIMIT 5
)
SELECT rm.brandName AS recentBrand, rm.receipt_count AS recentCount, pm.brandName AS previousBrand, pm.receipt_count AS previousCount FROM recent_month rm
LEFT JOIN previous_month pm ON rm.brandName = pm.brandName
UNION
SELECT pm.brandName AS recentBrand,NULL AS recentCount,pm.brandName AS previousBrand, pm.receipt_count AS previousCount FROM previous_month pm
LEFT JOIN recent_month rm ON pm.brandName = rm.brandName
WHERE rm.brandName IS NULL
ORDER BY recentCount DESC, previousCount DESC;


/*3.When considering average spend from receipts with 'rewardsReceiptStatus’ of ‘Accepted’ or ‘Rejected’, which is greater?*/

SELECT rewardsReceiptStatus, AVG(totalSpent) AS average_spend FROM Receipts
WHERE rewardsReceiptStatus IN ('Accepted', 'Rejected')
GROUP BY rewardsReceiptStatus;


/*4.When considering total number of items purchased from receipts with 'rewardsReceiptStatus’ of ‘Accepted’ or ‘Rejected’, which is greater?*/

SELECT rewardsReceiptStatus, SUM(purchasedItemCount) AS total_items FROM Receipts
WHERE rewardsReceiptStatus IN ('Accepted', 'Rejected')
GROUP BY rewardsReceiptStatus;



/*5.Which brand has the most spend among users who were created within the past 6 months?*/

SELECT b.name AS brandName, SUM(r.totalSpent) AS totalSpent FROM Users u
JOIN Receipts r 
ON u.user_id = r.user_id
JOIN Brands b 
ON r.brand_id = b.brand_id
WHERE u.createdDate >= DATE_SUB(CURRENT_DATE, INTERVAL 6 MONTH)
GROUP BY b.name
ORDER BY totalSpent DESC LIMIT 1;

/*6.Which brand has the most transactions among users who were created within the past 6 months?*/

SELECT b.name AS brandName, COUNT(r.receipt_id) AS transactionCount FROM Users u
JOIN Receipts r 
ON u.user_id = r.user_id
JOIN Brands b 
ON r.brand_id = b.brand_id
WHERE u.createdDate >= DATE_SUB(CURRENT_DATE, INTERVAL 6 MONTH)
GROUP BY b.name
ORDER BY transactionCount DESC LIMIT 1;
