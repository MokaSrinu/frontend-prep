SELECT * 
FROM Parks_and_Recreation.employee_demographics;


SELECT * 
FROM Parks_and_Recreation.employee_demographics
WHERE first_name = 'April';

SELECT * 
FROM employee_salary
WHERE salary > 50000;

SELECT * 
FROM Parks_and_Recreation.employee_demographics
WHERE gender != 'Female';

SELECT * 
FROM Parks_and_Recreation.employee_demographics
WHERE birth_date > '1985-01-01';


-- AND OR NOT -- Logical Operators

SELECT * 
FROM Parks_and_Recreation.employee_demographics
WHERE birth_date > '1985-01-01'
AND gender = 'Male';

SELECT * 
FROM Parks_and_Recreation.employee_demographics
WHERE birth_date > '1985-01-01'
OR gender = 'Male';

SELECT * 
FROM Parks_and_Recreation.employee_demographics
WHERE birth_date > '1985-01-01'
OR NOT gender = 'Male';

-- LIKE Statement --
-- % and _

SELECT *
FROM employee_demographics
WHERE first_name LIKE 'Tom';

SELECT *
FROM employee_demographics
WHERE first_name LIKE '%om';

SELECT *
FROM employee_demographics
WHERE first_name LIKE '%o%';

SELECT *
FROM employee_demographics
WHERE first_name LIKE 'A__';

SELECT *
FROM employee_demographics
WHERE first_name LIKE 'A__%';




