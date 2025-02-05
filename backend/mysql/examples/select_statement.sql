SELECT * 
FROM Parks_and_Recreation.employee_demographics;

SELECT first_name, last_name, birth_date, age, (age+10)*10 inc_age 
FROM Parks_and_Recreation.employee_demographics;

# PEMDAS

SELECT DISTINCT gender
FROM Parks_and_Recreation.employee_demographics;