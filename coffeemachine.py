from time import sleep

MAX_COFFEE = 5


class CoffeeMachine:
    def __init__(self):
        self.coffee = MAX_COFFEE
        self.coffeeQueue = []
        self.supplyQueue = []
        self.paused = False
        self.supplyRequested = False

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
        if self.paused:
            return
        if len(self.coffeeQueue) > 0:
            return self.coffeeQueue[0]

    def orderPop(self):
        if self.paused:
            return
        return self.coffeeQueue.pop(0)

    def processSupply(self):
        if len(self.supplyQueue) > 0:
            return self.supplyQueue.pop(0)

    def pause(self):
        self.paused = True

    def resume(self):
        self.paused = False

    def refilling(self, client_address):
        self.pause()
        self.fill()
        self.resume()
        print("Coffee machine is resuming")
        self.coffeeQueue.append(client_address)
