# Digit Classifier

A simple digit recogniser trained on the MNIST dataset. This project implements a three-tier architecture consisting of a Model Service, a Web App, and a Database, as outlined in the [ADR](ADR.md).

## Project Overview

This project demonstrates an end-to-end machine learning application for classifying handwritten digits using a convolutional neural network (CNN) trained on the MNIST dataset.

## Architecture

The application follows a **Three-Tier Containerised Architecture**:

- **Model Service**: Handles model inference using a trained CNN via FastAPI.
- **Web App**: Provides a user interface (using Streamlit) for digit drawing and prediction display.
- **Database**: A PostgreSQL database for logging prediction results.

Communication between services is handled over HTTP for the model service and via direct database connectivity for logging.

## Setup Instructions

1. **Clone the Repository**
   Using HTTPS:
   ```bash
   git clone https://github.com/maxitect/digit-classifier.git
   ```
   Using SSH:
   ```bash
   git clone git@github.com:maxitect/digit-classifier.git
   ```
2. **Environment Setup**

   - Install dependencies using Conda:
     ```bash
     conda env create -f environment.yml -n mnist
     conda activate mnist
     ```

3. **Train the Model**

   - **Train**: `python model_services/src/train.py`
   - **Evaluate**: `python model_services/src/evaluate.py`
   - **Export**: `python model_services/src/export.py`

4. **Starting the Services**

   - **Database**: Start the PostgreSQL container.
   - **Model Service**: In your conda environment, run `python model_service/src/main.py`.
   - **Web App**: Run `streamlit run web_app/src/app.py`.

5. **Running Tests**
   - Run tests for each component:
     ```bash
     python -m unittest discover -s model_service/tests
     python -m unittest discover -s web_app/tests
     python -m unittest discover -s db/tests
     ```

## Contributing

Please refer to [STANDARDS.md](STANDARDS.md) for coding practices, [SPEC.md](SPEC.md) for the detailed specification and [ADR.md](ADR.md) for architectural decision details.

## License

MIT License.
