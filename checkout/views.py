from django.shortcuts import render
from django.conf import settings
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.http.response import JsonResponse, HttpResponse
from django.contrib.auth.models import User

from profiles.models import Profile
import stripe


# Create your views here.

@login_required(login_url='home:login')
def checkout(request):
    """view to return the stripe checkout page"""
    return render(request, 'full-version/full-version.html')

# https://testdriven.io/blog/django-stripe-tutorial/


def success_view(request):
    return render(request, 'success/success.html')


def cancelled_view(request):
    return render(request, 'cancelled/cancelled.html')


@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config_data = {'publicKey': settings.STRIPE_PUBLIC_KEY}
        return JsonResponse(stripe_config_data, safe=False)


@csrf_exempt
def create_checkout_session(request):
    if request.method == 'GET':
        print(request.user.id)
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
                success_url=domain_url + 'checkout/success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'checkout/cancelled/',
                payment_method_types=['card'],
                metadata={"user_id": request.user.id},
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


@csrf_exempt
def stripe_webhook(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    endpoint_secret = settings.STRIPE_WH_SECRET
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event = None

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, endpoint_secret
        )
    except ValueError as e:
        # Invalid payload
        return HttpResponse(status=400)
    except stripe.error.SignatureVerificationError as e:
        # Invalid signature
        return HttpResponse(status=400)

    # Handle the checkout.session.completed event
    if event['type'] == 'checkout.session.completed':
        # this user has payed saving that in his profile
        intent = event.data.object
        user_id = intent.metadata.user_id
        current_user = User.objects.get(pk=user_id)
        current_user.profile.payed_full_version = True
        current_user.save()

    return HttpResponse(status=200)
