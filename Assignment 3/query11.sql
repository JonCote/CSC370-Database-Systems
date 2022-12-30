-- Retrieve the county name, industry name, and the average payroll for the corresponding county and industry,
-- for counties with more than 2 percent of unemployment rate in any year. 
-- Order the results by county name, then industry name, then average payroll.

-- 1.05 marks: < 19 operators
-- 1.0 marks: < 22 operators
-- 0.9 marks: < 25 operators
-- 0.8 marks: correct answer
-- 0.8 marks: correct answer

-- cant get the payroll to order proper need to fix (might be more issues also)
SELECT c.name AS name, i.name AS indname, ci.payroll as payroll
FROM County c INNER JOIN Countyindustries ci ON c.fips=ci.county AND EXISTS(SELECT unemployed, labour_force FROM Countylabourstats WHERE (labour_force / unemployed) > 0.02)
INNER JOIN Industry i ON ci.industry=i.id
ORDER BY c.name ASC, indname ASC, payroll ASC
