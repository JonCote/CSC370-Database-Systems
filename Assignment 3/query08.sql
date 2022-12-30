-- Retrieve the list of counties sorted by the ratio 
-- between male and female population for each county 
-- in descending order or the aforementioned ratio, and then in the ascending order of county FIP.
-- Exclude tuples with ratio of 1:1 from returned result.

-- 1.05 marks: < 7 operators
-- 1.0 marks: < 8 operators
-- 0.8 marks: correct answer

SELECT county, (
    SUM(
        case 
            when gender='male' then population 
            else 0 
        end)
    /
    SUM(
        case 
            when gender='female' then population 
            else 0 
        end)
    ) AS ratio
FROM genderbreakdown
GROUP BY county
HAVING ratio != 1
ORDER BY ratio DESC, county ASC;