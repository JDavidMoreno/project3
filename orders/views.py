from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


from orders.models import RegPizzaPrices, SiciPizzaPrices, Toppings, Subs, Pastas, Salads, DinnerPlatters, Orders


# Create your views here.
def index(request):
    return render(request, "orders/index.html")


def register(request):

    if request.method == "POST":

        password = request.POST["password"]
        username = request.POST["username"]
        email = request.POST["email"]
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]


        user = User.objects.create_user(username, email, password, first_name=first_name, last_name=last_name)
        user.save()
        return render(request, "orders/index.html")
    else:
        return render(request, "orders/register.html")


def login_page(request):

    if request.method == 'POST':
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return render(request, "orders/index.html")
    else:
        return render(request, "orders/login.html")

def logout_page(request):
    logout(request)
    return HttpResponseRedirect(reverse('index'))


def pizzas(request):
    regular_pizzas = RegPizzaPrices.objects.all()
    sicilian_pizzas = SiciPizzaPrices.objects.all()
    toppings = Toppings.objects.all()


    context = {
        "regular_pizzas": regular_pizzas,
        "sicilian_pizzas": sicilian_pizzas,
        "toppings": toppings,

    }

    return render(request, "orders/pizzas.html", context)


def subs(request):
    subs = Subs.objects.all()
    context = {
        "subs":subs
    }

    return render(request, "orders/subs.html", context)


def pasta(request):
    pasta = Pastas.objects.all()
    return render(request, "orders/pasta.html", {"pasta": pasta})


def salads(request):
    salads = Salads.objects.all()
    return render(request, "orders/salads.html", {"salads": salads})


def platters(request):
    platters = DinnerPlatters.objects.all()

    context = {
    "platters": platters
    }
    return render(request, "orders/platters.html", context)
def added(request):

    dish = request.POST["dish"]
    type = request.POST["type"]
    size = request.POST["size"]
    price = request.POST["price"]

    try:
        topping1 = request.POST["toppings0"]
        print(topping1)
    except KeyError:
        topping1 = None
    try:
        topping2 = request.POST["toppings1"]
        print(topping2)
    except KeyError:
        topping2 = None
    try:
        topping3 = request.POST["toppings2"]
        print(topping3)
    except KeyError:
        topping3 = None
    try:
        topping4 = request.POST["toppings3"]
        print(topping4)
    except KeyError:
        topping4 = None
    try:
        topping5 = request.POST["toppings4"]
        print(topping5)
    except KeyError:
        topping5 = None


    if topping1: topping_to_add1 = Toppings.objects.get(id=topping1)
    if topping2: topping_to_add2 = Toppings.objects.get(id=topping2)
    if topping3: topping_to_add3 = Toppings.objects.get(id=topping3)
    if topping4: topping_to_add4 = Toppings.objects.get(id=topping4)
    if topping5: topping_to_add5 = Toppings.objects.get(id=topping5)



    order = Orders(dish=dish, pizza_type=type, size=size, price=price, username=request.user.username, order_status="draft")

    order.save()

    if topping1: order.pizza_toppings.add(topping_to_add1)
    if topping2: order.pizza_toppings.add(topping_to_add2)
    if topping3: order.pizza_toppings.add(topping_to_add3)
    if topping4: order.pizza_toppings.add(topping_to_add4)
    if topping5: order.pizza_toppings.add(topping_to_add5)

    order.save()

    return JsonResponse({"success": True})

def cart(request):

    orders = Orders.objects.filter(username=request.user.username)

    return render(request, "orders/cart.html", {"orders": orders})

def delete(request):
    id = request.POST["id"]

    order = Orders.objects.get(id=id)

    order.delete()

    return JsonResponse({"success": True})
