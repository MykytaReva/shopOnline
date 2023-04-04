from django.shortcuts import redirect
from django.contrib import messages

from .forms import DailyLetterForm
from .models import DailyLetter


def daily_newsletter_form(request):
    # if get method - render the form
    d_form = DailyLetterForm()
    context = {
        'd_form': d_form,
    }
    # if post method - save obj
    if request.method == 'POST':
        d_form = DailyLetterForm(request.POST)
        if d_form.is_valid():
            # get credentials for user
            email = d_form.cleaned_data['email']
            DailyLetter.objects.create(email=email)
            messages.success(
                request,
                'You successfully signed up for our newsletter!'
            )
            return redirect('marketplace:home_view')
        else:
            messages.error(request, d_form.errors)
            d_form = DailyLetterForm()
            return redirect('marketplace:home_view')
    return context
