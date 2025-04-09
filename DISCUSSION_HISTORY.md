# Discussion History

This document records the key points from our conversation regarding the project
setup and changes. Use this file to refresh the context and recall past
decisions and modifications across sessions.

## Summary of Discussions

- **Project Setup and Structure**:

  - Established a three-tier architecture including `model_service`, `web_app`,
    and `db`.
  - Created placeholder files for key components in each tier.

- **Documentation Updates**:

  - The `README.md` was updated with a detailed project overview, architecture
    description, and setup instructions.
  - Configuration instructions were refined (e.g., using Streamlit for the web
    app).

- **Data Loading and Preprocessing**:

  - A PyTorch script (`model_service/src/data_loader.py`) was implemented to
    load and preprocess the MNIST dataset.
  - Proper transformations, normalization, and data loaders for training and
    testing were provided.

- **Model Implementation**:

  - A CNN model class (`MNISTCNN`) was implemented in
    `model_service/src/model.py` designed for MNIST digit classification.

- **Training and Evaluation**:

  - A training script (`model_service/src/train.py`) was developed to train the
    CNN model, including validation, checkpoint saving, metric logging, and early
    stopping.
  - An evaluation script (`model_service/src/evaluate.py`) was implemented to
    assess model performance, reporting accuracy, precision, recall, and confusion
    matrix.

- **Model Export**:

  - An export script (`model_service/src/export.py`) was added to convert the
    trained model into a format suitable for inference in the model service, along
    with necessary preprocessing functions.

- **Session Context**:

  - Notably, the conversational context does not persist between login sessions.
    This document serves to retain key discussion points and decisions.

- **Database and Logging Infrastructure**:

  - Implemented SQL scripts for initializing the predictions database with a
    predictions table containing not-null constraints, proper checks, and indices.
  - Developed the database connection module in `db/src/db.py`, which includes
    connection pooling, query execution, and robust error handling.
  - Created the prediction logging module in `db/src/prediction_logger.py` to
    securely log prediction results using parameterized queries.
  - Added lightweight tests in `db/tests/test_db.py` to validate the database
    infrastructure and logging functionality, including fixes for module import
    issues.

- **Recent Interaction Update**:
  - Added and reviewed the `db/src/db.py` file to consolidate database
    connection logic.
  - Confirmed sys.path adjustments in tests to resolve module import errors.
  - Finalised implementations for the database connection and logging modules in
    this session.

_Last updated: 2025-04-10_
