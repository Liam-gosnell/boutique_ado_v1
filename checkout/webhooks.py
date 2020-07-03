import json
from django.conf import settings
from django.http import HttpResponse
# from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt

from checkout.webhook_handler import StripeWH_Handler
import stripe


stripe.api_key = settings.STRIPE_SECRET_KEY


@csrf_exempt
def webhook(request):

    payload = request.body
    event = None

    try:
        event = stripe.Event.construct_from(
                    json.loads(payload), stripe.api_key
                )

    except ValueError as e:
        # Invalid payload
        print("Value error:", e)
        return HttpResponse(status=400)

    # Handle the event
    if event.type == 'payment_intent.succeeded':
        print("Success")
        payment_intent = event.data.object # contains a stripe.PaymentIntent
        # Then define and call a method to handle the successful payment intent.
        # handle_payment_intent_succeeded(payment_intent)
    elif event.type == 'payment_method.attached':
        print("4")
        payment_method = event.data.object # contains a stripe.PaymentMethod
        # Then define and call a method to handle the successful attachment of a PaymentMethod.
        # handle_payment_method_attached(payment_method)
        # ... handle other event types
    else:
        # Unexpected event type
        return HttpResponse(status=400)

    print(5)
    return HttpResponse(status=200)















# # @require_POST
# @csrf_exempt
# def webhook(request):
#     """Listen for webhooks from Stripe"""

#     # Setup
#     wh_secret = settings.STRIPE_WH_SECRET
#     stripe.api_key = settings.STRIPE_SECRET_KEY

#     # Get the webhook data and verify its signature
#     payload = request.body
#     sig_header = request.META['HTTP_STRIPE_SIGNATURE']
#     event = None

#     try:
#         event = stripe.Webhook.construct_event(
#             payload, sig_header, wh_secret
#         )

#     except ValueError as e:
#         # Invalid payload
#         return HttpResponse(status=400)

#     except stripe.error.SignatureVerificationError as e:
#         # Invalid signature
#         return HttpResponse(status=400)

#     except Exception as e:
#         return HttpResponse(content=e, status=400)

#     # Set up a webhook handler
#     handler = StripeWH_Handler(request)

#     # Map webhook events to relevant handler functions
#     event_map = {
#         'payment_intent.succeeded': handler.handle_payment_intent_succeeded,
#         'payment_intent.payment_failed': handler.handle_payment_intent_payment_failed,
#     }

#     # Get the webhook type from Stripe
#     event_type = event['type']

#     # If there's a handler for it, get it from the event map
#     # Use the generic one by default
#     event_handler = event_map.get(event_type, handler.handle_event)

#     # Call the event handler with the event
#     response = event_handler(event)
#     return response