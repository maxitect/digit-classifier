# Implementation Plan

## For MNIST Digit Classifier

Version 1.0  
Prepared by maxitect  
Machine Learning Institute (MLX)  
April 2, 2025

## Revision History

| Name     | Date          | Reason For Changes | Version |
| -------- | ------------- | ------------------ | ------- |
| maxitect | April 2, 2025 | Initial draft      | 1.0     |

## Implementation Tracking

### Tracking Mechanism

- Unique identifier for each task (e.g., 1.1.1)
- Status tracking (Not Started, In Progress, Completed)
- Dependencies clearly marked for each step
- Estimated time: 1 hour maximum per task

### Completion Criteria

- [ ] CNN model trained with ≥85% accuracy
- [ ] Model service API fully functional
- [ ] Web interface complete with drawing capabilities
- [ ] Database logging system implemented
- [ ] All components containerised
- [ ] Application deployed to Hetzner server
- [ ] Documentation completed

### Continuous Improvement

- End-of-phase review for each major component
- Validation of progress against requirements
- Technical debt tracking and documentation

## Implementation Plan

### 1. Project Initialisation

**Objective:** Establish the foundational development environment and project structure

#### 1.1 Repository and Environment Setup

- [ ] Task 1.1.1 - **Prompt:**

```
Create a new Git repository for the MNIST Digit Classifier project. Set up a comprehensive .gitignore file for Python, Docker, and environment files. Include patterns for __pycache__, .env, .venv, *.pyc, .DS_Store, and any IDE-specific files.
```

- [ ] Task 1.1.2 - **Prompt:**

```
Create a conda environment.yml file that specifies all required dependencies with exact versions as outlined in the specification document: Python 3.13.2, PyTorch 2.6, Streamlit 1.44.0, psycopg 3.2.6, and any other necessary libraries. Include instructions for creating the environment.
```

#### 1.2 Project Structure Creation

- [ ] Task 1.2.1 - **Prompt:**

```
Create the basic project directory structure that follows the three-tier architecture decided in the ADR. Include directories for model_service, web_app, and db, with appropriate subdirectories for source code, tests, and configuration. Create empty placeholder files for key components.
```

- [ ] Task 1.2.2 - **Prompt:**

```
Set up a basic README.md file with project overview, architecture description, and setup instructions. This should be a living document that will be updated throughout development.
```

### 2. CNN Model Development

**Objective:** Create, train and validate a CNN model with at least 85% accuracy on MNIST

#### 2.1 Data Handling

- [ ] Task 2.1.1 - **Prompt:**

```
Create a Python script for loading and preprocessing the MNIST dataset using PyTorch. Include functions for downloading the dataset, normalising the images, and creating data loaders for training and testing. Make sure to include proper data transformations.
```

#### 2.2 Model Architecture

- [ ] Task 2.2.1 - **Prompt:**

```
Implement a PyTorch CNN model class for MNIST digit classification. The model should include at least two convolutional layers with appropriate activations, pooling, and fully connected layers. Make sure the output layer has 10 units for the 10 digit classes.
```

#### 2.3 Training Pipeline

- [ ] Task 2.3.1 - **Prompt:**

```
Create a training script that initialises the CNN model, defines loss function and optimiser, and implements a training loop. Include validation after each epoch to monitor accuracy on a validation set. Add early stopping to prevent overfitting.
```

- [ ] Task 2.3.2 - **Prompt:**

```
Enhance the training script to save model checkpoints during training. Include functionality to log training metrics (loss, accuracy) for each epoch. Add a configuration file or command-line arguments to adjust hyperparameters easily.
```

#### 2.4 Model Evaluation

- [ ] Task 2.4.1 - **Prompt:**

```
Create an evaluation script that loads a trained model checkpoint and evaluates it on the MNIST test dataset. Calculate and report metrics including accuracy, precision, recall, and confusion matrix. Verify that the model achieves at least 85% accuracy.
```

- [ ] Task 2.4.2 - **Prompt:**

```
Implement a model export function that converts the trained PyTorch model to a format suitable for inference in the model service. Include any necessary preprocessing functions that will be required during inference. Save the model in a specified location.
```

### 3. Model Service Development

**Objective:** Create a FastAPI service that provides digit classification predictions

#### 3.1 Service Setup

- [ ] Task 3.1.1 - **Prompt:**

```
Set up a basic FastAPI application for the model service. Create the project structure with appropriate modules for models, routers, and utilities. Include configuration for CORS, logging, and error handling.
```

- [ ] Task 3.1.2 - **Prompt:**

```
Implement model loading functionality that initialises the trained CNN model when the FastAPI service starts. The model should be loaded once at startup and reused for all predictions. Include error handling for missing model files.
```

#### 3.2 Image Processing

- [ ] Task 3.2.1 - **Prompt:**

```
Create a module for image preprocessing that takes raw image data (from canvas drawings) and converts it to the format expected by the model. Include functions for resizing, inverting colors if needed, normalising, and tensor conversion. The preprocessing should match what was used during training.
```

#### 3.3 Prediction API

- [ ] Task 3.3.1 - **Prompt:**

```
Implement a "/predict" endpoint that accepts POST requests with image data. The endpoint should decode the image data, preprocess it using the previously created functions, run inference with the loaded model, and return the predicted digit along with confidence scores for all digits.
```

- [ ] Task 3.3.2 - **Prompt:**

```
Add request validation, error handling, and logging to the prediction endpoint. Implement proper HTTP status codes and error messages for different failure scenarios. Include input validation for the image data format.
```

#### 3.4 Service Testing

- [ ] Task 3.4.1 - **Prompt:**

```
Create a simple test script that sends sample MNIST images to the prediction endpoint and verifies the responses. Include both valid and invalid requests to test error handling. Add documentation on how to run the tests.
```

### 4. Database Setup

**Objective:** Configure PostgreSQL database for logging prediction results

#### 4.1 Schema Design

- [ ] Task 4.1.1 - **Prompt:**

```
Create SQL scripts for initialising the PostgreSQL database with appropriate tables for logging predictions. The main table should include columns for id (serial), timestamp, predicted_digit, confidence_score, and true_label. Include appropriate indices and constraints.
```

#### 4.2 Connection Handling

- [ ] Task 4.2.1 - **Prompt:**

```
Implement a database connection module using psycopg 3.2.6 that manages connections to PostgreSQL. Include connection pooling for efficiency and error handling for connection failures. The module should have functions for connecting, executing queries, and closing connections.
```

#### 4.3 Logging Functionality

- [ ] Task 4.3.1 - **Prompt:**

```
Create a logging module that provides functions for storing prediction results in the database. Implement a function that takes prediction data (predicted digit, confidence score, true label) and inserts it into the predictions table. Use parameterised queries to prevent SQL injection.
```

### 5. Web Application Development

**Objective:** Create a Streamlit interface with drawing capabilities and prediction display

#### 5.1 Basic Setup

- [ ] Task 5.1.1 - **Prompt:**

```
Set up a basic Streamlit application with a title, description, and layout for the digit classifier. Include sections for the drawing canvas, prediction results, and true label input. Add necessary imports and configuration.
```

#### 5.2 Drawing Canvas

- [ ] Task 5.2.1 - **Prompt:**

```
Implement a drawing canvas component for the Streamlit application. Use HTML components and JavaScript to create a canvas where users can draw digits. Include functionality for pen drawing and a clear button. The canvas should be responsive and produce an image that can be sent to the model service.
```

#### 5.3 Model Service Integration

- [ ] Task 5.3.1 - **Prompt:**

```
Create a client module for communicating with the model service. Implement a function that takes canvas image data, sends it to the model service's prediction endpoint, and receives the prediction results. Include error handling for API failures.
```

#### 5.4 Prediction Display

- [ ] Task 5.4.1 - **Prompt:**

```
Implement a prediction display component that shows the predicted digit and confidence scores. Use Streamlit components to create a visually appealing display with the predicted digit prominently shown and a bar chart or similar visualisation for confidence scores of all digits.
```

#### 5.5 User Feedback

- [ ] Task 5.5.1 - **Prompt:**

```
Add a form for users to provide the true label for their drawn digit. Implement input validation to ensure only valid digits (0-9) are accepted. Include a submit button that captures the true label and stores it with the prediction.
```

#### 5.6 Database Integration

- [ ] Task 5.6.1 - **Prompt:**

```
Integrate the database logging module with the Streamlit application. When a prediction is made and the user provides a true label, log this information to the database. Include error handling for database connection failures.
```

### 6. Containerisation

**Objective:** Package all components in Docker containers with proper configuration

#### 6.1 Model Service Container

- [ ] Task 6.1.1 - **Prompt:**

```
Create a Dockerfile for the model service that starts from an appropriate Python 3.13.2 base image, installs all required dependencies, copies the model and service code, and configures the service to run on startup. Include proper health checks and configuration for production use.
```

#### 6.2 Web Application Container

- [ ] Task 6.2.1 - **Prompt:**

```
Create a Dockerfile for the Streamlit web application that installs all required dependencies, copies the application code, and configures Streamlit to run on startup. Include proper port mapping and any necessary environment variables.
```

#### 6.3 Database Container

- [ ] Task 6.3.1 - **Prompt:**

```
Configure a PostgreSQL 17.4 container with appropriate initialisation scripts to create the required tables on startup. Set up volume mapping for data persistence and configure database credentials using environment variables.
```

#### 6.4 Docker Compose

- [ ] Task 6.4.1 - **Prompt:**

```
Create a docker-compose.yml file that defines services for the model service, web application, and database. Configure networking so the web application can access both the model service and database. Set up appropriate environment variables, port mappings, and volume mounts.
```

- [ ] Task 6.4.2 - **Prompt:**

```
Enhance the docker-compose.yml file with proper service dependencies, restart policies, and health checks. Include configuration for environment-specific settings and documentation on how to start, stop, and manage the containerised application.
```

### 7. Deployment

**Objective:** Deploy the application to a Hetzner server with CI/CD pipeline

#### 7.1 CI/CD Pipeline

- [ ] Task 7.1.1 - **Prompt:**

```
Create a GitHub Actions workflow file that builds and tests the application on each push to the main branch. Include steps for running the model evaluation to ensure accuracy meets requirements.
```

- [ ] Task 7.1.2 - **Prompt:**

```
Extend the GitHub Actions workflow to include deployment to the Hetzner server when changes are pushed to the main branch. Configure secrets for server access and any necessary environment variables.
```

#### 7.2 Server Configuration

- [ ] Task 7.2.1 - **Prompt:**

```
Create a deployment script that sets up the Hetzner server with all necessary dependencies including Docker and Docker Compose. Include security configuration such as a basic firewall and SSH hardening.
```

- [ ] Task 7.2.2 - **Prompt:**

```
Implement a deployment script that pulls the latest code from the repository, builds the Docker images if necessary, and starts the services using Docker Compose. Include error handling and rollback capabilities.
```

### 8. Testing and Finalisation

**Objective:** Ensure all components work together correctly and meet requirements

#### 8.1 Integration Testing

- [ ] Task 8.1.1 - **Prompt:**

```
Create an integration test script that verifies the entire application flow from drawing a digit to storing the result in the database. Test both successful and error scenarios to ensure robust error handling.
```

#### 8.2 Documentation Completion

- [ ] Task 8.2.1 - **Prompt:**

```
Complete the README.md with comprehensive documentation including project overview, architecture description, setup instructions, usage guidelines, and known limitations. Include screenshots of the application in use.
```

- [ ] Task 8.2.2 - **Prompt:**

```
Document the deployment process including how to deploy to a new server, how to update the application, and how to monitor and troubleshoot issues. Include information about the CI/CD pipeline and how it automates deployment.
```

#### 8.3 Performance Verification

- [ ] Task 8.3.1 - **Prompt:**

```
Perform performance testing to ensure all components meet the requirements: model inference time < 2 seconds, web interface responsiveness < 1 second, and database logging < 1 second per entry. Document the results.
```

## Output Expectations

- Fully functional MNIST Digit Classifier web application
- CNN model with ≥85% accuracy on MNIST test set
- Interactive drawing canvas with prediction functionality
- Database logging for predictions and user feedback
- Containerised deployment with Docker
- Automated CI/CD pipeline with GitHub Actions
- Comprehensive documentation

The implementation plan provides a structured approach to building the MNIST Digit Classifier project, breaking it down into manageable, sequential steps. Each task is designed to be completed within an hour, with clear dependencies and objectives. The LLM prompts are crafted to guide the implementation through each step, ensuring consistent progress toward a complete, functional application that meets all requirements specified in the project documentation.
