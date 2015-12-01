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


class TaskManager(models.Manager):
    def add_task(self, author, calendar, name, date_start, date_end, **kwargs):
        if not author:
            raise ValueError("Author must be set")

        if not calendar:
            raise ValueError("Calendar must be set")

        if not name:
            raise ValueError("Name must be set")

        if not date_start:
            raise ValueError("Start date must be set")

        if not date_end:
            raise ValueError("End date must be set")

        task = self.model(author=author,
                          calendar=calendar,
                          name=name,
                          date_start=date_start,
                          date_end=date_end,
                          **kwargs)

        task.save()
        return task
