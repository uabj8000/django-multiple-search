from django.db import models

# Create your models here.
from django.conf import settings
from django.db.models import Q

class ProfileQuerySet(models.QuerySet):
    def search(self, query=None):
        qs = self
        if query is not None:
            or_lookup = (
                        Q(user__username__icontains=query) | 
                        Q(title__icontains=query) | 
                        Q(description__icontains=query)| 
                        Q(slug__icontains=query)
                        )
            qs = qs.filter(or_lookup).distinct()
        return qs


class ProfileManager(models.Manager):
    def get_queryset(self):
        return ProfileQuerySet(self.model, using=self._db)

    def search(self, query=None):
        return self.get_queryset().search(query=query)


class Profile(models.Model):
    user            = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title           = models.CharField(max_length=120)
    description     = models.TextField(null=True, blank=True)
    slug            = models.SlugField(blank=True, unique=True)
    timestamp       = models.DateTimeField(auto_now_add=True)
    
    objects         = ProfileManager()
