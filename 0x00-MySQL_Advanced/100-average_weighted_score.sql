-- SQL script that creates a stored procedure ComputeAverageWeightedScoreForUser that computes and store the average weighted score for a student
DELIMITER //

DROP PROCEDURE IF EXISTS ComputeAverageWeightedScoreForUser;

CREATE PROCEDURE ComputeAverageWeightedScoreForUser(IN user_id INT)
BEGIN
    DECLARE t_score FLOAT DEFAULT 0;
    DECLARE t_weight FLOAT DEFAULT 0;

    SELECT SUM(corrections.score * projects.weight), SUM(projects.weight) INTO t_score, t_weight
    FROM corrections
    INNER JOIN projects ON corrections.project_id = projects.id;

    IF t_weight > 0 THEN
        UPDATE users SET average_score = t_score / t_weight WHERE id = user_id;
    ELSE
        UPDATE users SET average_score = 0 WHERE id = user_id;
    END IF;
END; //

DELIMITER ;
