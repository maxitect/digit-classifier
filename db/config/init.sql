-- Placeholder SQL for initializing the database.
CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    predicted_digit INTEGER,
    confidence_score FLOAT,
    true_label INTEGER
);
