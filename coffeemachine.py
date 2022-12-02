from time import sleep
import fakeTCP
import socket
import threading
import queue

MAX_COFFEE = 20
REQUEST_COFFEE = 0
speed = 0.1


class Monitor:
    def __init__(self, value):
        self.lock = threading.Lock()
        self.value = value

    def get(self):
        with self.lock:
            r = self.value
        return r

    def set(self, value):
        with self.lock:
            self.value = value

    def increment(self):
        with self.lock:
            self.value += 1

    def decrement(self):
        with self.lock:
            self.value -= 1


class CoffeeMachine:
    def __init__(self, supply_address, coffee_address):
        self.coffee = Monitor(MAX_COFFEE)

        self.coffee_queue = queue.Queue()
        self.supply_queue = queue.Queue()

        self.supply_requested = False
        self.supplier_server_address = supply_address
        self.coffee_server_address = coffee_address

    def refill_coffee(self):
        print("Refilling", end="", flush=True)
        for i in range(0, 30):
            print(".", end="", flush=True)
            sleep(speed)
        self.coffee.set(MAX_COFFEE)
        print(" Done!")

    def pour_coffee(self):
        # Simulate coffee being poured animation in console
        print("Pouring", end="", flush=True)
        for i in range(0, 10):
            print(".", end="", flush=True)
            sleep(speed)
        print(" Done!")

    def put_in_order(self, client_address):
        self.coffee_queue.put(client_address)

    def can_accept_orders(self):
        customers = self.coffee_queue.qsize()
        coffees = self.coffee.get()

        return (coffees - customers) > 0

    def process_order(self):
        if self.coffee_queue.qsize() <= 0:
            return

        # Create a socket
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as coffee_socket:
            # Get first order in queue
            client_address = self.coffee_queue.get()
            self.coffee.decrement()

            print("\nProcessing order from {}, ".format(client_address), end="")
            # Establish "connection" with client
            if fakeTCP.sendAndReceive(coffee_socket, b"CONNECT", client_address, 5, 3, b"CONNECTED") and \
                    fakeTCP.sendAndReceive(coffee_socket, b"PAY", client_address, 5, 3, b"PAYMENT") and \
                    fakeTCP.sendAndReceive(coffee_socket, b"RECEIPT", client_address, 5, 3, b"ARRIVED"):
                self.pour_coffee()
                if fakeTCP.sendAndReceive(coffee_socket, b"COFFEE", client_address, 5, 3, b"THANKS"):
                    print("Coffee delivered")
            else:
                print("Connection rejected - Order cancelled")
                self.coffee.increment()

    def request_supply(self):
        if (self.coffee.get() <= REQUEST_COFFEE) and (self.supply_requested is False):
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as supply_socket:
                print(f"\nOut of coffee - supplier notified at {self.supplier_server_address}")
                if fakeTCP.sendAndReceive(supply_socket, b"REFILL", self.supplier_server_address, 5, 3, b"ACCEPTED"):
                    print("Supplier accepted request")
                    self.supply_requested = True

    def process_supply(self):
        self.request_supply()
        if self.supply_queue.qsize() > 0:
            # Create a socket
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as supply_socket:
                # Get first order in queue
                supply_address = self.supply_queue.get()
                print("\nProcessing supply from {}, ".format(supply_address), end="")
                self.refill_coffee()
                fakeTCP.sendAndReceive(supply_socket, b"REFILLED", supply_address, 5, 3, None)
                print("Coffee machine refilled")
                self.supply_requested = False
