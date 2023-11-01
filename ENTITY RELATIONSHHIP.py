#!/usr/bin/env python
# coding: utf-8

# In[37]:


get_ipython().run_line_magic('load_ext', 'sql')


# In[2]:


get_ipython().run_line_magic('sql', 'mysql://root:Kwambu6000#@localhost:3306/united_nations')


# In[3]:


get_ipython().run_cell_magic('sql', '', 'SELECT\n* \nFROM\n    united_nations.access_to_basic_services\nLIMIT 5;\n')


# ## Create table geographic_locations

# %%sql
# 
# CREATE TABLE united_nations.Geographic_Location (
#   Country_name VARCHAR(37) PRIMARY KEY,
#   Sub_region VARCHAR(25),
#   Region VARCHAR(32),
#   Land_area NUMERIC(10,2)
# );

# ## Extract the relevant columns from the original table

# INSERT INTO united_nations.Geographic_Location (Country_name, Sub_region, Region, Land_area)
# SELECT Country_name,
#     Sub_region,
#     Region,
#     AVG(Land_area) as Country_area
# FROM united_nations.Access_to_Basic_Services
# GROUP BY Country_name,
#     Sub_region,
#     Region;

# In[7]:


get_ipython().run_cell_magic('sql', '', 'CREATE TABLE united_nations.basic_services2 (\n Country_name VARCHAR(37),\n Time_period INT,\n Pct_managed_drinking_water_services NUMERIC(5,2),\n Pct_managed_sanitation_services NUMERIC (5,2),\n PRIMARY KEY(Country_name,Time_period),\n FOREIGN KEY (Country_name) REFERENCES geographic_location (Country_name)\n);\n')


# In[8]:


get_ipython().run_cell_magic('sql', '', '\nINSERT INTO Basic_Services2 (Country_name, Time_period, Pct_managed_drinking_water_services, Pct_managed_sanitation_services)\nSELECT Country_name,\n    Time_period,\n    Pct_managed_drinking_water_services,\n    Pct_managed_sanitation_services\nFROM united_nations.Access_to_Basic_Services;\n')


# In[11]:


get_ipython().run_cell_magic('sql', '', 'SELECT * FROM united_nations.basic_services2;\n')


# ## Chinook DB Join Statments

# In[16]:


get_ipython().run_line_magic('sql', 'sqlite:///C:/Users/wwaswa/Desktop/Serverless/chinook.db')


# In[18]:


get_ipython().run_cell_magic('sql', '', 'SELECT\n*\nFROM\n    employees\nLIMIT5;\n')


# In[23]:


get_ipython().run_cell_magic('sql', '', 'SELECT \n*\nFROM\ntracks\n')


# In[24]:


get_ipython().run_cell_magic('sql', '', 'SELECT \n*\nFROM\nalbums\n')


# In[25]:


get_ipython().run_cell_magic('sql', '', '\nSELECT\n    a.AlbumId,\n    a.Title AS "Album Title",\n    t.Name AS "Track Name"\nFROM\n    albums a\nINNER JOIN\n    tracks AS t\n    ON a.Title = t.Name\nLIMIT 10;\n')


# In[26]:


get_ipython().run_cell_magic('sql', '', '\nSELECT\n    a.AlbumId,\n    a.Title AS "Album Title",\n    t.Name AS "Track Name",\n    ar.Name AS "Artist Name"\nFROM\n    albums AS a\nINNER JOIN\n    tracks AS t\n    ON a.Title = t.Name\nINNER JOIN\n    artists AS ar\n    ON ar.ArtistId = a.ArtistId\n')


# ## Dam levels Data

# In[5]:


get_ipython().run_line_magic('sql', 'sqlite:///C:/Users/wwaswa/Desktop/Serverless/dam_levels.db')


# ## Checking the db tables

# In[6]:


get_ipython().run_cell_magic('sql', '', 'SELECT *\nFROM\ndam_levels\n')


# In[7]:


##It seems that data for two dams have been lumped together in some rows. Write a query to delete these rows.


# In[8]:


get_ipython().run_cell_magic('sql', '', '\nDELETE\nFROM\n    dam_levels\nWHERE\n    Assessment_Officer = "V. Mokere";\n')


# In[9]:


get_ipython().run_cell_magic('sql', '', 'SELECT *\nFROM\ndam_levels\n')


# In[ ]:


##Now, re-insert the deleted rows of data the right way, with a focus on atomicity.


# In[12]:


get_ipython().run_cell_magic('sql', '', 'INSERT INTO dam_levels (year,dam_name,Assessment_Officer,Officer_Reg,water_level,dam_latitude,dam_longitude)\nVALUES\n    ( 2012,"STEENBRAS LOWER","V. Mokere",201124,20.3,-34.180527,18.866688),\n    ( 2012,"STEENBRAS UPPER","V. Mokere",201124,24.2,-34.166702,18.90976),\n    ( 2013,"STEENBRAS LOWER","V. Mokere",201124,22.4,-34.180527,18.866688),\n    ( 2013,"STEENBRAS UPPER","V. Mokere",201124,24.6,-34.166702,18.90976),\n    ( 2015,"STEENBRAS LOWER","V. Mokere",201124,22.7,-34.180527,18.866688),\n    ( 2015,"STEENBRAS UPPER","V. Mokere",201124,24.6,-34.16670,18.90976);\n')


# In[13]:


get_ipython().run_cell_magic('sql', '', 'SELECT *\nFROM\ndam_levels\n')


# In[14]:


##Start by creating the structure of the new table dam_levels_1nf.


# In[15]:


get_ipython().run_cell_magic('sql', '', '\nCREATE TABLE dam_levels_1nf (\n    AssessmentId INTEGER PRIMARY KEY AUTOINCREMENT,\n    year INTEGER,\n    dam_name VARCHAR(100),\n    Assessment_Officer VARCHAR(100),\n    Officer_Reg INTEGER,\n    water_level NUMERIC(10,1),\n    dam_latitude NUMERIC(3,6),\n    dam_longitude NUMERIC(3,6)\n);\n')


# In[16]:


##Insert the data into the new table


# In[17]:


get_ipython().run_cell_magic('sql', '', '\nINSERT INTO\n    dam_levels_1nf(\n            year,\n            dam_name,\n            Assessment_Officer,\n            Officer_Reg,\n            water_level,\n            dam_latitude,\n            dam_longitude\n        )\nSELECT\n    year,\n    dam_name,\n    Assessment_Officer,\n    Officer_Reg,\n    water_level,\n    dam_latitude,\n    dam_longitude\nFROM\n    dam_levels\nORDER BY year;\n')


# In[18]:


##Delete the redundant table, dam_levels


# In[ ]:





# In[20]:


get_ipython().run_cell_magic('sql', '', 'SELECT *\nFROM\n dam_levels_1nf\n')


# ## The Second Normal Form

# In[21]:


## Creatring tables


# In[22]:


get_ipython().run_cell_magic('sql', '', '\nCREATE TABLE assessments (\n    AssessmentId INTEGER PRIMARY KEY AUTOINCREMENT,\n    year INTEGER,\n    Assessment_Officer VARCHAR(100),\n    Officer_Reg INTEGER,\n    water_level NUMERIC(10,1)\n);\n')


# In[23]:


##Copy the relevant data into the assessments table from dam_levels_1nf.


# In[24]:


get_ipython().run_cell_magic('sql', '', '\nINSERT INTO\n    assessments(\n            AssessmentId,\n            year,\n            Assessment_Officer,\n            Officer_Reg,\n            water_level\n        )\nSELECT\n    AssessmentId,\n    year,\n    Assessment_Officer,\n    Officer_Reg,\n    water_level\nFROM\n    dam_levels_1nf\nORDER BY year;\n')


# In[25]:


##Create the dams table.


# In[26]:


get_ipython().run_cell_magic('sql', '', '\nCREATE TABLE dams (\n    dam_name VARCHAR(100),\n    dam_latitude NUMERIC(3,6),\n    dam_longitude NUMERIC(3,6)\n);\n')


# In[27]:


##Copy the relevant data into the dams table from dam_levels_1nf


# In[28]:


get_ipython().run_cell_magic('sql', '', '\nINSERT INTO\n    dams(\n            dam_name,\n            dam_latitude,\n            dam_longitude\n        )\nSELECT\n    dam_name,\n    dam_latitude,\n    dam_longitude\nFROM\n    dam_levels_1nf\nGROUP BY dam_name;\n')


# In[29]:


##Using the AssessmentId from the assessments table and the dam_name from the dams table, create the junction table. Call it dam_assessments.


# In[30]:


get_ipython().run_cell_magic('sql', '', '\nCREATE TABLE\n    dam_assessments (\n        AssessmentId INTEGER PRIMARY KEY AUTOINCREMENT,\n        dam_name VARCHAR(100)\n    );\n')


# In[31]:


##Insert the relevant data into the dam_assessments table.


# In[32]:


get_ipython().run_cell_magic('sql', '', '\nINSERT INTO\n    dam_assessments(\n            AssessmentId,\n            dam_name\n        )\nVALUES\n    (1 \t, "WEMMERSHOEK"),\n    (2 \t, "VOËLVLEI"),\n    (3 \t, "HELY-HUTCHINSON"),\n    (4 \t, "WOODHEAD"),\n    (5 \t, "STEENBRAS LOWER"),\n    (6 \t, "STEENBRAS UPPER"),\n    (7 \t, "WEMMERSHOEK"),\n    (8 \t, "VOËLVLEI"),\n    (9 \t, "HELY-HUTCHINSON"),\n    (10 , "WOODHEAD"),\n    (11 , "STEENBRAS LOWER"),\n    (12 , "STEENBRAS UPPER"),\n    (13 , "WEMMERSHOEK"),\n    (14 , "VOËLVLEI"),\n    (15 , "HELY-HUTCHINSON"),\n    (16 , "WOODHEAD"),\n    (17 , "STEENBRAS LOWER"),\n    (18 , "STEENBRAS UPPER");\n')


# In[33]:


##Delete the now redundant dam_levels_1nf table.


# ## SoftDevEmployees

# In[35]:


##Connecting to the db


# In[38]:


get_ipython().run_line_magic('sql', 'sqlite:///C:/Users/wwaswa/Desktop/Serverless/SoftDevEmployees.db')


# In[39]:


get_ipython().run_cell_magic('sql', '', 'SELECT *\nFROM\n    employees\nWHERE\n    Role LIKE \'%,%\'    -- we use the LIKE keyword to search for the comma "," delimiter\nOR\n    Department LIKE \'%,%\' -- we use the LIKE keyword to search for the comma "," delimiter\n')


# In[40]:


##Let's get to it by first creating the required table based on the above structure.


# In[45]:


get_ipython().run_cell_magic('sql', '', '\n\nCREATE TABLE Employees_1N (\n    Name VARCHAR NOT NULL,\n    Surname VARCHAR NOT NULL,\n    Role VARCHAR NOT NULL,\n    Department VARCHAR NOT NULL,\n    Title VARCHAR,\n    OccupationBand VARCHAR,\n    Salary REAL,\n    PRIMARY KEY(Name, Surname, Role, Department)\n);\n')


# In[46]:


##Firstly, split the contents of the FullName column into Name and Surname, such that each cell only contains one piece of data. Then capitalise the first letter of the Title column.


# In[47]:


get_ipython().run_cell_magic('sql', '', "SELECT\n    FullName,\n    TRIM(SUBSTR(FullName,1,INSTR(FullName,',')-1)) AS Name, --Get substring before comma\n    TRIM(SUBSTR(FullName,INSTR(FullName,',')+1)) AS Surname, --Get substring after comma\n    UPPER(SUBSTR(Title,1,1)) ||LOWER(SUBSTR(Title,2)) AS Title --Standardising all Titles to start with a capital letter\nFROM\n    Employees\nLIMIT 5;\n")


# In[48]:


##The set of all entries that only contain atomic cells.


# In[49]:


get_ipython().run_cell_magic('sql', '', "SELECT\n    TRIM(SUBSTR(FullName,1,INSTR(FullName,',')-1)) AS Name,     --Splitting FullName to obtain Name,\n    TRIM(SUBSTR(FullName,INSTR(FullName,',')+1)) AS Surname,    --Splitting FullName to obtain Surname\n    UPPER(SUBSTR(Title,1,1)) ||LOWER(SUBSTR(Title,2)) AS Title, --Standardising all Titles to start with a capital letter\n    Role,\n    OccupationBand,\n    Salary,\n    Department\nFROM\n    Employees\nWHERE\n    ROLE LIKE '%,%' OR Department LIKE '%,%' --Targets only the non-atomic values\n")


# In[50]:


get_ipython().run_cell_magic('sql', '', "\n/*SET #1 ======================================================================================\n   The set of all entries containing the first `Role` or `Department` for all non-atomic cells.\n==============================================================================================*/\n\nSELECT\n    TRIM(SUBSTR(FullName,1,INSTR(FullName,',')-1)) AS Name,             -- Splitting FullName to obtain Name\n    TRIM(SUBSTR(FullName,INSTR(FullName,',')+1)) AS Surname,            -- Splitting FullName to obtain Surname\n    UPPER(SUBSTR(Title,1,1)) || LOWER(SUBSTR(Title,2)) AS Title,        -- Standardising all Titles to start with a capital letter\n\n    CASE\n        WHEN                                                            -- When the row only has one role, i.e. there's no value after any comma\n            TRIM(SUBSTR(Role,1,INSTR(Role,',')-1))=''\n        THEN\n            Role                                                        -- return the original role\n        ELSE\n            TRIM(SUBSTR(Role,1,INSTR(Role,',')-1))                      -- otherwise return the substring before the comma\n    END AS Role,                                                        -- and include that as the Role\n\n    OccupationBand,\n    Salary,\n\n    CASE                                                                -- When the row only has one department, i.e. there's no value after any comma\n        WHEN\n            TRIM(SUBSTR(Department,1,INSTR(Department,',')-1))=''\n        THEN\n            Department                                                 -- return the original department\n        ELSE\n            TRIM(SUBSTR(Department,1,INSTR(Department,',')-1))         -- otherwise return the substring before the comma\n    END AS Department                                                  --  and include that as the Department\n\nFROM\n    Employees\nWHERE\n    Role LIKE '%,%' OR Department LIKE '%,%'                           -- Filter all entries that have non-atomic values in the Role and Department columns\n\nUNION\n\n/*SET #2 ======================================================================================\n   The set of all entries containing the second `Role` or `Department` for all non-atomic cells.\n==============================================================================================*/\n\nSELECT\n    TRIM(SUBSTR(FullName,1,INSTR(FullName,',')-1)) AS Name,             -- Splitting FullName to obtain Name\n    TRIM(SUBSTR(FullName,INSTR(FullName,',')+1)) AS Surname,            -- Splitting FullName to obtain Surname\n    UPPER(SUBSTR(Title,1,1)) || LOWER(SUBSTR(Title,2)) AS Title,        -- Standardising all Titles to start with a capital letter\n\n    CASE\n        WHEN                                                            -- When the row only has one role, i.e. there's no value after any comma\n            TRIM(SUBSTR(Role,1,INSTR(Role,',')-1))=''\n        THEN\n            Role                                                        -- return the original role\n        ELSE\n            TRIM(SUBSTR(Role,INSTR(Role,',')+1))                     -- otherwise return the substring after the comma\n    END AS Role,                                                        -- and include that as the Role\n\n    OccupationBand,\n    Salary,\n\n    CASE                                                                -- When the row only has one department, i.e. there's no value after any comma\n        WHEN\n            TRIM(SUBSTR(Department,1,INSTR(Department,',')-1))=''\n        THEN\n            Department                                                 -- return the original department\n        ELSE\n            TRIM(SUBSTR(Department,INSTR(Department,',')+1))         -- otherwise return the substring after the comma\n    END AS Department                                                  --  and include that as the Department\n\nFROM\n    Employees\nWHERE\n    Role LIKE '%,%' OR Department LIKE '%,%'\n\nUNION\n\n/*SET #3 ======================================================================================\n   The set of all entries that **only** contain atomic cells.\n==============================================================================================*/\n\nSELECT\n    TRIM(SUBSTR(FullName,1,INSTR(FullName,',')-1)) AS Name,     --Splitting FullName to obtain Name\n    TRIM(SUBSTR(FullName,INSTR(FullName,',')+1)) AS Surname,    --Splitting FullName to obtain Surname\n    UPPER(SUBSTR(Title,1,1)) ||LOWER(SUBSTR(Title,2)) AS Title, --Standardising all Titles to start with a capital letter\n    Role,\n    OccupationBand,\n    Salary,\n    Department\nFROM\n    Employees\nWHERE ROLE NOT LIKE '%,%' AND Department NOT LIKE '%,%' --Targets only the atomic values;\n")


# In[ ]:


##Use the combined query in Exercise 4 to insert the data into the table we created in Exercise 1.


# In[51]:


get_ipython().run_cell_magic('sql', '', "--Below is the INSERT query for the First Normal Form.\n\nDELETE FROM Employees_1NF;\n\nINSERT INTO Employees_1NF (Name,Surname,Title,Role,OccupationBand,Salary,Department)\n\n/*SET #1 ======================================================================================\n   The set of all entries containing the first `Role` or `Department` for all non-atomic cells.\n==============================================================================================*/\n\nSELECT\n    TRIM(SUBSTR(FullName,1,INSTR(FullName,',')-1)) AS Name,             -- Splitting FullName to obtain Name\n    TRIM(SUBSTR(FullName,INSTR(FullName,',')+1)) AS Surname,            -- Splitting FullName to obtain Surname\n    UPPER(SUBSTR(Title,1,1)) || LOWER(SUBSTR(Title,2)) AS Title,        -- Standardising all Titles to start with a capital letter\n\n    CASE\n        WHEN                                                            -- When the row only has one role, i.e. there's no value after any comma\n            TRIM(SUBSTR(Role,1,INSTR(Role,',')-1))=''\n        THEN\n            Role                                                        -- return the original role\n        ELSE\n            TRIM(SUBSTR(Role,1,INSTR(Role,',')-1))                      -- otherwise return the substring before the comma\n    END AS Role,                                                        -- and include that as the Role\n\n    OccupationBand,\n    Salary,\n\n    CASE                                                                -- When the row only has one department, i.e. there's no value after any comma\n        WHEN\n            TRIM(SUBSTR(Department,1,INSTR(Department,',')-1))=''\n        THEN\n            Department                                                 -- return the original department\n        ELSE\n            TRIM(SUBSTR(Department,1,INSTR(Department,',')-1))         -- otherwise return the substring before the comma\n    END AS Department                                                  --  and include that as the Department\n\nFROM\n    Employees\nWHERE\n    Role LIKE '%,%' OR Department LIKE '%,%'                           -- filter all entries that have non-atomic values in the Role and Department columns\n\nUNION\n\n/*SET #2 ======================================================================================\n   The set of all entries containing the second `Role` or `Department` for all non-atomic cells.\n==============================================================================================*/\n\nSELECT\n    TRIM(SUBSTR(FullName,1,INSTR(FullName,',')-1)) AS Name,             -- Splitting FullName to obtain Name\n    TRIM(SUBSTR(FullName,INSTR(FullName,',')+1)) AS Surname,            -- Splitting FullName to obtain Surname\n    UPPER(SUBSTR(Title,1,1)) || LOWER(SUBSTR(Title,2)) AS Title,        -- Standardising all Titles to start with a capital letter\n\n    CASE\n        WHEN                                                            -- When the row only has one role, i.e. there's no value after any comma\n            TRIM(SUBSTR(Role,1,INSTR(Role,',')-1))=''\n        THEN\n            Role                                                        -- return the original role\n        ELSE\n            TRIM(SUBSTR(Role,INSTR(Role,',')+1))                     -- otherwise return the substring after the comma\n    END AS Role,                                                        -- and include that as the Role\n\n    OccupationBand,\n    Salary,\n\n    CASE                                                                -- When the row only has one department, i.e. there's no value after any comma\n        WHEN\n            TRIM(SUBSTR(Department,1,INSTR(Department,',')-1))=''\n        THEN\n            Department                                                 -- return the original department\n        ELSE\n            TRIM(SUBSTR(Department,INSTR(Department,',')+1))         -- otherwise return the substring after the comma\n    END AS Department                                                  --  and include that as the Department\n\nFROM\n    Employees\nWHERE\n    Role LIKE '%,%' OR Department LIKE '%,%'\n\nUNION\n\n/*SET #3 ======================================================================================\n   The set of all entries that **only** contain atomic cells.\n==============================================================================================*/\n\nSELECT\n    TRIM(SUBSTR(FullName,1,INSTR(FullName,',')-1)) AS Name,     --Splitting FullName to obtain Name\n    TRIM(SUBSTR(FullName,INSTR(FullName,',')+1)) AS Surname,    --Splitting FullName to obtain Surname\n    UPPER(SUBSTR(Title,1,1)) ||LOWER(SUBSTR(Title,2)) AS Title, --Standardising all Titles to start with a capital letter\n    Role,\n    OccupationBand,\n    Salary,\n    Department\nFROM\n    Employees\nWHERE ROLE NOT LIKE '%,%' AND Department NOT LIKE '%,%' --Targets only the atomic values;\n")


# ## Creating views

# In[52]:


get_ipython().run_line_magic('sql', 'sqlite:///C:/Users/wwaswa/Desktop/Serverless/chinook.db')


# In[53]:


##Create a LOOKUP view of the surname, first name, title, and country of each employee called Employee_View


# In[54]:


get_ipython().run_cell_magic('sql', '', '\nCREATE VIEW Employee_View AS\nSELECT LastName, FirstName, Title, Country\nFROM Employees;\n')


# In[55]:


get_ipython().run_cell_magic('sql', '', "\nSELECT * FROM Employee_View\nWHERE Title LIKE '%Sales%'\n")


# In[56]:


get_ipython().run_cell_magic('sql', '', '\nCREATE VIEW Customer_Support_View AS\nSELECT c.FirstName Customer_Name, c.LastName Customer_Surname, c.Country Customer_Country, c.SupportRepId, e.EmployeeId, e.LastName Employee_surname, e.FirstName Employee_first_name, e.Title Employee_job_title, e.Country Employee_Country\nFROM customers c\nINNER JOIN employees e\nON c.SupportRepId = e.EmployeeId\n')


# In[57]:


##Query the Customer_Support_View view to get a list of the names and surnames of the clients 
##who were helped by an employee with the Employeeid '3'.


# In[58]:


get_ipython().run_cell_magic('sql', '', '\nSELECT Customer_Name, Customer_Surname\nFROM Customer_Support_View\nWHERE Employeeid = 3;\n')


# In[59]:


##Create an AGGREGATING view that counts the number of customers that are currently 
##being serviced per country, called Customer_per_Country_View.


# In[60]:


get_ipython().run_cell_magic('sql', '', '\nCREATE VIEW Customer_per_Country_View AS\nSELECT COUNT (CustomerId) AS Num_customers, Country\nFROM customers\nGROUP BY Country;\n')


# In[61]:


##Write a query that returns the country with the most customers from Customer_per_Country_View.


# In[62]:


get_ipython().run_cell_magic('sql', '', '\nSELECT Country, MAX(Num_customers)\nFROM Customer_per_Country_View\n')


# In[63]:


##Write a query that returns the number of customers that each support employee services,
##along with the name of the employee. Call this view Support_Person_Stats.


# In[64]:


get_ipython().run_cell_magic('sql', '', '\nCREATE VIEW Support_Person_Stats AS\nSELECT COUNT(c.SupportRepId) Count_of_Customers_Serviced , e.EmployeeId, e.LastName\nFROM customers c\nINNER JOIN employees e\nON c.SupportRepId = e.EmployeeId\nGROUP BY e.EmployeeId;\n')


# ## Northwind db Views

# In[65]:


get_ipython().run_line_magic('sql', 'sqlite:///C:/Users/wwaswa/Desktop/Serverless/Northwind.db')


# In[66]:


##Write a SQL statement to create a view named CustomerOrderView that shows the CustomerID, OrderID, and OrderDate from the Orders table, and CompanyName
##from the Customers table.


# In[67]:


get_ipython().run_cell_magic('sql', '', '\nCREATE VIEW CustomerOrderView AS\nSELECT o.CustomerID, o.OrderID, o.OrderDate, c.CompanyName\nFROM Orders o\nINNER JOIN Customers c ON o.CustomerID = c.CustomerID;\n')


# In[68]:


##Write a SQL query to retrieve all the data from the CustomerOrderView view.


# In[69]:


get_ipython().run_cell_magic('sql', '', 'SELECT *\nFROM\nCustomerOrderView\n')


# In[70]:


##Write a SQL statement to update the CustomerOrderView view to separate the OrderDate column into two different date 
##and time columns named OrderDateOnly and OrderTimeOnly respectively.


# In[71]:


get_ipython().run_cell_magic('sql', '', '\nDROP VIEW IF EXISTS CustomerOrderView;\n\nCREATE VIEW CustomerOrderView AS\nSELECT o.CustomerID, o.OrderID, DATE(o.OrderDate) AS OrderDateOnly, TIME(o.OrderDate) AS OrderTimeOnly, c.CompanyName\nFROM Orders o\nINNER JOIN Customers c ON o.CustomerID = c.CustomerID;\n')


# In[72]:


##Write a SQL query to retrieve all the data from the updated CustomerOrderView view.


# In[73]:


get_ipython().run_cell_magic('sql', '', '\nSELECT *\nFROM CustomerOrderView;\n')


# ## Sub querries and CTEs

# In[74]:


##Retrieve product details from products that have been ordered by customers from the UK


# In[75]:


get_ipython().run_cell_magic('sql', '', '\nWITH most_orders AS (\n    SELECT orders.CustomerID\n    FROM orders\n    GROUP BY orders.CustomerID\n    ORDER BY COUNT(*) DESC\n    LIMIT 1\n)\nSELECT customers.*\nFROM customers\nJOIN most_orders\nON customers.CustomerID = most_orders.CustomerID;\n')


# In[76]:


##Find out the names of customers who have ordered products of more than the average order value.


# In[77]:


get_ipython().run_cell_magic('sql', '', '\nWITH avg_order_value AS (\n    SELECT AVG(OrderDetails.UnitPrice * OrderDetails.Quantity) AS average_value\n    FROM OrderDetails\n)\nSELECT DISTINCT customers.CompanyName\nFROM customers\nJOIN orders ON customers.CustomerID = orders.CustomerID\nJOIN OrderDetails ON orders.OrderID = OrderDetails.OrderID\nWHERE (OrderDetails.UnitPrice * OrderDetails.Quantity) > (SELECT average_value FROM avg_order_value);\n')


# In[78]:


##Write a CTE to find the most ordered product by each customer.


# In[79]:


get_ipython().run_cell_magic('sql', '', '\nWITH most_ordered_products AS (\n    SELECT customers.CustomerID, OrderDetails.ProductID, COUNT(*) AS order_count\n    FROM customers\n    JOIN orders ON customers.CustomerID = orders.CustomerID\n    JOIN OrderDetails ON orders.OrderID = OrderDetails.OrderID\n    GROUP BY customers.CustomerID, OrderDetails.ProductID\n)\nSELECT customers.CompanyName, products.ProductName, max_order_count\nFROM (\n    SELECT CustomerID, MAX(order_count) AS max_order_count\n    FROM most_ordered_products\n    GROUP BY CustomerID\n) AS max_order_count\nJOIN most_ordered_products ON max_order_count.CustomerID = most_ordered_products.CustomerID AND max_order_count.max_order_count = most_ordered_products.order_count\nJOIN customers ON most_ordered_products.CustomerID = customers.CustomerID\nJOIN products ON most_ordered_products.ProductID = products.ProductID;\n')


# In[80]:


##Using a CTE, list employees who have more than the average number of reports.



# In[81]:


get_ipython().run_cell_magic('sql', '', '\nWITH avg_reports AS (\n    SELECT AVG(report_count) AS average_count\n    FROM (\n        SELECT COUNT(*) AS report_count\n        FROM employees\n        JOIN employees AS reports ON employees.EmployeeID = reports.ReportsTo\n        GROUP BY employees.EmployeeID\n    ) AS report_counts\n)\nSELECT employees.*\nFROM employees\nJOIN employees AS reports ON employees.EmployeeID = reports.ReportsTo\nGROUP BY employees.EmployeeID\nHAVING COUNT(*) > (SELECT average_count FROM avg_reports);\n')


# In[ ]:




