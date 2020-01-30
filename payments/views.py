from django.conf import settings  # new
from django.views.generic.base import TemplateView
import stripe
from django.http import HttpResponse
from django.shortcuts import render

stripe.api_key = settings.STRIPE_SECRET_KEY  # new


class HomePageView(TemplateView):
    template_name = 'home.html'

    def get_context_data(self, **kwargs):  # new
        context = super().get_context_data(**kwargs)
        context['key'] = settings.STRIPE_PUBLISHABLE_KEY
        return context


def charge(request):  # new
    # if request.method == 'POST':
    #     charge = stripe.Charge.create(
    #         amount=500,
    #         currency='usd',
    #         description='A Django charge',
    #         source=request.POST['stripeToken']
    #     )
    try:
        charge = stripe.Charge.create(
            amount=500,
            currency="inr",
            description='A Django charge',
            source="tok_mastercard",
            metadata={'order_id': '6735'},
            idempotency_key='sSLwex2yaSVbiPyx'


        )

    except stripe.error.CardError as e:
        # Problem with the card
        return HttpResponse(e)

    except stripe.error.RateLimitError as e:
        # Too many requests made to the API too quickly
        return HttpResponse(e)
    except stripe.error.InvalidRequestError as e:
        # Invalid parameters were supplied to Stripe API
        return HttpResponse(e)

    except stripe.error.AuthenticationError as e:
        # Authentication Error: Authentication with Stripe API failed (maybe you changed API keys recently)
        return HttpResponse(e)

    except stripe.error.APIConnectionError as e:
        # Network communication with Stripe failed
        return HttpResponse(e)

    except stripe.error.StripeError as e:
        # Stripe Error
        return HttpResponse(e)

    else:
        return render(request, 'charge.html')
