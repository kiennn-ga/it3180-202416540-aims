class Cart:
    MAX_CAPACITY = 20

    def __init__(self):
        self.items = []

    def add_dvd(self, dvd):
        if len(self.items) >= self.MAX_CAPACITY:
            print("The cart is full.")
            return False
        self.items.append(dvd)
        print("Đã thêm đĩa vào giỏ hàng")
        return True

    def remove_dvd(self, dvd):
        if dvd in self.items:
            self.items.remove(dvd)

    def total_cost(self):
        return sum(dvd.cost for dvd in self.items)

    def print_cart(self):
        if not self.items:
            print("The cart is empty")
            return
        print("*********************** CART ***********************")
        for index, dvd in enumerate(self.items, start=1):
            print(
                f"{index}. DVD - {dvd.title} - {dvd.category} - "
                f"{dvd.director} - {dvd.length}: {dvd.cost:.2f} $"
            )
        print(f"Total cost: {self.total_cost():.2f} $")
        print("****************************************************")

    def total_cost_with_discount(self, percent):
        if not 0 <= percent <= 100:
            raise ValueError("Discount percent must be between 0 and 100.")
        return self.total_cost() * (1 - percent / 100)
