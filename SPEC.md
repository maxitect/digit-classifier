# Functional Specification

## For MNIST Digit Classifier

Version 0.1  
Prepared by maxitect
Machine Learning Institute (MLX)  
March 31, 2025

## Revision History

| Name     | Date           | Reason For Changes | Version |
| -------- | -------------- | ------------------ | ------- |
| maxitect | March 31, 2025 | Initial draft      | 0.1     |

## 1. Introduction

### 1.1 Document Purpose

This document provides a comprehensive overview of the functional requirements and core objectives for the MNIST Digit Classifier project as part of an application to the Machine Learning Institute (MLX) programme.

### 1.2 Product Scope

The MNIST Digit Classifier is an educational project that demonstrates end-to-end machine learning application development, containerisation, and deployment. The application allows users to draw digits on a canvas, which are then classified by a trained neural network model. Results are logged to a database for potential future analysis.

### 1.3 Definitions, Acronyms and Abbreviations

- **MNIST**: Modified National Institute of Standards and Technology database - a large database of handwritten digits used for training image processing systems
- **CNN**: Convolutional Neural Network - a class of deep neural networks commonly used for image analysis
- **CI/CD**: Continuous Integration/Continuous Deployment - automated workflow for software development
- **MLX**: Machine Learning Institute

### 1.4 References

- MNIST Dataset: http://yann.lecun.com/exdb/mnist/
- PyTorch Documentation: https://pytorch.org/docs/
- Streamlit Documentation: https://docs.streamlit.io/
- Docker Documentation: https://docs.docker.com/

### 1.5 Document Overview

This document outlines the requirements, constraints, and implementation details for the MNIST Digit Classifier. It serves as a guide for development and deployment of the application.

## 2. Product Overview

### 2.1 Product Perspective

This is a new, standalone project developed as an application exercise for the MLX programme. It demonstrates the ability to build, containerise, and deploy a complete machine learning application.

### 2.2 Product Functions

- Train a CNN model on the MNIST dataset to classify handwritten digits
- Provide a web interface for users to draw digits and submit for classification
- Display prediction results and confidence scores
- Allow users to provide correct labels for drawn digits
- Log prediction details to a PostgreSQL database
- Containerise all components using Docker
- Deploy the application to a self-managed server

### 2.3 Product Constraints

- Development timeframe: Must be completed within the next couple of days
- Minimum model accuracy: 85% on MNIST test set
- Infrastructure: Self-managed server (Hetzner basic instance)
- Technological constraints: Specified technology stack and versions

### 2.4 User Characteristics

The primary users will be evaluators from the Machine Learning Institute who will assess the technical implementation and functionality of the application. These users will be technically proficient and familiar with machine learning concepts.

### 2.5 Assumptions and Dependencies

- Users have a modern web browser with JavaScript enabled
- The Hetzner server instance is available and accessible
- Internet connectivity is stable for deployment and access
- The specified versions of tools and libraries are compatible

### 2.6 Apportioning of Requirements

#### Must-have features:

- CNN model trained on MNIST with at least 85% accuracy
- Interactive web interface with drawing canvas
- Prediction functionality with confidence score display
- PostgreSQL database logging
- Docker containerisation of all components
- Deployment to self-managed server
- CI/CD pipeline for deployment

#### Should-have features:

- Error handling and fallback mechanisms
- Clear, responsive user interface
- Data persistence for the database

#### Could-have features:

- Additional model visualisations
- Performance optimisations

#### Won't-have features:

- User authentication
- Advanced monitoring or analytics
- Custom domain name

## 3. Requirements

### 3.1 External Interfaces

#### 3.1.1 User Interfaces

- Web-based interface using Streamlit
- Square, responsive drawing canvas with clear functionality
- Display area for prediction results and confidence scores
- Input field for users to provide the true label
- Clear error messages when issues occur

#### 3.1.2 Hardware Interfaces

- Deployment on Hetzner basic instance or equivalent self-managed server

#### 3.1.3 Software Interfaces

- PyTorch 2.6 for model development and inference
- Streamlit 1.44.0 for web interface
- PostgreSQL 17.4 for database
- Python 3.13.2 as the primary programming language
- psycopg 3.2.6 for database connectivity
- Docker and Docker Compose for containerisation

### 3.2 Functional Requirements

#### 3.2.1 Model Development

- Develop a CNN model using PyTorch 2.6
- Train on the MNIST dataset
- Achieve minimum 85% accuracy on the test set
- Save model for inference in the web application

#### 3.2.2 Web Interface

- Implement using Streamlit 1.44.0
- Provide a square, responsive drawing canvas
- Include a clear button to reset the canvas
- Submit button to send the drawing for classification
- Display the predicted digit and confidence score
- Allow users to input the true label
- Implement appropriate error handling and fallbacks

#### 3.2.3 Database Logging

- Use PostgreSQL 17.4
- Create a "predictions" table with incremental serial indices
- Log the following for each prediction:
  - Timestamp
  - Predicted digit
  - Confidence score
  - User-provided true label
- Ensure data persistence through Docker volumes

#### 3.2.4 Containerisation

- Create Docker containers for each component:
  - PyTorch model service
  - Streamlit web application
  - PostgreSQL database
- Develop a docker-compose.yml file to define the multi-container setup
- Configure volumes for database data persistence

#### 3.2.5 Deployment

- Set up a Hetzner basic instance or equivalent
- Configure the server with Docker and necessary dependencies
- Implement CI/CD pipeline for deployment
- Deploy the application with public IP access
- Document the deployment process in the GitHub README

#### 3.2.6 GitHub Integration

- Create a GitHub repository for the project
- Include comprehensive README with:
  - Project overview
  - Setup instructions
  - Link to the live application (IP address)
  - Usage guidelines
- Commit all code, configuration files, and documentation

### 3.3 Quality of Service

#### 3.3.1 Performance

- Model inference time: < 2 seconds per prediction
- Web interface responsiveness: < 1 second for UI interactions
- Database logging: < 1 second per entry

#### 3.3.2 Security

- Secure PostgreSQL database with strong credentials
- Use environment variables for sensitive configuration
- Implement proper Docker security practices
- Configure server firewall to expose only necessary ports

#### 3.3.3 Reliability

- Application should handle invalid inputs gracefully
- Implement error handling and fallbacks for all critical functions
- Ensure database persistence through Docker volumes

#### 3.3.4 Availability

- The application should be accessible 24/7 via the server IP address

### 3.4 Compliance

No specific compliance requirements beyond standard software development practices.

### 3.5 Design and Implementation

#### 3.5.1 Installation

- Docker-based installation requiring minimal manual steps
- Requirements documented in the GitHub README

#### 3.5.2 Distribution

- Accessible via server IP address
- Source code available on GitHub

#### 3.5.3 Maintainability

- Clear code structure with appropriate comments
- Separation of concerns between model, interface, and database
- Use of Docker for consistent environments

#### 3.5.4 Reusability

- Modular components that can be repurposed for similar projects
- Clearly defined interfaces between components

#### 3.5.5 Portability

- Docker containerisation ensures portability across environments
- Explicit version specifications for all dependencies

#### 3.5.6 Cost

- Hetzner basic instance or equivalent low-cost server

#### 3.5.7 Deadline

- Project to be completed within the next couple of days

#### 3.5.8 Proof of Concept

- Functional prototype demonstrating end-to-end workflow:
  - Drawing a digit
  - Receiving a prediction
  - Logging the result to the database

## 4. Verification

- Model accuracy validated against MNIST test dataset (≥ 85%)
- End-to-end testing of the web interface and prediction functionality
- Database logging verification
- Deployment testing on target server
- Cross-browser testing for the web interface

## 5. Appendixes

### Appendix A: Glossary

- **MNIST**: A large database of handwritten digits commonly used for training various image processing systems.
- **CNN**: Convolutional Neural Network, a class of deep neural networks most commonly applied to analyzing visual imagery.
- **Docker**: A platform used to develop, ship, and run applications inside containers.
- **Container**: A standard unit of software that packages up code and all its dependencies.
- **CI/CD**: Continuous Integration/Continuous Deployment, practices that involve automatically building, testing, and deploying code changes.
- **PostgreSQL**: An open-source relational database system.
- **Streamlit**: An open-source app framework for Machine Learning and Data Science teams.
- **PyTorch**: An open-source machine learning framework based on the Torch library.

### Appendix B: Technical Stack Details

- Python 3.13.2
- PyTorch 2.6
- psycopg 3.2.6
- PostgreSQL 17.4
- Streamlit 1.44.0
- Docker & Docker Compose
