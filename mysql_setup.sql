CREATE DATABASE IF NOT EXISTS health_prediction_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE health_prediction_db;

CREATE TABLE IF NOT EXISTS patients (
    id            INT           NOT NULL AUTO_INCREMENT PRIMARY KEY,
    full_name     VARCHAR(255)  NOT NULL,
    date_of_birth DATE          NOT NULL,
    email         VARCHAR(255)  NOT NULL,
    glucose       FLOAT         NOT NULL,
    haemoglobin   FLOAT         NOT NULL,
    cholesterol   FLOAT         NOT NULL,
    remarks       TEXT,
    created_at    DATETIME      NOT NULL DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO patients (full_name, date_of_birth, email, glucose, haemoglobin, cholesterol, remarks) VALUES
('Nidhi Sharma',  '1990-01-01', 'nidhisharma@gmail.com',  95,  13.5, 185, 'All values are within healthy ranges. No immediate health risks indicated. Maintain a balanced diet and regular exercise.'),
('Shubham Gawas', '1990-01-01', 'shubhamgawas@gmail.com', 130, 11.2, 245, 'Possible health risks: Diabetes, anaemia, heart disease. Elevated glucose, low haemoglobin, and high cholesterol require medical attention.'),
('Sejal Gawas',   '2002-09-29', 'sejagawas@gmail.com',    88,  14.1, 172, 'Possible health risk: None indicated. All values within normal range. Continue healthy lifestyle habits.'),
('Sonali Gawas',  '1990-01-01', 'sonaligawas@gmail.com',  90,  13.5, 180, 'Possible health risk: None indicated. All blood test values are within healthy ranges. Keep up the good work.');

SELECT * FROM patients;
