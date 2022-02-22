## Ticket System

**Ticket system developed in Python using sockets**

### Start

1. Start the server using the command:

> python3 server.py -p port_number

2. Start a client that connects to the server (IP_server = localhost):

> python3 client.py -p port_number -h IP_server

### Commands

The commands are presented in ***short command / long command***:
    
    -i/--insert: Insertar un nuevo Ticket.
    -l/--list: Listar los Tickets.
    -f/--filter: Filtrar los Tickets por autor, estado y fecha, como también permite una combinación de paramatros de filtrado
    -e/--edit: Editar un Ticket seleccionado, permite modficar título, estado y descripción.
    -x/--export: Exportar Tickets mediante un filtro a un archivo CSV y un archivo comprimido .zip
    -q/--quit: Salir del programa
