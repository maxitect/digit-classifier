import logging
from src.utils.db import execute_query

logger = logging.getLogger(__name__)


def log_prediction(
    predicted_digit: int,
    confidence_score: float,
    true_label: int
):
    """
    Logs a prediction result to the predictions table in the database.
    """
    query = """
    INSERT INTO predictions (predicted_digit, confidence_score, true_label)
    VALUES (%s, %s, %s)
    """
    params = (predicted_digit, confidence_score, true_label)
    try:
        execute_query(query, params)
        logger.info("Logged prediction: %s, %s, %s",
                    predicted_digit, confidence_score, true_label)
    except Exception as e:
        logger.error("Failed to log prediction: %s", e)
        raise
