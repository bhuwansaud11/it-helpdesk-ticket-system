class TicketManager:
    def __init__(self):
        self.tickets = []
        self.next_id = 1

    def create_ticket(self, requester_name, department, title,
                      description, priority):
        if not requester_name.strip():
            raise ValueError("Requester name cannot be empty")
        if not department.strip():
            raise ValueError("Department cannot be empty")
        if not title.strip():
            raise ValueError("Ticket title cannot be empty")
        if not description.strip():
            raise ValueError("Description cannot be empty")
        if priority not in ["Low", "Medium", "High"]:
            raise ValueError("Priority must be Low, Medium or High")

        ticket = {
            "id": self.next_id,
            "requester_name": requester_name,
            "department": department,
            "title": title,
            "description": description,
            "priority": priority,
            "status": "Open",
            "assigned_to": None
        }
        self.tickets.append(ticket)
        self.next_id += 1
        return ticket

    def get_all_tickets(self):
        return self.tickets

    def get_ticket(self, ticket_id):
        for ticket in self.tickets:
            if ticket["id"] == ticket_id:
                return ticket
        raise ValueError("Ticket not found")

    def update_status(self, ticket_id, status):
        if status not in ["Open", "In Progress", "Resolved"]:
            raise ValueError("Invalid status")
        ticket = self.get_ticket(ticket_id)
        ticket["status"] = status
        return ticket

    def assign_ticket(self, ticket_id, agent_name):
        if not agent_name.strip():
            raise ValueError("Agent name cannot be empty")
        ticket = self.get_ticket(ticket_id)
        ticket["assigned_to"] = agent_name
        return ticket

    def delete_ticket(self, ticket_id):
        ticket = self.get_ticket(ticket_id)
        self.tickets.remove(ticket)
        return {"message": "Ticket deleted successfully"}

    def search_tickets(self, keyword):
        keyword = keyword.strip().lower()
        return [
            ticket for ticket in self.tickets
            if keyword in ticket["requester_name"].lower()
            or keyword in ticket["department"].lower()
        ]

    def filter_tickets(self, priority=None, status=None):
        results = self.tickets
        if priority:
            results = [t for t in results if t["priority"] == priority]
        if status:
            results = [t for t in results if t["status"] == status]
        return results
