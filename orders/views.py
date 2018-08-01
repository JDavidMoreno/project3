from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout


from orders.models import RegPizzaPrices, SiciPizzaPrices, Toppings, Subs, Pastas, Salads, DinnerPlatters, Orders, Additions, Confirmations


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
        addition1 = request.POST["checkbox0"]
        print(addition1)
    except KeyError:
        addition1 = None

    try:
        addition2 = request.POST["checkbox1"]
        print(addition1)
    except KeyError:
        addition2 = None

    try:
        addition3 = request.POST["checkbox2"]
        print(addition1)
    except KeyError:
        addition3 = None

    try:
        addition4 = request.POST["checkbox3"]
        print(addition1)
    except KeyError:
        addition4 = None



    try:
        extra_cheese = request.POST["extra_cheese"]
        print(extra_cheese)
    except KeyError:
        extra_cheese = None
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
    if extra_cheese: cheese_to_add = Additions.objects.filter(addition='Extra Cheese on any sub')
    if addition1: addition_to_add1 = Additions.objects.filter(addition=addition1)
    if addition2: addition_to_add2 = Additions.objects.filter(addition=addition2)
    if addition3: addition_to_add3 = Additions.objects.filter(addition=addition3)
    if addition4: addition_to_add4 = Additions.objects.filter(addition=addition4)




    order = Orders(dish=dish, pizza_type=type, size=size, price=price, username=request.user.username, order_status="draft")

    order.save()

    if topping1: order.pizza_toppings.add(topping_to_add1)
    if topping2: order.pizza_toppings.add(topping_to_add2)
    if topping3: order.pizza_toppings.add(topping_to_add3)
    if topping4: order.pizza_toppings.add(topping_to_add4)
    if topping5: order.pizza_toppings.add(topping_to_add5)
    if extra_cheese: order.sub_additions.add(cheese_to_add[0])
    if addition1: order.sub_additions.add(addition_to_add1[0])
    if addition2: order.sub_additions.add(addition_to_add2[0])
    if addition3: order.sub_additions.add(addition_to_add3[0])
    if addition4: order.sub_additions.add(addition_to_add4[0])

    order.save()

    request.session["blue_cart"] = True
    print(request.session["blue_cart"])

    return JsonResponse({"success": True})

def cart(request):

    orders = Orders.objects.filter(username=request.user.username)

    return render(request, "orders/cart.html", {"orders": orders})

def delete(request):
    id = request.POST["id"]

    try:
        no_content = request.POST["no_content"]
    except KeyError:
        no_content = None

    order = Orders.objects.get(id=id)

    order.delete()

    if no_content == 'no_content':
        request.session["blue_cart"] = False
        print(request.session["blue_cart"])

    return JsonResponse({"success": True})

def confirmation(request):

    orders = Orders.objects.filter(username=request.user.username)

    for order in orders:
        confirmation = Confirmations(dish=order.dish, pizza_type=order.pizza_type, size=order.size, price=order.price,
        username=order.username, order_status='Confirmed')
        confirmation.save()
        confirmation.pizza_toppings.set(order.pizza_toppings.all())
        confirmation.sub_additions.set(order.sub_additions.all())
        confirmation.save()
        order.delete()

    confirmations = Confirmations.objects.filter(username=request.user.username, order_status='Confirmed')
    return render(request, "orders/confirmation.html" , {"confirmations": confirmations} )
