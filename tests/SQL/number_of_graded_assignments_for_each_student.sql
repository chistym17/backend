
SELECT student_id, COUNT(*) AS graded_counts
FROM assignments
WHERE state = 'GRADED'
GROUP BY student_id;
