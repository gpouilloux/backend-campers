from decimal import Decimal
from datetime import date
from typing import Optional

from django.db import models

from django.db.models import FloatField, DecimalField, QuerySet, BooleanField, DateField

SEARCH_COORDINATES_PADDING = 0.1


class CamperQuerySet(models.QuerySet):
    def within_coordinates(self, latitude: float, longitude: float) -> QuerySet:
        return self.filter(
            latitude__gt=latitude - SEARCH_COORDINATES_PADDING,
            latitude__lt=latitude + SEARCH_COORDINATES_PADDING,
            longitude__gt=longitude - SEARCH_COORDINATES_PADDING,
            longitude__lt=longitude + SEARCH_COORDINATES_PADDING,
        )

    def available_within_dates(
        self, start_date: Optional[date], end_date: Optional[date]
    ) -> QuerySet:
        if start_date or end_date:
            return self.exclude(
                campercalendar__start_date__lte=end_date,
                campercalendar__end_date__gte=start_date,
                campercalendar__is_available=False,
            )
        return self


class Camper(models.Model):
    latitude = FloatField()
    longitude = FloatField()
    price_per_day = DecimalField(max_digits=10, decimal_places=2, null=True)
    weekly_discount = DecimalField(max_digits=5, decimal_places=2, null=True)
    objects = CamperQuerySet.as_manager()

    @staticmethod
    def get_price(
        price_per_day: Decimal,
        weekly_discount: Decimal,
        start_date: Optional[date],
        end_date: Optional[date],
    ) -> Decimal:
        """
        Calculate the price of a camper rental.
        If no dates are provided, the price is the `price_per_day`.
        Weekly discount is applied for rentals of 7 days or more.
        :param price_per_day: the price per day
        :param weekly_discount: a weekly discount
        :param start_date: the rental start date
        :param end_date: the rental end date
        :return: the price of a camper rental
        """
        if start_date and end_date:
            number_days = (end_date - start_date).days + 1
            weekly_discount = (
                weekly_discount
                if weekly_discount and number_days >= 7
                else Decimal(0.0)
            )
            return (price_per_day * number_days) * (1 - weekly_discount)
        return price_per_day


class CamperCalendar(models.Model):
    camper = models.ForeignKey(Camper, on_delete=models.CASCADE)
    is_available = BooleanField(default=False)
    start_date = DateField()
    end_date = DateField()
