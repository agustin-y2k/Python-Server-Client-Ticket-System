from client_functions import *
from server_functions import verify_ticketId

client = create_socket_client()
client_server_connection(client)

while True:

    print("""
    *** Menu ***
    * -i/--insert: insert a ticket
    * -l/--list: list tickets
    * -f/--filter: filter tickets
    * -e/--edit: edit a ticket
    * -x/--export: export tickets 
    * -q/--quit: disconnect client
    """)
    option = input("Option: ")
    
    opts, args = getopt.getopt(option, "p:h:ilfexq", ['insert', 'list', 'filter', 'edit', 'export', 'quit'])
    client.send(option.encode())
    
    if option in ['-i', '--insert']:
        ticket = client_create_ticket()
        ticket_obj = json.dumps(ticket)
        client.send(ticket_obj.encode())

    elif option in ['-l', '--list']:
        tickets_amount = client.recv(1024).decode()
        print("The number of tickets is: ", tickets_amount)
        amount = input("Enter the Number of Tickets you want to get: ")
        try:
            while int(amount) > int(tickets_amount):
                amount = str(input("You have entered an amount greater than the available amount, try again "))
        except ValueError:
            amount = str(input("invalid syntax, try again: "))
        client.send(amount.encode())
        get_tickets(client, amount)

    elif option in ['-f', '--filter']:
        client_ticket_filter(client)
        tickets_amount = client.recv(1024).decode()
        print("amount received: ", tickets_amount)
        verify = verify_amount_received(tickets_amount)
        if not verify:
            print("There are no tickets with those arguments")
            continue
        amount = input("Enter the Number of Tickets you want to get: ")
        while int(amount) > int(tickets_amount):
            amount = str(input("You have entered an amount greater than the available amount, try again"))
        client.send(amount.encode())
        get_tickets(client, amount)

    elif option in ['-e', '--edit']:
        ticket_ID = input("Ingress Ticket Idt: ")
        verify = verify_ticketId(ticket_ID)
        client.send(ticket_ID.encode())
        if not verify:
            print("There are no tickets with those arguments")
            continue
        ticket = client.recv(1024).decode()
        ticket_edited = edit_ticket(ticket)
        ticket_edited_json = json.dumps(ticket_edited)
        client.send(ticket_edited_json.encode())

    elif option in ['-x', '--export']:
        client_ticket_filter(client)
        tickets_amount = client.recv(1024).decode()
        print("amount received: ", tickets_amount)
        verify = verify_amount_received(tickets_amount)
        if not verify:
            print("There are no tickets with those arguments")
            continue
        amount = input("Enter the amount of Tickets you want to export: ")
        while int(amount) > int(tickets_amount):
            amount = str(input("You have entered an amount greater than the available amount, try again"))
        client.send(amount.encode())
        export_received_tickets(client, amount)

    elif option in ['-q', '--exit']:
        break

    else:
        print('\nInvalid option!\n')
        input('Press Enter')

client.close()
