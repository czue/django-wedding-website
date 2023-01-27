# A Django Wedding Website and Invitation + Guest Management System

Live site examples:

- [Standard Wedding Website](http://rowena-and.coryzue.com/)
- [Random Save The Date Email](http://rowena-and.coryzue.com/save-the-date/) (refresh for more examples)
- [Sample Personal Invitation Page](http://rowena-and.coryzue.com/invite/b2ad24ec5dbb4694a36ef4ab616264e0/)

There is also [a longer writeup on this project here](https://www.placecard.me/blog/django-wedding-website/).

## What's included?

This includes everything we did for our own wedding:

- A responsive, single-page traditional wedding website
- A complete guest management application
- Email framework for sending save the dates
- Email framework for invitations and built in RSVP system
- Guest dashboard

More details on these below.

### The "Standard" Wedding Website

The standard wedding website is a responsive, single-page, twitter bootstrap-based site (using a modified version of
[this theme](https://blackrockdigital.github.io/startbootstrap-creative/)).

It is completely customizable to your needs and the content is laid out in standard django templates. By default it includes:

- A "hero" splash screen for a photo
- A mobile-friendly top nav with scrollspy
- A photo/hover navigation pane
- Configurable content sections for every aspect of your site that you want
- A set of different styles you can use for different sections

![Hero Section of Wedding Website](https://raw.githubusercontent.com/czue/django-wedding-website/master/screenshots/hero-page.png)

### Guest management

The guest management functionality acts as a central place for you to manage your entire guest list.
It includes two data models - the `Party` and the `Guest`.

#### Party model

The `Party` model allows you to group your guests together for things like sending a single invitation to a couple.
You can also add parties that you're not sure you're going to invite using the `is_invited` field, which works great for sending tiered invitations.
There's also a field to track whether the party is invited to the rehearsal dinner.

#### Guest model

The `Guest` model contains all of your individual guests.
In addition to standard name/email it has fields to represent whether the guest is a child (for kids meals/pricing differences),
and, after sending invitations, marking whether the guest is attending and what meal they are having.

#### Excel import/export

The guest list can be imported and exported via excel (csv).
This allows you to build your guest list in Excel and get it into the system in a single step.
It also lets you export the data to share with others or for whatever else you need.

See the `import_guests` management command for more details and `guests/tests/data` for sample file formats or see the customization section below.

### Save the Dates

The app comes with a built-in cross-client and mobile-friendly email template for save the dates (see `save_the_date.html`).

You can create multiple save the dates and send them out either randomly or by `Party` type (useful if you want to send formal
invitations to some people and more playful ones to others).

See `save_the_date.py` and `SAVE_THE_DATE_CONTEXT_MAP` for customizing your save the dates.

### Invitations and RSVPs

The app also comes with a built-in invitation system.
The template is similar to the save-the-date template, however in addition to the standard invitation content it includes:

- A built in tracking pixel to know whether someone has opened the email or not
- Unique invitation URLs for each party with pre-populated guest names ([example](http://rownena-and.coryzue.com/invite/b2ad24ec5dbb4694a36ef4ab616264e0/))
- Online RSVP system with meal selection and validation

### Guest dashboard

After your invitations go out you can use the guest dashboard to see how many people have RSVP'd, everyone who still
has to respond, people who haven't selected a meal, etc.
It's a great way of tracking your big picture numbers in terms of how many guests to expect.

Just access `/dashboard/` from an account with admin access. Your other guests won't be able to see it.

![Wedding Dashboard](https://raw.githubusercontent.com/czue/django-wedding-website/master/screenshots/wedding-dashboard.png)

### Other details

You can easily hook up Google analytics by editing the tracking ID in `google-analytics.html`.


## Installation

This is developed for Python 3 and Django 4.1.

It's recommended that you setup a virtualenv before development.

Then just install requirements, migrate, and runserver to get started:

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

If you run into Python errors, try to replace `python` with `python3`.

You can now visit your site at `http://localhost:8000/`.

The dashboard and admin interface are available at `http://localhost:8000/dashboard/` and `http://localhost:8000/admin/`. 
Use the superuser created in step three of the commands above.

## Customization

I recommend forking this project and just manually modifying it by hand to replace everything with what you want.
Searching for the text on a page in the repository is a great way to find where something lives.

Some things are already customizable thanks to the use of variables. 
Copy `bigday/localsettings.py.template` to `bigday/localsettings.py` and edit the values.
You definitely need to change the `SECRET_KEY` to a new secure value.

`localsettings.py` is excluded from Git, so you won't accidentally submit your personal data to a public repository.

### Sending email

This application uses Django's email framework for sending mail. 
In order to hook it into a real server, you need to switch the variable `MAIL_BACKEND` of the `bigday/settings.py` from `console` to `smtp`.
You have to enter your email configuration in the `bigday/localsettings.py` (see `Customization`).

This [thread on stack overflow](https://stackoverflow.com/questions/6367014/how-to-send-email-via-django) has a working example for a Gmail configuration.

Save the dates and invitations can be send with the following commands:
```bash
python manage.py send_save_the_dates --send --mark-sent
python send_invitations --send --mark-sent
```

If you want to know more about the command line options, please use the `-h` option:
```bash
python manage.py send_save_the_dates -h
python send_invitations -h
```

### Email addresses

To customize the email addresses, see the `DEFAULT_WEDDING_FROM_EMAIL` and
`DEFAULT_WEDDING_REPLY_EMAIL` variables in `bigday/localsettings.py` (See `Customization`).
You are also able to CC someone on all your outgoing emails using `WEDDING_CC_LIST`

### Import guests

To actually be able to send emails, you need to import your guests first.
The import method expects a CSV file with the following header:

`party_name,first_name,last_name,party_type,is_child,category,is_invited,email`

A sample line could be:

`Party Name,Phred,McPhredson,formal,n,Groom,y,email@domain.tld`

The import command is:

```bash
python manage.py import_guests guestList.csv
```

If you want to add more guests to the list, simply create a new CSV and rerun the command.

### Other customizations

If you want to use this project for your wedding but need help getting started just [get in touch](http://www.coryzue.com/contact/) or make an issue
for anything you encounter and I'm happy to help.

I haven't built out more complete customization docs yet because I wasn't sure anyone would be interested in this,
but will add to these instructions whenever I get questions!

-Cory
