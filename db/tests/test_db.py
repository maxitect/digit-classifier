import os
import time
import pytest
from db.src.db import init_pool, execute_query
from db.src.prediction_logger import log_prediction

def test_log_prediction():
    # Initialize the connection pool
    init_pool()
    
    # Define test prediction data
    test_predicted_digit = 7
    test_confidence_score = 0.88
    test_true_label = 7

    # Log the prediction
    log_prediction(test_predicted_digit, test_confidence_score, test_true_label)
    
    # Give a short delay to ensure the database has processed the insert (if needed)
    time.sleep(0.5)
    
    # Query the latest record from the predictions table
    query = "SELECT predicted_digit, confidence_score, true_label FROM predictions ORDER BY id DESC LIMIT 1"
    results = execute_query(query)
    
    assert results, "No record found in predictions table."
    record = results[0]
    assert record[0] == test_predicted_digit, f"Expected predicted_digit {test_predicted_digit}, got {record[0]}"
    # Allow for float precision issues in confidence_score comparison
    assert abs(record[1] - test_confidence_score) < 1e-6, f"Expected confidence_score {test_confidence_score}, got {record[1]}"
    assert record[2] == test_true_label, f"Expected true_label {test_true_label}, got {record[2]}"
