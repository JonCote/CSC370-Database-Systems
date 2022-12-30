-- Retrieve the abbreviations of states that have over 150 counties 
-- which have an employment rate of at least 90% for each county in 2008, 
-- ordered by the number of counties in each state in descending order.

-- 1.05 marks: <8 operators
-- 1.0 marks: <10 operators
-- 0.8 marks: correct answer

SELECT abbr FROM State
JOIN County ON state=id 
JOIN Countylabourstats ON fips = county
AND year=2008 AND EXISTS (SELECT * FROM Countylabourstats WHERE employed / labour_force >= 0.90)
GROUP BY state 
HAVING COUNT(state) >= 150
ORDER BY COUNT(state) DESC;