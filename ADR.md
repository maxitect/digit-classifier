# Architecture Decision Record

## For MNIST Digit Classifier

Version 0.1  
Prepared by maxitect
Machine Learning Institute (MLX)  
March 31, 2025

## Revision History

| Name     | Date           | Reason For Changes | Version |
| -------- | -------------- | ------------------ | ------- |
| maxitect | March 31, 2025 | Initial draft      | 0.1     |

## 1. Context and Problem Statement

### 1.1 Background

The MNIST Digit Classifier is an educational application demonstrating end-to-end machine learning development, containerisation, and deployment. The application allows users to draw digits on a canvas, which are then classified by a trained neural network model with results logged to a database.

Business drivers:

- Demonstrate ability to build and deploy a complete ML application
- Showcase containerisation and deployment skills
- Create a functional prototype within a tight timeframe

Technical challenges:

- Integration of multiple technologies (PyTorch, Streamlit, PostgreSQL)
- Containerisation of all components
- Rapid development with high-quality results

Constraints and limitations:

- Development timeframe: Only a couple of days
- Specific technology stack with version requirements
- Limited server resources (Hetzner basic instance)

### 1.2 Problem Definition

The architectural challenges include:

Technical requirements:

- CNN model trained on MNIST with ≥85% accuracy
- Interactive web interface with drawing capabilities
- Prediction functionality with confidence scores
- Database logging system
- Containerised deployment

System complexity:

- Integration between frontend, model service, and database
- Coordinating containerised services
- Managing data flow between components

Performance expectations:

- Model inference time: < 2 seconds
- Web interface responsiveness: < 1 second
- Database logging: < 1 second per entry

## 2. Decision Drivers

### 2.1 Technical Constraints

Key technical constraints include:

- Technology stack requirements:

  - Python 3.13.2
  - PyTorch 2.6
  - Streamlit 1.44.0
  - PostgreSQL 17.4
  - psycopg 3.2.6
  - Docker & Docker Compose

- Performance requirements:

  - Minimum model accuracy threshold
  - Quick response times for predictions
  - Responsive web interface

- Integration needs:
  - Component communication
  - Data transformation between components
  - Containerised deployment

### 2.2 Business Constraints

Business-driven architectural considerations:

- Cost limitations:

  - Hetzner basic instance (limited resources)

- Time-to-market pressures:

  - Extremely short development timeframe
  - Focus on core functionality over advanced features

- Scalability requirements:
  - Educational project with limited expected user load
  - Emphasis on demonstrating concepts rather than high scalability

## 3. Considered Alternatives

### 3.1 Monolithic Architecture

- Description: Single container housing all components (model, web interface, database)
- Pros:
  - Fastest implementation path
  - No network communication overhead
  - Simpler debugging and testing
- Cons:
  - Limited scalability
  - Tightly coupled components
  - Doesn't properly demonstrate containerisation skills
- Fit with requirements: Fails to meet containerisation requirements

### 3.2 Microservices Architecture

- Description: Fully decoupled services with robust API communication
- Pros:
  - Clean separation of concerns
  - Independent scaling of components
  - More resilient system
- Cons:
  - Significantly higher complexity
  - Challenging to implement quickly
  - Overkill for this application scope
- Fit with requirements: Meets containerisation requirements but exceeds complexity needs

### 3.3 Three-Tier Containerised Architecture

- Description: Three distinct containers with simplified communication
- Pros:
  - Clear separation of components
  - Demonstrates containerisation skills
  - Reasonable implementation complexity
- Cons:
  - Some communication overhead
  - More complex than monolithic
- Fit with requirements: Balanced approach meeting all requirements

## 4. Decision Outcome

### 4.1 Chosen Alternative

We've selected the Three-Tier Containerised Architecture with:

Core architectural pattern:

- Model Service container (PyTorch)
- Web Application container (Streamlit)
- Database container (PostgreSQL)
- Communication via HTTP for model inference
- Direct database connection for logging

Key technology choices:

- FastAPI for model service (simple, high-performance)
- Docker Compose for container orchestration
- Docker volumes for database persistence

Rationale:

- Balances separation of concerns with implementation simplicity
- Meets containerisation requirements
- Achievable within tight timeframe
- Demonstrates proper architectural patterns

### 4.2 Positive Consequences

Benefits of the chosen architecture:

- Performance advantages:

  - Dedicated model container optimised for inference
  - FastAPI provides high-performance for prediction requests
  - Streamlined data flow between components

- Scalability benefits:

  - Independent scaling of components if needed
  - Clear component boundaries enable future enhancements
  - Container-based deployment enables horizontal scaling

- Maintainability improvements:
  - Clear separation simplifies code management
  - Independent containers allow isolated updates
  - Docker Compose provides unified deployment

### 4.3 Negative Consequences

Potential drawbacks:

- Known limitations:

  - Network communication adds some latency
  - More complex deployment than single container
  - Requires proper error handling between services

- Future considerations:

  - Basic API implementation may need enhancement later
  - Simplified error handling sufficient for demo but not production

- Complexity trade-offs:
  - More moving parts than monolithic approach
  - Docker networking requires proper configuration
  - Inter-service dependencies must be managed

## 5. Technical Architecture

### 5.1 System Components

The system comprises three main components:

- Model Service:

  - Loads trained CNN model
  - Provides prediction API endpoints
  - Processes image data for inference
  - Returns predictions with confidence scores

- Web Application:

  - Presents drawing canvas to users
  - Communicates with model service for predictions
  - Displays prediction results
  - Collects true labels from users
  - Initiates database logging

- Database Service:
  - Stores prediction logs
  - Maintains data persistence

Interaction patterns:

- Web app sends image data to model service via HTTP
- Model service returns prediction results as JSON
- Web app logs predictions to database via direct connection

### 5.2 Technical Interfaces

Key technical interfaces:

- Model Service API:

  - POST /predict endpoint accepting image data
  - Returns JSON with predicted digit and confidence scores

- Database Interface:

  - "predictions" table with timestamp, prediction, confidence, true label
  - Direct SQL operations via psycopg

- Web UI Elements:
  - Canvas for digit drawing
  - Prediction display area
  - True label input field

Data exchange:

- Base64-encoded image data for API requests
- JSON for prediction responses
- SQL for database operations

### 5.3 Performance Considerations

Performance optimisation strategies:

- Efficient processing:

  - Model loaded once at service startup
  - Optimised image preprocessing pipeline
  - Minimal data transformations

- Resource management:

  - Appropriate container resource allocation
  - Efficient database operations for logging
  - Lightweight communication protocols

- User experience:
  - Responsive canvas implementation
  - Immediate feedback on prediction
  - Clear error handling

### 5.4 Security Architecture

Security considerations:

- Configuration security:

  - Environment variables for sensitive configuration
  - PostgreSQL credentials managed via Docker secrets

- Network security:

  - Server firewall limiting exposed ports
  - Docker networks for proper service isolation
  - Internal communication between containers

- Data handling:
  - No personally identifiable information collected
  - Basic input validation

## 6. Technology Stack

### 6.1 Frontend Technologies

- Streamlit 1.44.0:

  - Primary web framework
  - Interactive components
  - Responsive layout

- HTML5 Canvas:
  - Drawing implementation
  - Image capture for prediction

### 6.2 Backend Technologies

- Python 3.13.2:

  - Primary programming language

- PyTorch 2.6:

  - CNN model implementation
  - MNIST training and inference

- FastAPI:

  - Model service API framework
  - Request/response handling

- psycopg 3.2.6:

  - PostgreSQL connectivity
  - Database operations

- PostgreSQL 17.4:
  - Prediction logging database

### 6.3 Infrastructure

- Docker:

  - Application containerisation
  - Multi-container orchestration via Docker Compose
  - Volume management for persistence

- Deployment:
  - Hetzner basic instance
  - GitHub Actions CI/CD pipeline
  - Container orchestration via Docker Compose

## 7. Monitoring and Observability

### 7.1 Logging Strategy

- Application logging:

  - Standard Python logging
  - Container stdout/stderr capture
  - Critical error reporting

- Database logging:
  - Prediction history
  - User feedback (true labels)
  - Timestamp information

### 7.2 Performance Monitoring

- Basic metrics:

  - Request timing for model inference
  - API response times
  - Database operation performance

- Implementation:
  - Simple logging of key metrics
  - Manual review process
  - No complex monitoring due to project scope

## 8. Future Considerations

### 8.1 Potential Evolutions

Potential architecture improvements:

- Enhanced model:

  - More sophisticated CNN architecture
  - Model versioning and A/B testing
  - Explainability features

- Extended functionality:

  - User accounts and history
  - Training feedback loop
  - More advanced visualisations

- Infrastructure upgrades:
  - More robust hosting
  - Proper load balancing
  - Enhanced monitoring

### 8.2 Technical Debt

Areas for future improvement:

- Known limitations:

  - Basic error handling
  - Limited monitoring
  - Simplified security implementation

- Potential improvements:

  - More comprehensive testing
  - Enhanced API design
  - Better failure recovery mechanisms

- Future refactoring:
  - More modular codebase
  - Enhanced configuration management
  - Production-ready security enhancements

## 9. Appendixes

### Appendix A: Architectural Diagrams

```
┌─────────────────┐     HTTP     ┌─────────────────┐
│                 │─────────────▶│                 │
│  Web App        │              │  Model Service  │
│  (Streamlit)    │◀────────────│  (PyTorch)      │
│                 │   JSON       │                 │
└────────┬────────┘              └─────────────────┘
         │
         │ SQL
         ▼
┌─────────────────┐
│                 │
│  Database       │
│  (PostgreSQL)   │
│                 │
└─────────────────┘
```

### Appendix B: Technology Evaluation Details

**Web Framework Evaluation:**

- Streamlit: Chosen for rapid development, interactive components, and ML focus
- Flask: Considered but requires more boilerplate for UI
- Dash: Good alternative but less familiar than Streamlit

**Model Service API:**

- FastAPI: Selected for performance, simplicity, and automatic documentation
- Flask: Good alternative but marginally slower
- Direct integration: Rejected to maintain container separation

**Database Options:**

- PostgreSQL: Selected for reliability and Docker support
- SQLite: Simpler but lacks robustness for containerisation
- MongoDB: Overkill for simple logging requirements
