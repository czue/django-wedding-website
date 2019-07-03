# A Django Wedding Website and Invitation + Guest Management System

## Upstream
Code taken and rebranded from [Standard Wedding Website](http://coryandro.com/)
There is also [a longer writeup on this project here](https://www.placecard.me/blog/django-wedding-website/).


## Rebranded
Live site examples:
- [Standard Wedding Website](https://fiechegutierrez.com//)
- [Random Save The Date Email](https://fiechegutierrez.com//save-the-date/) (refresh for more examples)
- [Sample Personal Invitation Page](https://fiechegutierrez.com//invite/b2ad24ec5dbb4694a36ef4ab616264e0/)


## What's included?
This includes parts of the original project:
- A responsive, single-page traditional wedding website
- A complete guest management application
- ~~Email framework for sending save the dates~~
- Email framework for invitations and built in RSVP system
- Guest dashboard

Plus:
- Wedding list view and management dashboard.

#### Excel import/export

The guest list can be imported and exported via excel (csv).
This allows you to build your guest list in Excel and get it into the system in a single step.
It also lets you export the data to share with others or for whatever else you need.

See the `import_guests` management command for more details and `bigday/guests/tests/data` for sample file formats.

### Invitations and RSVPs

The app also comes with a built-in invitation system.
The template is similar to the save-the-date template, however in addition to the standard invitation content it includes:

- A built in tracking pixel to know whether someone has opened the email or not
- Unique invitation URLs for each party with pre-populated guest names ([example](https://fiechegutierrez.com//invite/b2ad24ec5dbb4694a36ef4ab616264e0/))
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

It's recommended that you setup a virtualenv before development.

Then just install requirements, migrate, and runserver to get started:

```bash
pip3 install -r requirements.txt
python3 manage.py migrate
python3 manage.py runserver
```

## Customization

I recommend forking this project and just manually modifying it by hand to replace everything with what you want.
Searching for the text on a page in the repository is a great way to find where something lives.

If you want to use this project for your wedding but need help getting started just [get in touch](http://www.coryzue.com/contact/) or make an issue
for anything you encounter and I'm happy to help.

I haven't built out more complete customization docs yet because I wasn't sure anyone would be interested in this,
but am happy to do that if people are!

-Cory

### Photologue compatibility
Django 2.1.9 (3/08/2019) 
BC on 2.2.x when create a new gallery by admin tool

### I18N
Add key/ value in PO files then launch command  'python3 ./manage.py compilemessages' in order to see modifications





