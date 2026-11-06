class Cart:
    MAX_CAPACITY = 20

    def __init__(self):
        self.items = []

    def add_dvd(self, dvd):
        if len(self.items) >= self.MAX_CAPACITY:
            print("The cart is full.")
            return
        self.items.append(dvd)

    def remove_dvd(self, dvd):
        if dvd in self.items:
            self.items.remove(dvd)

    def total_cost(self):
        return sum(dvd.cost for dvd in self.items)
