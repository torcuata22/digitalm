from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse #added this as suggestion to avoid error, need to check
from  .models import Product, OrderDetail
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
import stripe, json

# Create your views here.
def index(request):
    products=Product.objects.all()
    return render (request, 'myapp/index.html', {"products":products})

def detail(request, id):
    product = Product.objects.get(id=id)
    stripe_publishable_key = settings.STRIPE_PUBLISHABLE_KEY
    return render (request, 'myapp/detail.html', {'product':product, 'stripe_publishable_key':stripe_publishable_key})


@csrf_exempt #allows crossite request with Stripe
def create_checkout_session(request, id):
     request_data = json.load(request.body)
     product = Product.objects.get(id=id)
     stripe.api_key = settings.STRIPE_SECRET_KEY
     checkout_session = stripe.checkout.Session().create( #everything here is defined by Stripe
        customer_email = request_data['email'],
        payment_method_types=['card'],
        line_items=[
         {
         'price_data':{
         'currency': 'usd',
         'product_data':{
         'name':product.name
         },
         'unit_amount':int(product.price * 100) #what stripe is going to charge, given as decimal, so I need to *100
         },
         'quantity':1,
         }
        ],
        mode='payment',
        success_url = request.build_absolute_uri(reverse('success')) + 
        "?session_id={CHECKOUT_SESSION_ID}",
        cancel_url = request.build_absolute_uri(reverse('failed')),
     )
     #after checkout session is completed:
     order = OrderDetail()
     order.customer_email = request_data['email'] #get field contents from the request data
     order.product = product #instantiated from Product class
     order.stripe_payment_intent = checkout_session['payment_intent']#we get this from the checkout session we created above
     order.amount = int(product.price)
     order.save()
     #this will not render any kind of page, it will instead return a JSON response
     #to get the session_id, we make it return a JSON response:
     return JsonResponse({'sessionId':checkout_session.id})

def payment_success_view(request):
    session_id = request.GET.get('session_id') #if it exists, then it is valid session. If not, session doesn't exist