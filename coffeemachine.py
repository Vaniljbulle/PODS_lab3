from time import sleep
import fakeTCP
import socket

MAX_COFFEE = 5

supplier_server_address = None
coffee_server_address = None


class CoffeeMachine:
    def __init__(self, supplyAddress, coffeeAddress):
        self.coffee = MAX_COFFEE
        self.coffee_queue = []
        self.supply_queue = []
        self.paused = False
        self.supply_requested = False
        self.supplier_server_address = supplyAddress
        self.coffee_server_address = coffeeAddress

    def __str__(self):
        return "Coffee left: {}".format(self.coffee)

    def fill(self):
        print("Refilling", end="", flush=True)
        for i in range(0, 30):
            print(".", end="", flush=True)
            sleep(0.5)
        self.coffee = MAX_COFFEE
        print(" Done!")

    def buy(self, coffee):
        self.coffee -= coffee
        print("Pouring", end="", flush=True)
        # Simulate coffee being poured animation in console
        for i in range(0, 10):
            print(".", end="", flush=True)
            sleep(0.5)
        print(" Done!")

    def inventory(self):
        return self.coffee

    def processOrder(self):
        if self.paused or (len(self.coffee_queue) <= 0):
            return

        # Create a socket
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as coffee_socket:
            # Get first order in queue
            client_address = self.coffee_queue[0]
            print("\nProcessing order from {}, ".format(client_address), end="")
            # Establish connection with client
            if fakeTCP.sendAndReceive(coffee_socket, b"CONNECT", client_address, 5, 3, b"CONNECTED"):
                # Ask for payment once connected
                if fakeTCP.sendAndReceive(coffee_socket, b"PAY", client_address, 5, 3, b"PAYMENT"):
                    # Confirm payment arrived, give receipt
                    if fakeTCP.sendAndReceive(coffee_socket, b"RECEIPT", client_address, 5, 3, b"ARRIVED"):
                        # Confirm receipt arrived, give coffee
                        self.buy(1)
                        if fakeTCP.sendAndReceive(coffee_socket, b"COFFEE", client_address, 5, 3, b"THANKS"):
                            print("Coffee delivered")
                        else:
                            print("Customer did not get his coffee")
                    else:
                        print("Customer left without coffee")
                else:
                    print("Payment rejected")
            else:
                print("Connection rejected")
            self.coffee_queue.pop(0)  # Remove client from queue

    def requestSupply(self):
        if (self.inventory() == 0) and (self.supply_requested is False):
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as supply_socket:
                print(
                    f"\nOut of coffee - supplier notified at {self.supplier_server_address}"
                    f"\nCoffee left: {self.inventory()}"
                    f"\nCustomers in queue: {len(self.coffee_queue)}")

                if fakeTCP.sendAndReceive(supply_socket, b"REFILL", supplier_server_address, 5, 3, b"ACCEPTED"):
                    self.supply_requested = True

    def processSupply(self):
        self.requestSupply()
        if len(self.supply_queue) > 0:
            # Create a socket
            with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as supply_socket:
                # Get first order in queue
                supply_address = self.supply_queue[0]
                print("\nProcessing supply from {}, ".format(supply_address), end="")
                self.fill()
                if fakeTCP.sendAndReceive(supply_socket, b"REFILLED", supply_address, 5, 3, b"CONFIRMED"):
                    print("Supplier notified")
                print("Coffee machine refilled")
                self.supply_requested = False
                self.supply_queue.pop(0)

                """"# Establish connection with client
                if fakeTCP.sendAndReceive(supply_socket, b"CONNECT", supply_address, 5, 3, b"CONNECTED"):
                    # Ask for payment once connected
                    if fakeTCP.sendAndReceive(supply_socket, b"REFILL", supply_address, 5, 3, b"REFILLED"):
                        print("Refill confirmed")
                        self.supply_requested = False
                        self.supply_queue.pop(0)"""

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def refilling(self, client_address):
        self.pause()
        self.fill()
        self.resume()
        print("Coffee machine is resuming")
        self.coffee_queue.append(client_address)
