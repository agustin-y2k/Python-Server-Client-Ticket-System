from sqlalchemy.orm.exc import NoResultFound
import getopt
import socket
import sys
import json
from datetime import date
from db_config import *
from model import *

from sqlalchemy.orm.exc import NoResultFound

from db_config import *
from model import *


# Create server socket
def create_server_socket():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    return server_socket


# Establish connection between server and socket
def connection_server_client(server_socket):
    (opt, arg) = getopt.getopt(sys.argv[1:], 'p:')
    for (op, ar) in opt:
        if op == '-p':
            p = int(ar)

        host = ""
        port = p
        server_socket.bind((host, port))
        server_socket.listen(1)


# Server creates a ticket
def server_create_ticket(dictionary):
    ticket = Ticket(title=dictionary['title'], author=dictionary['author'], description=dictionary['description'],
                    status=dictionary['status'], date=date.today())
    session.add(ticket)
    session.commit()


# Server list tickets
def server_list_tickets():
    tickets = session.query(Ticket).all()
    session.commit()
    return tickets


# Save ticket edited by the client in the database
def server_edit_ticket(id, values):
    ticket = session.query(Ticket).get(int(id))
    json_values = json.loads(values)
    ticket.title = json_values['title']
    ticket.description = json_values['description']
    ticket.status = json_values['status']
    session.add(ticket)
    session.commit()
    return ticket


# Get ticket by ID
def get_ticket_ById(id):
    ticket = session.query(Ticket).get(int(id))
    return ticket.toJSON()


# Verify ticket by ID
def verify_ticketId(ticket_id):
    try:
        session.query(Ticket).filter(Ticket.ticket_id == ticket_id).one()
        verify_return_server_ticket = True
    except NoResultFound:
        verify_return_server_ticket = False
    return verify_return_server_ticket


# Filter by author
def ticket_filter_byAuthor(argument, ticket):
    ticket = ticket.filter(Ticket.author == argument)
    return ticket


# Filter by status
def ticket_filter_by_status(argument, ticket):
    ticket = ticket.filter(Ticket.status == argument)
    return ticket


# Filter by date
def ticket_filter_by_date(argument, ticket):
    ticket = ticket.filter(Ticket.date == argument)
    return ticket


# Server ticket filter
def server_ticket_filter(sock):
    ticket = get_argument_byClient(sock)
    ticket_loads = json.loads(ticket)
    tickets = session.query(Ticket).filter()
    for k, v in dict(ticket_loads).items():
        if k == 'author':
            tickets = ticket_filter_byAuthor(ticket_loads['author'], tickets)
        if k == 'status':
            tickets = ticket_filter_by_status(ticket_loads['status'], tickets)
        if k == 'date':
            tickets = ticket_filter_by_date(ticket_loads['date'], tickets)
    return tickets


# Get argument send by client
def get_argument_byClient(sock):
    argument = sock.recv(1024).decode()
    return argument


# Admin a server log history
def server_history_log(ticket_date, option, address):
    history_file = open('server_history.log', 'a')
    history_file.write(f"\n Date: {ticket_date}, Option: {option}, Client %s:%d" % address)
    history_file.close()


# Get tickets selected and send amount of tickets
def get_tickets_ByAmount(ticket_list, sock, amount):
    amount_integer = int(amount)
    for ticket in ticket_list[0:amount_integer]:
        ticket_obj = json.dumps(ticket, cls=MyEncoder)
        sock.send(ticket_obj.encode())


# Verify amount tickets 
def verify_amount_tickets(amount):
    if amount == 0:
        amount_verify = False
    else:
        amount_verify = True
    return amount_verify
