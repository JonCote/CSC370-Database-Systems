-- Retrieve the top 5 industries 
-- in a decreasing order by number of employees, 
-- together with the corresponding number of employments 
-- and the average payroll. 

-- 1.05 marks: < 12 operators
-- 1.0 marks: < 14 operators
-- 0.8 marks: correct answer

SELECT i.name AS name, SUM(ci.employees) AS totalEmployees, AVG(ci.payroll) AS avgPayroll
FROM Countyindustries ci JOIN Industry i ON ci.industry = i.id
GROUP BY i.name
ORDER BY totalEmployees DESC, avgPayroll DESC
LIMIT 5;