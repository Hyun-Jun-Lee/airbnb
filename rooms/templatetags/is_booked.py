import datetime
from django import template
from reservations import models as reservation_models

register = template.Library()

# Can send 'is_booked' to templates


@register.simple_tag
def is_booked(room, day):
    if day.number == 0:
        return
    try:
        # reservations/models/BookedDay class는 datetime field이기 때문에 이런 형식 필요
        date = datetime.datetime(year=day.year, month=day.month, day=day.number)
        # BookedDay에 day, room과 같은 조건이 있는지 체크
        # 'reservation__room=room' : rsservation/models/Reservation class의 room field에 전달받은 room으로 지정
        reservation_models.BookedDay.objects.get(day=date, reservation__room=room)
        return True
    except reservation_models.BookedDay.DoesNotExist:
        return False
