from django.db import models
from django.contrib.auth.models import User

# profile model for each user
class Profile(models.Model):

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    favourites = models.ManyToManyField(
        "fundraising.Project", related_name="favourites"
    )

    def __str__(self):
        return self.user.username
