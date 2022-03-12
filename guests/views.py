import base64
from collections import namedtuple
import random
from datetime import datetime
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.urls import reverse
from django.db.models import Count, Q
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView
from guests import csv_import
from guests.invitation import get_invitation_context, INVITATION_TEMPLATE, guess_party_by_invite_id_or_404, \
    send_invitation_email
from guests.models import Guest, MEALS, Party, RsvpForm, UpdateInfoForm
from guests.save_the_date import get_save_the_date_context, send_save_the_date_email, SAVE_THE_DATE_TEMPLATE, \
    SAVE_THE_DATE_CONTEXT_MAP


class GuestListView(ListView):
    model = Guest

@login_required
def export_guests(request):
    export = csv_import.export_guests()
    response = HttpResponse(export.getvalue(), content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=all-guests.csv'
    return response


@login_required
def dashboard(request):
    parties_with_pending_invites = Party.objects.filter(
        is_invited=True, is_attending=None
    ).order_by('name')
    parties_with_unopen_invites = parties_with_pending_invites.filter(invitation_opened=None)
    parties_with_open_unresponded_invites = parties_with_pending_invites.exclude(invitation_opened=None)
    attending_guests = Guest.objects.filter(is_attending=True)
    guests_without_meals = attending_guests.filter(
        is_child=False
    ).filter(
        Q(meal__isnull=True) | Q(meal='')
    ).order_by(
        'first_name'
    )
    meal_breakdown = attending_guests.exclude(meal=None).values('meal').annotate(count=Count('*'))
    return render(request, 'guests/dashboard.html', context={
        'couple_name': settings.BRIDE_AND_GROOM,
        'guests': Guest.objects.filter(is_attending=True).count(),
        'possible_guests': Guest.objects.filter(party__is_invited=True).exclude(is_attending=False).count(),
        'not_coming_guests': Guest.objects.filter(is_attending=False).count(),
        'pending_invites': parties_with_pending_invites.count(),
        'pending_guests': Guest.objects.filter(party__is_invited=True, is_attending=None).count(),
        'guests_without_meals': guests_without_meals,
        'parties_with_unopen_invites': parties_with_unopen_invites,
        'parties_with_open_unresponded_invites': parties_with_open_unresponded_invites,
        'unopened_invite_count': parties_with_unopen_invites.count(),
        'total_invites': Party.objects.filter(is_invited=True).count(),
        'meal_breakdown': meal_breakdown,
    })


def invitation(request, invite_id):
    party = guess_party_by_invite_id_or_404(invite_id)
    if party.invitation_opened is None:
        # update if this is the first time the invitation was opened
        party.invitation_opened = datetime.utcnow()
        party.save()
    if request.method == 'POST':
        for response in _parse_invite_params(request.POST):
            guest = Guest.objects.get(pk=response.guest_pk)
            assert guest.party == party
            guest.is_attending = response.is_attending
            guest.meal = response.meal
            guest.save()
        if request.POST.get('comments'):
            comments = request.POST.get('comments')
            party.comments = comments if not party.comments else '{}; {}'.format(party.comments, comments)
        party.is_attending = party.any_guests_attending
        party.save()
        return HttpResponseRedirect(reverse('rsvp-confirm', args=[invite_id]))
    return render(request, template_name='guests/invitation.html', context={
        'party': party,
        'meals': MEALS,
    })


InviteResponse = namedtuple('InviteResponse', ['guest_pk', 'is_attending', 'meal'])


def _parse_invite_params(params):
    responses = {}
    for param, value in params.items():
        if param.startswith('attending'):
            pk = int(param.split('-')[-1])
            response = responses.get(pk, {})
            response['attending'] = True if value == 'yes' else False
            responses[pk] = response
        elif param.startswith('meal'):
            pk = int(param.split('-')[-1])
            response = responses.get(pk, {})
            response['meal'] = value
            responses[pk] = response

    for pk, response in responses.items():
        yield InviteResponse(pk, response['attending'], response.get('meal', None))


def rsvp_confirm(request, invite_id=None):
    party = guess_party_by_invite_id_or_404(invite_id)
    return render(request, template_name='guests/rsvp_confirmation.html', context={
        'party': party,
        'support_email': settings.DEFAULT_WEDDING_REPLY_EMAIL,
    })

def update_information(request, invite_id):


    if request.method == 'POST':
        return render(request, template_name='guests/update_information.html', context=context)
    else:
        l_party = Party.objects.get(invitation_id = invite_id)
        guest_num_in_party = Guest.objects.filter(party = l_party).count()
        guests = Guest.objects.filter(party = l_party)
        for num in range(0,guest_num_in_party):
            form = UpdateInfoForm(instance=guests[num])
            
        print(form)
        #form = [UpdateInfoForm(prefix=str(x), instance=Guest()) for x in range(0,(guest_num_in_party))]
        return render(request, template_name='guests/update_information.html', context={'form':form})


def rsvp_login(request):
    form = RsvpForm
    context = {
        'form': form,
        'support_email': settings.DEFAULT_WEDDING_REPLY_EMAIL,
    }
    if(request.GET.get('rsvp_code')):
        print(request.GET.get('rsvp_code'))
        l_InvitationID = rsvp_match(request)
        if(l_InvitationID != 0):
            return redirect("https://wedding.jacobrener.com/invite/" + l_InvitationID)  
        else:
            messages.error(request, "Incorrect RSVP code. Please try again. If problems persist, please contact Jacob and Kim at kimle.jacobrener@gmail.com")
            return render(request, template_name='guests/rsvp.html', context=context) 
    else:
        return render(request, template_name='guests/rsvp.html', context=context)

def rsvp_match(request):
    Party.objects
    l_rsvpcode = request.GET.get('rsvp_code')
    l_rsvpcode = l_rsvpcode.lower()
    try:
        l_party = Party.objects.get(rsvp_code = l_rsvpcode)
        return l_party.invitation_id
    except Party.DoesNotExist:
        return 0

@login_required
def invitation_email_preview(request, invite_id):
    party = guess_party_by_invite_id_or_404(invite_id)
    context = get_invitation_context(party)
    return render(request, INVITATION_TEMPLATE, context=context)


@login_required
def invitation_email_test(request, invite_id):
    party = guess_party_by_invite_id_or_404(invite_id)
    send_invitation_email(party, recipients=[settings.DEFAULT_WEDDING_TEST_EMAIL])
    return HttpResponse('sent!')


def save_the_date_random(request):
    #template_id = random.choice(SAVE_THE_DATE_CONTEXT_MAP.keys())
    template_id = 'kimandjacob'
    return save_the_date_preview(request, template_id)


def save_the_date_preview(request, template_id):
    context = get_save_the_date_context(template_id)
    context['email_mode'] = False
    return render(request, SAVE_THE_DATE_TEMPLATE, context=context)


@login_required
def test_email(request, template_id):
    context = get_save_the_date_context(template_id)
    send_save_the_date_email(context, [settings.DEFAULT_WEDDING_TEST_EMAIL])
    return HttpResponse('sent!')


def _base64_encode(filepath):
    with open(filepath, "rb") as image_file:
        return base64.b64encode(image_file.read())
