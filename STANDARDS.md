# Project Standards and Implementation Plan

## For MNIST Digit Classifier

Version 0.1  
Prepared by maxitect  
Machine Learning Institute (MLX)  
April 2, 2025

## Revision History

| Name     | Date          | Reason For Changes | Version |
| -------- | ------------- | ------------------ | ------- |
| maxitect | April 2, 2025 | Initial draft      | 0.1     |

## 1. Development Methodology

### 1.1 Chosen Methodology

- Solo development with checkpoints
- Development milestones tied to completion of major components:
  - Model training and validation
  - Model service API implementation
  - Web interface implementation
  - Database integration
  - Containerisation
  - Deployment
- Self-validation at each checkpoint before proceeding

### 1.2 Team Structure

- Single developer responsible for all aspects of the project
- Clear separation of concerns between components to maintain focus

## 2. Coding Standards

### 2.1 General Coding Principles

- Prioritise modularity, code reusability and maintainability at all times
- Follow PEP 8 coding style for all Python code
- Use flake8 linter in VS Code to enforce standards
- Emphasise readability and maintainability
- Apply KISS (Keep It Simple, Stupid) principles throughout
- Use comments sparingly, only when code is not self-explanatory
- Use docstrings only for generic functions or classes reused across multiple files

### 2.2 Language-Specific Standards

#### 2.2.1 Frontend Standards

- Streamlit component organisation:
  - Group related UI elements
  - Clear separation between drawing, prediction, and logging functionality
- Use Streamlit's native components when possible
- Minimise custom JavaScript to essential canvas functionality
- Responsive design to ensure usability across devices

#### 2.2.2 Backend Standards

- Model Service:
  - Clean separation between model loading, preprocessing, and inference
  - Clear API endpoint definitions with FastAPI
  - Appropriate error handling for invalid inputs
- Database Interface:
  - Code-first approach to schema management
  - Simple, direct queries using psycopg
  - Parameterised queries to prevent SQL injection

### 2.3 Code Review Process

- No formal code review process required for this solo project

## 3. Version Control

### 3.1 Repository Management

- Single main branch workflow
- Direct commits to main branch
- No feature branching required for this project timeline

### 3.2 Commit Standards

- Use [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
- Descriptive commit messages
- Logical commits tied to completion of specific features or fixes
- Avoid committing sensitive information (use .gitignore for .env files)

## 4. Testing Strategy

### 4.1 Testing Types

- Lightweight testing approach focused on essentials:
  - Model accuracy validation against MNIST test set (≥ 85%)
  - Basic API endpoint testing for model service
  - Manual testing of the web interface
- No formal unit testing required given time constraints
- No end-to-end automated testing required

### 4.2 Test Coverage

- Focus on critical functionality:
  - Model inference accuracy
  - Image preprocessing pipeline
  - Database logging reliability
- Manual validation of the complete workflow

### 4.3 Continuous Integration

- Simple GitHub Actions workflow for:
  - Automated testing of model accuracy
  - Deployment to the Hetzner server
  - Basic validation of container startup

## 5. Quality Assurance

### 5.1 Code Quality

- flake8 for linting and PEP 8 enforcement
- Manual review of code before deployment
- Focus on readability and simplicity

### 5.2 Performance Monitoring

- Performance benchmarks:
  - Model inference time: < 2 seconds per prediction
  - Web interface responsiveness: < 1 second for UI interactions
  - Database logging: < 1 second per entry
- Minimalist approach to performance logging
- Manual validation of performance metrics

## 6. Technical Debt Management

### 6.1 Identification

- Document known limitations in GitHub README
- Distinguish between essential improvements and nice-to-haves
- Focus on completing core functionality first

### 6.2 Mitigation Strategies

- Clear documentation of technical compromises
- Recommendations for future improvements
- Modular architecture to facilitate future enhancements

## 7. Implementation Roadmap

### 7.1 Project Phases

- Initial setup (Day 1, Morning):
  - Repository creation
  - Environment configuration
  - Basic project structure
- Model development (Day 1, Afternoon):
  - CNN implementation
  - MNIST training
  - Accuracy validation
- Service implementation (Day 1, Evening):
  - FastAPI model service
  - Image preprocessing pipeline
  - API endpoint testing
- Web interface (Day 2, Morning):
  - Streamlit application
  - Drawing canvas implementation
  - Integration with model service
- Database integration (Day 2, Afternoon):
  - PostgreSQL schema setup
  - Logging implementation
  - Data persistence configuration
- Containerisation (Day 2, Evening):
  - Docker configuration
  - Multi-container orchestration
  - Local testing
- Deployment (Day 2, Night):
  - CI/CD pipeline setup
  - Hetzner server deployment
  - Final testing and documentation

### 7.2 Milestones

- Working model with ≥85% accuracy
- Functional model service API
- Interactive web interface
- Integrated database logging
- Containerised application
- Deployed application on Hetzner server
- Complete documentation in GitHub README

### 7.3 Resource Allocation

- Single developer focus on all aspects
- Prioritisation based on component dependencies
- Time allocation aligned with project phases

## 8. Documentation Standards

### 8.1 Code Documentation

- Minimal inline comments for clarity
- Docstrings only for reusable components
- Clear variable and function naming following PEP 8

### 8.2 External Documentation

- Comprehensive GitHub README including:
  - Project overview
  - Architecture description
  - Setup instructions
  - Usage guidelines
  - Link to deployed application
  - Known limitations
  - Future improvement ideas

## 9. Security Standards

### 9.1 Secure Coding Practices

- Basic security best practices:
  - Input validation for all user-provided data
  - Parameterised SQL queries
  - Proper error handling without exposing internals
  - Environment variables for configuration

### 9.2 Data Protection

- Use of .env files for environment variables
- .gitignore configuration to exclude sensitive files
- No collection of personally identifiable information
- Server firewall configuration to limit exposed ports

## 10. Compliance and Governance

### 10.1 Regulatory Compliance

- No specific regulatory requirements for this educational project

### 10.2 Ethical Considerations

- Transparent documentation of system capabilities and limitations
- Clear attribution for MNIST dataset and any other resources

## 11. Appendixes

### Appendix A: Tools and Technologies

- Python 3.13.2
- PyTorch 2.6
- Streamlit 1.44.0
- PostgreSQL 17.4
- psycopg 3.2.6
- Docker & Docker Compose
- Anaconda for environment management
- VS Code with flake8 linting
- GitHub for version control
- GitHub Actions for CI/CD
- Hetzner basic instance for deployment

### Appendix B: Environment Setup

- Anaconda environment.yml for dependency management
- Conda-based Docker images
- Environment variables managed through .env files
- PostgreSQL data persistence through Docker volumes
