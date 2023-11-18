from django.conf import settings
from django.http import JsonResponse

from .forms import DailyLetterForm
from .models import DailyLetter


def daily_newsletter_form(request):
    # check if request is ajax
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        d_form = DailyLetterForm(request.POST)
        # check form
        if d_form.is_valid():
            email = d_form.cleaned_data["email"]
            DailyLetter.objects.create(email=email)
            return JsonResponse(
                {
                    "message": "You successfully signed up for our newsletter!",
                    "icon": "success",
                }
            )
        # unique error
        else:
            return JsonResponse(
                {
                    "message": "This email address already signed up for the newsletter.",
                    "icon": "error",
                }
            )
    # standard context_processor
    else:
        d_form = DailyLetterForm()
        context = {
            "d_form": d_form,
        }
        return context


def get_google_api(request):
    return {"GOOGLE_API_KEY": settings.GOOGLE_API_KEY}
