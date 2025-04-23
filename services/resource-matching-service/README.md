# EmpowerLink Nexus · Resource Matching Service

This microservice provides resource‐matching functionality for EmpowerLink Nexus: given a user request, it returns nearby clinic, legal, or social support resources ranked by proximity and other attributes.

---

## Table of Contents

1. [Features](#features)  
2. [Architecture](#architecture)  
3. [Getting Started](#getting-started)  
   - [Prerequisites](#prerequisites)  
   - [Installation](#installation)  
   - [Configuration](#configuration)  
   - [Initializing the Database](#initializing-the-database)  
4. [Running Locally](#running-locally)  
   - [REST API](#rest-api)  
   - [GraphQL API](#graphql-api)  
5. [AI Model](#ai-model)  
   - [Training the Model](#training-the-model)  
   - [Artifacts](#artifacts)  
6. [Docker](#docker)  
7. [CI/CD](#ci-cd)  
8. [Testing](#testing)  
9. [Contributing](#contributing)  
10. [License](#license)  

---

## Features

- **Nearest-Neighbor Matching**: content-based KNN on user⃗request vs. resources⃗profiles.  
- **REST endpoints** for simple JSON requests.  
- **GraphQL** for flexible querying and mutations.  
- **AI pipeline**:  
  - `ColumnTransformer` → OneHot + StandardScaler  
  - `NearestNeighbors` persisted  
- **Dockerized** for easy deployment.  
- **Automated CI/CD** on GitHub Actions.  
- **Unit tests** covering transformer & matching logic.

---

## Architecture

```Plaintext
────────────┐ ┌───────────────┐ ┌────────────┐ │ Client / │ ─────>│ API Gateway │ ────>│ This SVC │ │ Frontend │ └───────────────┘ └────────────┘ │ (REST/GRPC)│ ▲ └────────────┘ │ ┌────────────┐ │ Database │ └────────────┘ ▲ │ ┌────────────┐ │ AI Model │ └────────────┘

yaml
Copy
Edit

```

---

## Getting Started

### Prerequisites

- Python 3.10  
- pip (or pipenv / poetry)  
- Docker & Docker Compose (for containerized setup)  
- (Optional) PostgreSQL, or use bundled SQLite  

### Installation

```bash
git clone https://github.com/EmpowerLink-Nexus/services.git
cd services/resource-matching-service

python -m venv .venv
source .venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```
