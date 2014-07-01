import re
from django.utils.translation import ugettext_lazy as _
from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import BaseUserManager


class TrixUserManager(BaseUserManager):
 
    def create_user(self, email, password=None):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')

        user = self.model(
            email=TrixUserManager.normalize_email(email),
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


class User(AbstractBaseUser):
    """
    The Trix user model.
    """
    is_active = models.BooleanField(default=True,
            verbose_name=_('Is active?'),
            help_text=_('User is active? Inactive users can not log in.'))

    is_admin = models.BooleanField(default=False,
            verbose_name=_('Is admin?'),
            help_text=_('User is admin? Admins have full access to the admin UI.'))

    email = models.EmailField(max_length=250, blank=False, unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = TrixUserManager()


    class Meta:
        verbose_name = _("User")
        verbose_name_plural = _("Users")


    def __unicode__(self):
        return self.displayname

    def get_short_name(self):
        return self.displayname

    @property
    def displayname(self):
        """
        Get a name for the user. Use this whenever you show the user in the UI.
        """
        return self.email

    def has_perm(self, perm, obj=None):
        """
        Does the user have a specific permission?

        We do not use the permission system, so we answer YES.
        """
        return True

    def has_module_perms(self, app_label):
        """
        Does the user have permissions to view the app `app_label`?

        We do not use the permission system, so we answer YES.
        """
        return True

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



class TagQuerySet(models.query.QuerySet):
    def to_unicode(self):
        return ', '.join(tag.tag for tag in self.all())



class TagManager(models.Manager):
    use_for_related_fields = True

    def get_queryset(self):
        return TagQuerySet(self.model)

    def get_or_create(self, tag):
        try:
            tag = Tag.objects.get(tag=tag)
        except Tag.DoesNotExist:
            tag = Tag.objects.create(tag=tag)
        return tag



class Tag(models.Model):
    """
    A tag for an assignment and a course.
    """
    objects = TagManager()

    # NOTE: Help and field size in UI must make users use short tags
    tag = models.CharField(
        unique=True,
        max_length=30)

    category = models.CharField(
        max_length=1,
        blank=True, null=False,
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

    def __unicode__(self):
        return self.tag

    @classmethod
    def normalize_tag(cls, tag):
        """
        Normalize a tag:

            - Lowercase.
            - Replace all whitespace with a single space.
            - Strip all whitespace at both ends.
        """
        return re.sub(r'\s+', ' ', tag.strip().lower())

    @classmethod
    def split_commaseparated_tags(cls, commaseparatedtags):
        if commaseparatedtags.strip() == '':
            return []
        else:
            return [
                cls.normalize_tag(tagstring)
                for tagstring in commaseparatedtags.split(',')]


class Course(models.Model):
    """
    A course is simply a tag with an optional active period tag, and a list of admins.
    """
    admins = models.ManyToManyField(User)
    description = models.TextField(
            blank=True, null=False, default='') 

    #: TODO: Limit choices to ``c``-tags
    course_tag = models.ForeignKey(Tag, related_name='course_set')

    #: TODO: Limit choices to ``p``-tags
    active_period = models.ForeignKey(Tag, related_name='active_period_set',
        null=True, blank=True)

    class Meta:
        verbose_name = _('Course')
        verbose_name_plural = _('Courses')

    def __unicode__(self):
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
    tags = models.ManyToManyField(Tag,
        verbose_name=_('Tags'))
    text = models.TextField(
        verbose_name=_('Assignment text'),
        help_text=_('Write the assignment here.'))
    solution = models.TextField(
        blank=True, null=False, default='',
        verbose_name=_('Solution'),
        help_text=_('If you want your students to be able to view a suggested solution, write the solution here.'))

    objects = AssignmentManager()

    class Meta:
        verbose_name = _('Assignment')
        verbose_name_plural = _('Assignments')

    def __unicode__(self):
        return self.title

    @property
    def readable_id(self):
        return str(self.id)

    # def replace_tags(self, *tagstrings):
    #     self.tags.clear()
    #     for tagstring in tagstrings:
    #         tag = Tag.objects.get_or_create(tagstring)
    #         self.tags.add(tag)


class HowSolved(models.Model):
    """This class holds information on how the assignment was solved.


    """
    howsolved = models.CharField(
        max_length=10,
        null=False,
        choices=[
            ('bymyself', _('Solved by myself')),
            ('withhelp', _('Solved with help')),
        ]
    )
    
    assignment = models.ForeignKey(Assignment)
    user = models.ForeignKey(User)

    def  __unicode__(self):
        return self.howsolved


class Permalink(models.Model):
    tags = models.ManyToManyField(Tag)
    title = models.CharField(max_length=255,
        blank=True, null=False, default='')
    description = models.TextField(
        blank=True, null=False, default='')

    class Meta:
        verbose_name = _('Permalink')
        verbose_name_plural = _('Permalinks')

    def  __unicode__(self):
        return self.title

    @property
    def readable_id(self):
        return str(self.id)
