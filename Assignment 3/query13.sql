-- Retrieve names of top 10 counties and 
-- their growth ratio in terms of population compared between the latest census year and the oldest census year, 
-- in an descending order by their growth ratio.

-- 1.05 marks: < 15 operators
-- 1.0 marks: < 17 operators
-- 0.9 marks: < 19 operators
-- 0.8 marks: correct answer

SELECT c.name AS name, (MAX(cp.population) / MIN(cp.population)) AS popGrowthRatio
FROM County c JOIN Countypopulation cp ON c.fips=cp.county
WHERE cp.year = 2010 OR cp.year = 2019
AND (SELECT population FROM Countypopulation cp2 WHERE cp2.year=2010 AND cp2.county=cp.county) 
< (SELECT population FROM Countypopulation cp2 WHERE cp2.year=2019 AND cp2.county=cp.county)
GROUP BY fips
ORDER BY popGrowthRatio DESC
LIMIT 10;