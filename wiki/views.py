from django.shortcuts import render

from profiles.models import Card

from .forms import WikiForm
# Create your views here.


def wiki(request):
    """
    view for returning the wiki page
    processing the filters on the cards given by the user
    """
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = WikiForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data
            search_full_version = form.cleaned_data['search_full_version']
            skill_style = form.cleaned_data['skill_style']
            alowed_phase = form.cleaned_data['alowed_phase']
            cards = Card.objects.all()
            # if searching full version keep all cards in the query
            if search_full_version:
                pass
            # if not filter out the free version cards
            else:
                search_free_version = not search_full_version
                cards = cards.filter(in_freeversion=search_free_version)
            # if all skill styles selected keep all cards in the query
            if skill_style:
                if skill_style[0] == 'AL':
                    pass
                # if not filter out the cards with this skill type
                else:
                    cards = cards.filter(skill_style=skill_style[0])
            # if any phase is selected keep all cards in the query
            if alowed_phase:
                if alowed_phase[0] == 'ANY':
                    pass
                # if not filter out the allowed cards for this phase
                else:
                    cards = cards.filter(allowed_in_phase=alowed_phase[0])

            context = {
                'form': form,
                'search_full_version': search_full_version,
                'skill_style': skill_style,
                'alowed_phase': alowed_phase,
                'cards': cards,
            }

            # redirect to a new URL:
            return render(request, 'wiki/wiki.html', context)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = WikiForm()

    return render(request, 'wiki/wiki.html', {'form': form})
