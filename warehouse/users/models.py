from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    """
    Default custom user model for warehouse.
    If adding fields that need to be filled at user signup,
    check forms.SignupForm and forms.SocialSignupForms accordingly.
    """

    # First and last name do not cover name patterns around the globe
    name = models.CharField(_("Name of User"), blank=True, max_length=255)
    fullname = models.CharField(verbose_name=_("Fullname of user"), null=True, blank=True, max_length=255)
    patronymic = models.CharField(verbose_name=_("Middle name of user"), null=True, blank=True, max_length=255)


    def save(self, *args, **kwargs):
        if self.fullname is None:
            self.fullname = f"{self.last_name} {self.first_name}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.username


    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"username": self.username})


class Supplier(models.Model):
    supplier_name = models.CharField(verbose_name=_("Name of supplier or organization"), max_length=255)
    user = models.OneToOneField(User, verbose_name=_("Supplier account"), on_delete=models.CASCADE)
    website = models.URLField(verbose_name=_("Website"), null=True, blank=True)
    phone_number = models.CharField(verbose_name=_("Phone number of supplier"), max_length=20)
    email = models.EmailField(verbose_name=_("Email of supplier"), null=True, blank=True)

    def __str__(self):
        return self.supplier_name
