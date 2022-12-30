-- Retrieve the list of states (showing both the id and abbreviation) 
-- and their corresponding total area, 
-- not accounting for the counties that have more than 10000 population in the year of 2010, 
-- sorted by area in descending order.

-- 1.05 marks: < 11 operators
-- 1.0 marks: < 13 operators
-- 0.8 marks: correct answer

SELECT id, abbr, SUM(sq_km) AS "area" FROM State
JOIN County ON id = state
JOIN Countypopulation ON fips = county
WHERE population <= 10000 AND year = 2010
GROUP BY id
ORDER BY SUM(sq_km) DESC;
