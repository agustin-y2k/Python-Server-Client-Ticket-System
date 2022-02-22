from sqlalchemy import String, Integer, Column, Date, DateTime, MetaData
import json
from db_config import Base


# Ticket class
class Ticket(Base):
    __tablename__ = "tickets"
    ticket_Id = Column(Integer, primary_key=True)
    title = Column(String(45), nullable=False)
    author = Column(String(45), nullable=False)
    description = Column(String(300), nullable=False)
    status = Column(String(45), nullable=False)
    date = Column(Date, nullable=False)

    # Returns ticket as a string
    def __repr__(self):
        return '<Ticket: %r %r %r %r %r %r>' % (self.ticket_Id, self.title, self.author,
                                                self.description, self.status, self.date)

    # Constructor of the Ticket class
    def __init__(self, title, author, description, status, date):
        self.title = title
        self.author = author
        self.description = description
        self.status = status
        self.date = date

    # Convert a ticket object to JSON format
    def toJSON(self):
        ticket_json = {
            'ticket_Id': self.ticket_Id,
            'title': self.title,
            'author': self.author,
            'description': self.description,
            'status': self.status,
            'date': str(self.date)
        }
        return ticket_json


# JSON serializer class
# json.JSONEncoder -> Extensible JSON encoder for Python data structures.
class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Ticket):
            return {"ticket_Id": obj.ticket_Id, "title": obj.title, "author": obj.author,
                    "description": obj.description, "status": obj.status,
                    "date": str(obj.date)}
        return json.JSONEncoder.default(self, obj)


# Table creator
Base.metadata.create_all()
