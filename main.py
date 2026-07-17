# STEP 0

# SQL Library and Pandas Library
import sqlite3
import pandas as pd

# Connect to the database
conn = sqlite3.connect('data.sqlite')

pd.read_sql("""SELECT * FROM sqlite_master""", conn)

# STEP 1
# Return the first and last names for employees in Boston
q_boston = """
SELECT e.firstName, e.lastName
FROM employees e
JOIN offices o ON e.officeCode = o.officeCode
WHERE o.city = 'Boston'
"""
df_boston = pd.read_sql(q_boston, conn)

# STEP 2
# Return offices that have zero employees
q_zero_emp = """
SELECT o.officeCode, o.city
FROM offices o
LEFT JOIN employees e ON o.officeCode = e.officeCode
GROUP BY o.officeCode, o.city
HAVING COUNT(e.employeeNumber) = 0
"""
df_zero_emp = pd.read_sql(q_zero_emp, conn)

# STEP 3
# Return all employees with their office city and state
q_employee = """
SELECT e.firstName, e.lastName, o.city, o.state
FROM employees e
LEFT JOIN offices o ON e.officeCode = o.officeCode
ORDER BY e.firstName, e.lastName
"""
df_employee = pd.read_sql(q_employee, conn)

# STEP 4
# Return customers with no orders and their sales rep info
q_contacts = """
SELECT c.contactFirstName, c.contactLastName, c.phone, c.salesRepEmployeeNumber
FROM customers c
LEFT JOIN orders o ON c.customerNumber = o.customerNumber
WHERE o.orderNumber IS NULL
ORDER BY c.contactLastName
"""
df_contacts = pd.read_sql(q_contacts, conn)

# STEP 5
# Return customer contacts with payment amounts and dates, sorted by amount descending
q_payment = """
SELECT c.contactFirstName, c.contactLastName, p.paymentDate, CAST(p.amount AS REAL) AS amount
FROM customers c
JOIN payments p ON c.customerNumber = p.customerNumber
ORDER BY CAST(p.amount AS REAL) DESC
"""
df_payment = pd.read_sql(q_payment, conn)

# STEP 6
# Return employees whose customers have an average credit limit over 90k
q_credit = """
SELECT e.employeeNumber, e.firstName, e.lastName, COUNT(c.customerNumber) AS numcustomers
FROM employees e
JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
JOIN (
    SELECT c2.salesRepEmployeeNumber
    FROM customers c2
    GROUP BY c2.salesRepEmployeeNumber
    HAVING AVG(c2.creditLimit) > 90000
) sub ON e.employeeNumber = sub.salesRepEmployeeNumber
GROUP BY e.employeeNumber, e.firstName, e.lastName
ORDER BY numcustomers DESC
"""
df_credit = pd.read_sql(q_credit, conn)

# STEP 7
# Return products with the number of orders and total units sold
q_product_sold = """
SELECT p.productName, COUNT(DISTINCT o.orderNumber) AS numorders, SUM(od.quantityOrdered) AS totalunits
FROM products p
JOIN orderdetails od ON p.productCode = od.productCode
JOIN orders o ON od.orderNumber = o.orderNumber
GROUP BY p.productCode, p.productName
ORDER BY totalunits DESC
"""
df_product_sold = pd.read_sql(q_product_sold, conn)

# STEP 8
# Return products with the number of distinct customers who purchased them
q_total_customers = """
SELECT p.productName, p.productCode, COUNT(DISTINCT c.customerNumber) AS numpurchasers
FROM products p
JOIN orderdetails od ON p.productCode = od.productCode
JOIN orders o ON od.orderNumber = o.orderNumber
JOIN customers c ON o.customerNumber = c.customerNumber
GROUP BY p.productCode, p.productName
ORDER BY numpurchasers DESC
"""
df_total_customers = pd.read_sql(q_total_customers, conn)

# STEP 9
# Return the number of customers per office
q_customers = """
SELECT o.officeCode, o.city, COUNT(DISTINCT c.customerNumber) AS n_customers
FROM offices o
LEFT JOIN employees e ON o.officeCode = e.officeCode
LEFT JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
GROUP BY o.officeCode, o.city
ORDER BY o.officeCode
"""
df_customers = pd.read_sql(q_customers, conn)

# STEP 10
# Return employees who sold products ordered by fewer than 20 customers
q_under_20 = """
SELECT DISTINCT e.employeeNumber, e.firstName, e.lastName, o.city, o.officeCode
FROM employees e
JOIN offices o ON e.officeCode = o.officeCode
JOIN customers c ON e.employeeNumber = c.salesRepEmployeeNumber
JOIN orders ord ON c.customerNumber = ord.customerNumber
JOIN orderdetails od ON ord.orderNumber = od.orderNumber
JOIN products p ON od.productCode = p.productCode
WHERE p.productCode IN (
    SELECT od2.productCode
    FROM orderdetails od2
    JOIN orders ord2 ON od2.orderNumber = ord2.orderNumber
    JOIN customers c2 ON ord2.customerNumber = c2.customerNumber
    GROUP BY od2.productCode
    HAVING COUNT(DISTINCT c2.customerNumber) < 20
)
ORDER BY e.lastName, e.firstName
"""
df_under_20 = pd.read_sql(q_under_20, conn)

conn.close()