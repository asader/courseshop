from django.contrib.humanize.templatetags.humanize import intcomma

def make_display_price(price):
    rubles = round(price)
    return "%s руб." % (intcomma(int(rubles)))