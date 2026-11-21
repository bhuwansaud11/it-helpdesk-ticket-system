# IT Helpdesk Ticket Management System

## Project Description
A Python REST API for creating, assigning and tracking internal IT support tickets.

## Technologies
- Python
- FastAPI
- Pytest and pytest-cov
- Git and GitHub
- Docker
- Terraform

## Features
- Create and view support tickets
- Retrieve a ticket by ID
- Update ticket status
- Assign tickets to support agents
- Delete tickets
- Search by requester or department
- Filter by priority and status

## Install
```
python -m venv venv
# Windows PowerShell: .\venv\Scripts\Activate.ps1
# Linux/macOS: source venv/bin/activate
pip install -r requirements.txt
```

## Run locally
```
uvicorn app.main:app --reload
```

## API documentation
http://127.0.0.1:8000/docs

## Test
```
pytest -v
```

## Coverage
```
pytest --cov=app --cov-report=html
```

## Docker
```
docker build -t it-helpdesk-app:v1 .
docker run -d -p 8000:8000 --name it-helpdesk-container it-helpdesk-app:v1
```

## Terraform
```
cd terraform
terraform init
terraform plan
terraform apply
terraform destroy
```

## Data note
This training project uses in-memory sample data. Data resets when the API process or container restarts.
