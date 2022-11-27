class CoffeeMachine:
    def __init__(self):
        self.coffee = 5
        self.coffeeQueue = []

    def __str__(self):
        return "Coffee left: {}".format(self.coffee)

    def fill(self, coffee):
        self.coffee += coffee

    def buy(self, coffee):
        self.coffee -= coffee

    def inventory(self):
        return self.coffee
