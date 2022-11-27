from time import sleep


class CoffeeMachine:
    def __init__(self):
        self.coffee = 5
        self.coffeeQueue = []

    def __str__(self):
        return "Coffee left: {}".format(self.coffee)

    def fill(self, coffee):
        self.coffee += coffee

    def buy(self, coffee):
        print("Coffee machine is pouring coffee")
        # Simulate coffee being poured animation in console
        for i in range(0, 10):
            print(".", end="", flush=True)
            sleep(0.5)
        self.coffee -= coffee
        print(" Done!")

    def inventory(self):
        return self.coffee

    def processOrder(self):
        if len(self.coffeeQueue) > 0:
            return self.coffeeQueue.pop(0)
