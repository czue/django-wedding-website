
INVITATION_TEMPLATE = 'guests/email_templates/invitation.html'


def get_invitation_context():
    return {
        'title': "Lion's Head",
        'header_filename': 'hearts.png',
        'main_image': 'envelope.png',
        'main_color': '#fff3e8',
        'font_color': '#666666',
        'page_title': "Cory and Rowena - You're Invited!",
        'preheader_text': "Lucky you! You made the cut!",  # todo: make better
    }
