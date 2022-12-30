-- Out of those counties with temperature of more than 60, 
-- retrieve the pair that had the largest absolute difference in temperature
-- and their corresponding temperatures.
-- The second county in the pair has a temperature larger than the first county's temperature. 
-- If multiple pairs exist, retrieve the pair with the smallest FIP of the first county in the pair.


-- 1.05 marks: < 10 operators
-- 1.0 marks: < 12 operators
-- 0.8 marks: correct answer
-- count current 17... idk what i can do but will look again later

SELECT l.name AS name, l.temp AS temp, h.name AS name, h.temp AS temp
FROM County l
JOIN County h
WHERE l.temp>60
ORDER BY l.temp, l.fips, h.temp DESC
LIMIT 1;