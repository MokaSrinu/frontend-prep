-- Joins (Inner Join, Outer Join, Self Join) --

SELECT *
FROM employee_demographics;

SELECT * 
FROM employee_salary;

-- 1. Inner Join (JOIN -- by default considers as Inner Join ) --

SELECT * 
FROM employee_demographics
INNER JOIN employee_salary
	ON employee_demographics.employee_id = employee_salary.employee_id;
    
-- Alias names for easy access -- 
    
SELECT * 
FROM employee_demographics AS dem
INNER JOIN employee_salary AS sal
	ON dem.employee_id = sal.employee_id;
    
-- In Inner join we have to mention the table name for columns if both tables have the same column names    
    
SELECT dem.employee_id, age, occupation
FROM employee_demographics AS dem
INNER JOIN employee_salary AS sal
	ON dem.employee_id = sal.employee_id;
    

-- 2. Outer Join (Left Join, Right Join) --

-- Left Join (Takes everything from left table and takes the matching rows from the right table) --

SELECT *
FROM employee_demographics AS dem
Left JOIN employee_salary AS sal
	ON dem.employee_id = sal.employee_id;
    
-- Right Join (Takes everything from right table and takes the matching rows from the left table) -- 
    
SELECT *
FROM employee_demographics AS dem
Right JOIN employee_salary AS sal
	ON dem.employee_id = sal.employee_id;




-- 3. Self Join (where you tie the table to itself) --

SELECT *
FROM employee_demographics dem
JOIN employee_salary sal
	ON dem.employee_id + 1 = sal.employee_id;
  

SELECT dem.employee_id AS emp_id,
dem.first_name AS emp_first_name,
sal.employee_id AS santa_id,
sal.first_name AS santa_first_name
FROM employee_demographics dem
JOIN employee_salary sal
	ON dem.employee_id + 1 = sal.employee_id;



-- Joining multiple Tables

SELECT * 
FROM employee_demographics dem
INNER JOIN employee_salary sal
	ON dem.employee_id = sal.employee_id
    INNER JOIN parks_departments dp
    ON sal.dept_id = dp.department_id;

SELECT *
FROM employee_salary;





    
    
    