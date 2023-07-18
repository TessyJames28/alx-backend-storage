-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUsers that computes and store the average weighted score for all students.

DELIMITER //

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    UPDATE users
    JOIN (
        SELECT corrections.user_id, SUM(corrections.score * projects.weight) / SUM(projects.weight) AS average_weighted_score
        FROM corrections
        JOIN projects ON corrections.project_id = projects.id
        GROUP BY corrections.user_id
    ) AS uw ON users.id = uw.user_id
    SET users.average_score = uw.average_weighted_score;
END; //

DELIMITER ;
