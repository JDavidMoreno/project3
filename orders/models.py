from django.db import models

# Create your models here.
class Pizzas(models.Model):
    pizza = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.pizza}"

class Toppings(models.Model):
    topping = models.CharField(max_length=30)

    def __str__(self):
        return f"{self.topping}"

class RegPizzaPrices(models.Model):
    pizza = models.ForeignKey(Pizzas, on_delete=models.CASCADE, related_name="regular_price")
    small = models.DecimalField(max_digits=5, decimal_places=2)
    large = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Regular {self.pizza} pizza - Small:{self.small} Large:{self.large}"

class SiciPizzaPrices(models.Model):
    pizza = models.ForeignKey(Pizzas, on_delete=models.CASCADE, related_name="sicilian_price")
    small = models.DecimalField(max_digits=5, decimal_places=2)
    large = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Sicilian {self.pizza} pizza - Small:{self.small} Large:{self.large}"

class Subs(models.Model):
    sub = models.CharField(max_length=30)
    small = models.DecimalField(max_digits=5, decimal_places=2)
    large = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"Sub {self.sub} - Small:{self.small} Large:{self.large}"

class Additions(models.Model):
    addition = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.addition}"

class Pastas(models.Model):
    pasta = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.pasta} - Price:{self.price}"

class Salads(models.Model):
    salad = models.CharField(max_length=30)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.salad} - Price:{self.price}"

class DinnerPlatters(models.Model):
    dinner = models.CharField(max_length=40)
    small = models.DecimalField(max_digits=5, decimal_places=2)
    large = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f"{self.dinner} - Small:{self.small} Large:{self.large}"

class Orders(models.Model):
    dish = models.CharField(max_length=40)
    pizza_type = models.CharField(max_length=40, null=True)
    size = models.CharField(max_length=15, null=True)
    pizza_toppings = models.ManyToManyField(Toppings, related_name="orders")
    sub_additions = models.ManyToManyField(Additions, related_name="orders")
    price = models.DecimalField(max_digits=8, decimal_places=2)
    username = models.CharField(max_length=30)
    time = models.DateTimeField(auto_now=True)
    order_status = models.CharField(max_length=10)

    def __str__(self):
        return f"Order number: {self.id} Dish: {self.dish} Type Pizza: {self.pizza_type} Size Pizza: {self.size} Toppings: {self.pizza_toppings}\
        Sub Additions: {self.sub_additions} Price: {self.price} Order To: {self.username} Order At: {self.time} Order Status: {self.order_status}"
