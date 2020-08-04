from datetime import datetime, timedelta
from django import template


register = template.Library()

@register.simple_tag
def day_diffrence(today_date, song_date):
    now = datetime.now()
    difference = ''
    try:
    	today_date = datetime.strptime(today_date, '%Y-%m-%d')
    	song_date = datetime.strptime(song_date, '%Y-%m-%d')
    	difference = str(today_date - song_date)
    	if difference[0:7] == '0:00:00':
    		difference = "0 day"
    	else:
    		difference = difference[0:7]
    except Exception as e:
    	pass
    return difference