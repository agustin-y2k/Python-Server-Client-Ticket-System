import csv
import getopt
import json
import socket
import sys
import zipfile
from getopt import GetoptError
from multiprocessing import Process
from random import randint

from model import MyEncoder


# Create the Socket from the Client side.
def create_socket_client():
    try:
        socket_client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    except socket.error:
        print('Failed to create socket!')
        sys.exit()

    return socket_client


# Establishes the connection between the Client and the Server.
def client_server_connection(client):
    (opt, arg) = getopt.getopt(sys.argv[1:], 'h:p:')
    for (op, ar) in opt:
        if op == '-h':
            h = str(ar)
        elif op == '-p':
            p = int(ar)

    print('Socket created!')
    host = h
    port = p
    client.connect((host, port))
    print('Socket connected to host', host, 'in the port', port)
    return client


# Client enters the data of the Ticket to create
def client_create_ticket():
    title = input("Title: ")
    author = input("Author: ")
    description = input("Description: ")
    print("Status only can be... pending - in process - approved")
    status = input("Status: ")

    if status == 'pending' or status == 'in process' or status == 'approved':
        print("\n")
    else:
        print("Status only can be... pending - in process - approved")
        status = input("Status: ")
    ticket = {"title": title, "author": author, "description": description, "status": status}
    return ticket


# Show ticket list
def show_ticket_list(tickets):
    for ticket in tickets:
        ticket_dict = json.loads(ticket)
        print("\n", "Ticket_Id:", ticket_dict['ticket_Id'], "Title: ", ticket_dict['title'], "Author: ",
              ticket_dict['author'], "Description: ", ticket_dict['description'], "Status: ", ticket_dict['status'],
              "Date: ", ticket_dict['date'])


# Show one ticket
def show_ticket(ticket):
    print("\n", "Ticket_Id:", ticket['ticket_Id'], "Title: ", ticket['title'], "Author: ", ticket['author'],
          "Description: ", ticket['description'], "Status: ", ticket['status'], "Date: ", ticket['date'])


# Edit tickets
def edit_ticket(ticket):
    ticket_dict = json.loads(ticket)
    print("\n", "Choose ticket to edit")
    show_ticket(ticket_dict)
    print("\n")
    exit = False
    while not exit:
        print("Option: t(title) d(Description) s(Status) q(exit)", "\n")
        option = input("Option: ")
        print("\n")

        if option == 't':
            ticket_dict['title'] = input("Title: ")
        elif option == 'd':
            ticket_dict['description'] = input("Description: ")
        elif option == 's':
            ticket_dict['status'] = input("Status: ")
            if ticket_dict['status'] == ticket_dict['status'] == 'pending' or ticket_dict['status'] == 'in-process' or \
                    ticket_dict['status'] == 'approved':
                print("\n")
            else:
                print("Status only can be... pending - In process - approved")
                ticket_dict['status'] = input("Status: ")
        elif option == 'q':
            exit = True
        else:
            print("Invalid option!")

        print("\n", "Ticket edited")
        print("")
        show_ticket(ticket_dict)
        print("")
        dictionary = {"ticket_Id": ticket_dict['ticket_Id'], "title": ticket_dict['title'],
                      "author": ticket_dict['author'],
                      "description": ticket_dict['description'], "status": ticket_dict['status'],
                      "date": ticket_dict['date']}
        return dictionary


# Filter tickets according to the entered commands
def client_ticket_filter(client):
    print("Filter by... \nAuthor -> -a + author \nStatus -> -s + status \nDate -> -d + YYYY-MM-DD \nAll -> -l")
    print("You can take two or more filter argument, example: -a + author and -s + status")
    keywords = input("-a -s -d -l: ").split(" ")
    ticket = {}
    try:
        (opts, args) = getopt.getopt(keywords, 'a:s:d:l')
        for op, ar in opts:
            if op in '-a':
                argument = ar
                ticket['author'] = argument
            elif op in ['-s']:
                argument = ar
                ticket['status'] = argument
            elif op in ['-d']:
                argument = ar
                ticket['date'] = argument
            elif op in ['-l']:
                break
            else:
                print("Invalid option!")

        ticket_dict = json.dumps(ticket, cls=MyEncoder)
        send_argument(ticket_dict, client)
    except GetoptError:
        print("Invalid option!")
        client_ticket_filter(client)
    return ticket


# Send argument to the server
def send_argument(argument, client):
    argument_str = str(argument)
    client.send(argument_str.encode())


# Receive the amount entered by the user to print that amount of Tickets
def get_tickets(client, amount):
    amount_integer = int(amount)
    tickets = []
    for x in range(amount_integer):
        tickets.append(client.recv(1024).decode())
    print("Added Tickets: ", len(tickets))
    show_ticket_list(tickets)


# Export tickets in a csv file compressed on .zip
def client_export_ticket(list):
    with open("tickets.csv", "w", newline='') as f:
        fieldnames = ['ticket_Id', 'title', 'author', 'description', 'status', 'date']
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for ticket in list:
            ticket_dict = json.loads(ticket)
            writer.writerow(ticket_dict)

    jungle_zip = zipfile.ZipFile('tickets.zip' + str(randint(1, 10000)), 'w')
    jungle_zip.write('tickets.csv', compress_type=zipfile.ZIP_DEFLATED)
    jungle_zip.close()


# Receives the amount entered by the user and then prints that number of Tickets.
def export_received_tickets(client, amount):
    amount_integer = int(amount)
    tickets = []
    if amount_integer == 0:
        print("There are no tickets with that/those arguments for Export")
    else:
        for x in range(amount_integer):  # va amount integer
            tickets.append(client.recv(1024).decode())
        print("Added Tickets: ", len(tickets))
        show_ticket_list(tickets)
        process = Process(target=client_export_ticket, args=(tickets,))
        process.start()


# Verify the amount sent by the Server.
def verify_amount_received(amount):
    if amount == str(0):
        return_aux = False
    else:
        return_aux = True
    return return_aux
