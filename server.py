import threading
from server_functions import *
import json

server_socket = create_server_socket()
connection_server_client(server_socket)


# Server in charge of interpreting the commands sent by the Client.
def server_client_thread(sock, addr):
    while True:

        command_option = sock.recv(1024)
        ticket_date = date.today()

        print('Client %s:%s' % (addr[0], addr[1]))
        print("Option: " + command_option.decode())
        print("Date: ", ticket_date)
        print("")

        server_history_log(ticket_date=ticket_date, option=command_option.decode(), address=addr)

        if command_option.decode() == '-i' or command_option.decode() == '--insert':
            ticket = sock.recv(1024).decode()
            ticket_dict = json.loads(ticket)
            server_create_ticket(ticket_dict)
            print("Ticket created by the client %s:%s" % addr, "\n")

        elif command_option.decode() == '-l' or command_option.decode() == '--list':
            tickets = server_list_tickets()
            amount_tickets = str(len(tickets))
            sock.send(amount_tickets.encode())
            amount = sock.recv(1024).decode()
            get_tickets_ByAmount(tickets, sock, amount)
            print("Client %s:%s has listed the available Tickets" % addr, "\n")

        elif command_option.decode() == '-f' or command_option.decode() == '--filter':
            filtered_tickets = server_ticket_filter(sock)
            filtered_tickets = filtered_tickets.all()
            len_tickets = len(filtered_tickets)
            sock.send(str(len_tickets).encode())
            amount_verify = verify_amount_tickets(len_tickets)
            if not amount_verify:
                continue
            received_amount = sock.recv(1024).decode()
            get_tickets_ByAmount(filtered_tickets, sock, received_amount)
            print("Client %s:%s has filtered tickets" % addr, "\n")

        elif command_option.decode() == '-e' or command_option.decode() == '--edit':
            ticket_id = sock.recv(1024).decode()
            print("Id received: ", ticket_id)
            verify = verify_ticketId(ticket_id)
            if not verify:
                continue
            ticket = get_ticket_ById(ticket_id)
            obj_ticket = json.dumps(ticket, cls=MyEncoder)
            sock.send(obj_ticket.encode())
            ticket_edited = sock.recv(1024).decode()
            server_edit_ticket(ticket_id, ticket_edited)
            print("Client %s:%s has edited a Ticket" % addr, "\n")

        elif command_option.decode() == '-x' or command_option.decode() == '--export':
            filtered_tickets = server_ticket_filter(sock)
            filtered_tickets = filtered_tickets.all()
            len_tickets = len(filtered_tickets)
            sock.send(str(len_tickets).encode())
            amount_verify = verify_amount_tickets(len_tickets)
            if not amount_verify:
                continue
            received_amount = sock.recv(1024).decode()
            get_tickets_ByAmount(filtered_tickets, sock, received_amount)
            print("Client %s:%s has exported Tickets" % addr, "\n")

        elif command_option.decode() == '-q' or command_option.decode() == '--exit':
            print("Client %s:%s disconnected \n" % addr)
            break
        else:
            print('\nInvalid command_option!\n')


ThreadCount = 0

try:
    while True:
        client_socket, addr = server_socket.accept()
        print("\nConnecting from %s:%d\n" % (addr[0], addr[1]))
        ThreadCount += 1
        print('Thread Number: ' + str(ThreadCount), "\n")
        th = threading.Thread(target=server_client_thread, args=(client_socket, addr,)).start()
except KeyboardInterrupt:
    client_socket.close()
