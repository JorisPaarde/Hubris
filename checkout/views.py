from django.shortcuts import render
from django.conf import settings
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.sites.models import Site

from profiles.models import Profile
import stripe


# Create your views here.


def checkout(request):
    """view to return the stripe checkout page"""
    # current_user = request.user
    # print("Check it out")
    # payed_full_version = current_user.profile.payed_full_version
    # user_email = current_user.email
    # bio = current_user.profile.bio
    # print(payed_full_version)
    # print(user_email)
    # print(bio)

    return render(request, 'full-version/full-version.html')


def success_view(request):
    return render(request, 'success/success.html')


def cancelled_view(request):
    return render(request, 'cancelled/cancelled.html')


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config_data = {'publicKey': settings.STRIPE_PUBLIC_KEY}
        print(stripe_config_data)
        return JsonResponse(stripe_config_data, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        current_site = Site.objects.get_current()
        domain_url = current_site.domain
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            # Create new Checkout Session for the order
            # Other optional params include:
            # [billing_address_collection] - to display billing address details on the page
            # [customer] - if you have an existing Stripe Customer ID
            # [payment_intent_data] - capture the payment later
            # [customer_email] - prefill the email input in the form
            # For full details see https://stripe.com/docs/api/checkout/sessions/create

            # ?session_id={CHECKOUT_SESSION_ID} means the redirect will have the session ID set as a query param
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'name': 'Full version Huberis',
                        'quantity': 1,
                        'currency': 'usd',
                        'amount': '299',
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})

