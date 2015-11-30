from django.db import models


class CalendarManager(models.Manager):
    def add_calendar(self, author, name, **kwargs):
        if not author:
            raise ValueError("Author must be set")

        if not name:
            raise ValueError("Name must be set")

        calendar = self.model(author=author,
                              name=name,
                              **kwargs)

        calendar.save()
        calendar.members.add(author)

        return calendar
