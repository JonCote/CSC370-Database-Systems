-- Retrieve the distinct abbreviations of states which have a county that does NOT have the 
-- "Management of companies and enterprises" industry 
-- and also the corresponding total number of counties in each state
-- in descending order of the number of distinct counties in each state, then in alphebatical order of the abbreviations.
-- Your query need to use the name "Management of companies and enterprises" to filter the tuples, instead of just the industry id as prior knowledge.

-- 1.05 marks: < 13 operators
-- 1.0 marks: < 15 operators
-- 0.8 marks: correct answer

SELECT abbr, COUNT(state) AS numCounties
FROM County c JOIN State s ON c.state = s.id
WHERE c.fips NOT IN (SELECT county FROM Countyindustries WHERE industry IN (SELECT id FROM Industry WHERE name = "Management of companies and enterprises"))
GROUP BY state
ORDER BY numCounties DESC, abbr;