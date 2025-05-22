# from alembic import op
#import sqlalchemy as sa

def upgrade():
    """
    Create trigger not to allow for a question to have
    more than 4 answers (including 1 right and 3 wrong answers)
    """

    op.execute("""
    DELIMITER //
    
    CREATE TRIGGER check_valid_answers
    BEFORE INSERT ON answers
    FOR EACH ROW
    BEGIN
        DECLARE bad_answers_count INT;
        DECLARE good_answer INT;
        DECLARE set_answers_count INT;
       
      
        SELECT 
            COUNT(CASE WHEN ans_validation = TRUE THEN 1 ELSE NULL END) AS good_answer,
            COUNT(CASE WHEN ans_validation = FALSE THEN 1 ELSE NULL END) AS bad_answers_count,
            COUNT(*) OVER(PARTITION BY question_id) AS set_answers_count
        INTO good_answer, bad_answers_count,  set_answers_count
        FROM (SELECT * FROM answers WHERE question_id = NEW.question_id) answer_set;
    
       
        IF set_answers_count > 3 THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'The question cannot have more then 4 answers';
        END IF;
       
       
        IF   good_answer > 0 AND NEW.ans_validation = TRUE THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'The question cannot have more then 1 right answer';      
        END IF;
       
       
        IF   good_answer > 2 AND NEW.ans_validation = FALSE THEN
            SIGNAL SQLSTATE '45000'
            SET MESSAGE_TEXT = 'The question cannot have more then 3 wrong answers';
        END IF;
    
    END ;
    
    //
    
    DELIMITER ;
    """)



def downgrade():
    op.execute("DROP TRIGGER IF EXISTS check_valid_answers")
