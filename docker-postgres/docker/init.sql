-- Create the database if it doesn't exist
CREATE DATABASE retail_store_sales;

-- Connect to the database
\c retail_store_sales;

-- Create your tables here
CREATE TABLE retail_store_sales (
	"Transaction_ID" TEXT, 
	"Customer_ID" TEXT, 
	"Category" TEXT, 
	"Item" TEXT, 
	"Price_Per_Unit" FLOAT(53), 
	"Quantity" FLOAT(53), 
	"Total_Spent" FLOAT(53), 
	"Payment_Method" TEXT, 
	"Location" TEXT, 
	"Transaction_Date" TIMESTAMP WITHOUT TIME ZONE, 
	"Discount_Applied" BOOLEAN
)