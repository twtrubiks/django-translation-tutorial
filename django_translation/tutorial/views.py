from django.shortcuts import render
from django.utils.translation import gettext as _
from django.utils.translation import pgettext
from django.utils.translation import ngettext

# Create your views here.
def index(request):
    data = _('Hello')

    m=1
    d= 20
    output = _('Today is %(month)s / %(day)s.') % {'month': m, 'day': d}

    # Translators: contextual-markers
    p_blue_color = pgettext("color", "blue")
    # Translators: contextual-markers
    p_blue_mood = pgettext("mood", "blue")

    # pluralization
    count = 2
    pluralization = ngettext(
    'There is %(count)d %(name)s object available.',
    'There are %(count)d %(name)s objects available.',
    count
    ) % {
        'count': count,
        'name':'test',
    }

    return render(request, 'tutorial/index.html', {
        "data" : data,
        "output" : output,
        "p_blue_color": p_blue_color,
        "p_blue_mood": p_blue_mood,
        "pluralization" : pluralization
    })
