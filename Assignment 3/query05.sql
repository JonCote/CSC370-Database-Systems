-- Retrieve the list of abbreviations of states that have
-- a total precipitation of more than 1000 for each state,
-- ordered by the total precipitation in descending order.

-- 1.05 marks: < 7 operators
-- 1.0 marks: < 8 operators
-- 0.8 marks: correct answer

SELECT abbr, SUM(precip) AS 'total' FROM State
JOIN County ON id = state
GROUP BY id
HAVING SUM(precip) > 1000
ORDER BY SUM(precip) DESC;