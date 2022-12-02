import re
from django.utils.translation import gettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager
from django.contrib.auth.models import PermissionsMixin


class TrixUserManager(BaseUserManager):

    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(email, password=password)
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """
    The Trix user model.
    """
    is_active = models.BooleanField(
        default=True,
        verbose_name=_('Is active?'),
        help_text=_('User is active? Inactive users can not log in.')
    )

    is_admin = models.BooleanField(
        default=False,
        verbose_name=_('Is superuser?'),
        help_text=_('User is superuser? Superusers have full access to the admin UI.')
    )

    email = models.EmailField(
        max_length=255,
        blank=False,
        unique=True
    )

    consent_datetime = models.DateTimeField(
        blank=True,
        null=True
    )

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = TrixUserManager()

    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")
        ordering = ['email']

    def __str__(self):
        return self.displayname

    def get_long_name(self):
        return self.displayname

    def get_short_name(self):
        return self.displayname

    @property
    def displayname(self):
        """
        Get a name for the user. Use this whenever you show the user in the UI.
        """
        return self.email

    def is_admin_on_anything(self):
        if self.is_staff:
            return True
        else:
            return Course.objects.filter(admins=self).exists()

    def is_course_owner(self, course):
        if self.is_staff:
            return True
        else:
            return self.owner.filter(id=course.id).exists()

    @property
    def is_staff(self):
        """
        Is the user a member of staff?
        """
        return self.is_admin

    @property
    def is_superuser(self):
        """
        Is the user a superuser?
        """
        return self.is_admin

    @property
    def has_consented(self):
        return self.consent_datetime is not None


class Tag(models.Model):
    """
    A tag for an assignment and a course.
    """

    # NOTE: Help and field size in UI must make users use short tags
    tag = models.CharField(
        unique=True,
        max_length=30)

    category = models.CharField(
        max_length=1,
        blank=True,
        null=False,
        default='',
        choices=[
            ('', _('No category')),
            ('c', _('Course')),
            ('p', _('Period')),
        ]
    )

    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        ordering = ['tag']

    def __str__(self):
        return self.tag

    @classmethod
    def normalize_tag(cls, tag):
        """
        Normalize a tag:

            - Lowercase.
            - Replace all whitespace with a single space.
            - Strip all whitespace at both ends.
        """
        return re.sub(r'\s+', ' ', tag.strip().lower().lstrip('-'))

    @classmethod
    def split_commaseparated_tags(cls, commaseparatedtags):
        """
        Normalize and then split tags on commas and spaces.
        Empty tags are removed.
        """
        if commaseparatedtags.strip() == '':
            return []
        else:
            return [
                cls.normalize_tag(tagstring)
                for tagstring in list([_f for _f in re.split(r'[,\s]', commaseparatedtags) if _f])]


class Course(models.Model):
    """
    A course is simply a tag with an optional active period tag, and a list of admins and owners.
    """
    admins = models.ManyToManyField(User, blank=True, related_name="admin")
    owner = models.ManyToManyField(
        User,
        blank=True,
        related_name="owner",
    )

    description = models.TextField(
        verbose_name=_('Description'),
        blank=True,
        null=False,
        default='')

    course_tag = models.ForeignKey(
        Tag,
        related_name='course_set',
        on_delete=models.CASCADE,
        limit_choices_to={
            'category': 'c'
        })

    active_period = models.ForeignKey(
        Tag,
        related_name='active_period_set',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        limit_choices_to={
            'category': 'p'
        })

    class Meta:
        verbose_name = _('Course')
        verbose_name_plural = _('Courses')
        ordering = ['course_tag']

    def __str__(self):
        return self.course_tag.tag


class AssignmentQuerySet(models.query.QuerySet):
    """ AssignmentQuerySet

    """

    def filter_by_tag(self, tag):
        return self.filter(tags=tag)


class AssignmentManager(models.Manager):
    """docstring for AssignmentManager"""

    def get_queryset(self):
        return AssignmentQuerySet(self.model, using=self._db)

    def filter_by_tag(self, tag):
        return self.get_queryset().filter_by_tag(tag)

    def filter_by_tags(self, tags):
        qryset = self.get_queryset()
        for tag in tags:
            qryset = qryset.filter_by_tag(tag)
        return qryset


class Assignment(models.Model):
    title = models.CharField(
        max_length=255,
        verbose_name=_('Title'))
    tags = models.ManyToManyField(
        Tag,
        verbose_name=_('Tags'))
    text = models.TextField(
        verbose_name=_('Assignment text'),
        help_text=_('Write the assignment here.'))
    solution = models.TextField(
        blank=True, null=False, default='',
        verbose_name=_('Solution'),
        help_text=_('If you want your students to be able to view a suggested solution, write the '
                    'solution here.'))
    created_datetime = models.DateTimeField(
        verbose_name=_('Created'),
        auto_now_add=True)
    lastupdate_datetime = models.DateTimeField(
        verbose_name=_('Last changed'),
        auto_now=True)
    HIDDEN_CHOICES = [(True, _('Yes')), (False, _('No'))]
    hidden = models.BooleanField(
        null=True,
        choices=HIDDEN_CHOICES,
        default=False,
        verbose_name=_('Hide assignment from students'))

    objects = AssignmentManager()

    class Meta:
        verbose_name = _('Assignment')
        verbose_name_plural = _('Assignments')
        ordering = ['-lastupdate_datetime']

    def __str__(self):
        return self.title

    @property
    def readable_id(self):
        return str(self.id)

    def _normalize_text(self, text):
        # Normalize newlines. Just makes sure newlines is \n,
        # does not remove any empty lines or anything like that.
        text = '\n'.join(text.splitlines())

        # Convert tabs to spaces. Editing tabs through the browser
        # is very error prone, so it is safer to just convert them.
        text = text.replace('\t', '    ')

        return text

    def clean(self):
        # NOTE: Without this, the YAML output for bulk editing becomes unreadable
        self.text = self._normalize_text(self.text)
        self.solution = self._normalize_text(self.solution)


class HowSolved(models.Model):
    """
    This class holds information on how the assignment was solved.
    """
    howsolved = models.CharField(
        max_length=10,
        null=False,
        choices=[
            ('bymyself', _('Solved by myself')),
            ('withhelp', _('Solved with help')),
        ]
    )

    assignment = models.ForeignKey(Assignment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    solved_datetime = models.DateTimeField(
        verbose_name=_('Solved'),
        auto_now=True
    )

    def __str__(self):
        return self.howsolved


class Permalink(models.Model):
    course = models.ForeignKey(
        Course,
        verbose_name=_('Course'),
        on_delete=models.CASCADE)
    tags = models.ManyToManyField(
        Tag,
        verbose_name=_('Tags'))
    title = models.CharField(
        verbose_name=_('Title'),
        max_length=255,
        blank=True,
        null=False,
        default='')
    description = models.TextField(
        verbose_name=_('Description'),
        blank=True,
        null=False,
        default='')

    class Meta:
        verbose_name = _('Permalink')
        verbose_name_plural = _('Permalinks')
        ordering = ['title']

    def __str__(self):
        return self.title

    @property
    def readable_id(self):
        return str(self.id)
