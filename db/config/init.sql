-- SQL script for initializing the predictions database.
CREATE TABLE predictions (
    id SERIAL PRIMARY KEY,
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    predicted_digit SMALLINT NOT NULL CHECK (predicted_digit BETWEEN 0 AND 9),
    confidence_score FLOAT NOT NULL CHECK (confidence_score >= 0.0 AND confidence_score <= 1.0),
    true_label SMALLINT NOT NULL CHECK (true_label BETWEEN 0 AND 9)
);

CREATE INDEX idx_predictions_timestamp ON predictions(timestamp);
CREATE INDEX idx_predictions_predicted_digit ON predictions(predicted_digit);
