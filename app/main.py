from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from app.ticket_manager import TicketManager

app = FastAPI(
    title="IT Helpdesk Ticket Management System",
    description="DevOps Integrated Practical Project",
    version="1.0"
)

manager = TicketManager()


class TicketRequest(BaseModel):
    requester_name: str = Field(min_length=1)
    department: str = Field(min_length=1)
    title: str = Field(min_length=1)
    description: str = Field(min_length=1)
    priority: str


class StatusRequest(BaseModel):
    status: str


class AssignmentRequest(BaseModel):
    agent_name: str = Field(min_length=1)


@app.get("/")
def home():
    return {"message": "IT Helpdesk API is running"}


@app.post("/tickets", status_code=201)
def create_ticket(request: TicketRequest):
    try:
        return manager.create_ticket(
            request.requester_name,
            request.department,
            request.title,
            request.description,
            request.priority
        )
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error))


@app.get("/tickets")
def get_all_tickets():
    return manager.get_all_tickets()


@app.get("/tickets/{ticket_id}")
def get_ticket(ticket_id: int):
    try:
        return manager.get_ticket(ticket_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@app.put("/tickets/{ticket_id}/status")
def update_status(ticket_id: int, request: StatusRequest):
    try:
        return manager.update_status(ticket_id, request.status)
    except ValueError as error:
        status_code = 404 if str(error) == "Ticket not found" else 400
        raise HTTPException(status_code=status_code, detail=str(error))


@app.put("/tickets/{ticket_id}/assign")
def assign_ticket(ticket_id: int, request: AssignmentRequest):
    try:
        return manager.assign_ticket(ticket_id, request.agent_name)
    except ValueError as error:
        status_code = 404 if str(error) == "Ticket not found" else 400
        raise HTTPException(status_code=status_code, detail=str(error))


@app.delete("/tickets/{ticket_id}")
def delete_ticket(ticket_id: int):
    try:
        return manager.delete_ticket(ticket_id)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error))


@app.get("/tickets/search/{keyword}")
def search_tickets(keyword: str):
    return manager.search_tickets(keyword)


@app.get("/ticket-filters")
def filter_tickets(priority: str = None, status: str = None):
    return manager.filter_tickets(priority, status)
