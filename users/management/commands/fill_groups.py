from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.core.management import BaseCommand

from blog.models import Article
from jobs.models import Mailing
from users.models import User


content_type_1 = ContentType.objects.get_for_model(Mailing)
mailing_permissions = ['view_mailing', 'set_activity']

content_type_2 = ContentType.objects.get_for_model(User)
user_permissions = ['view_user', 'set_activity']

content_type_3 = ContentType.objects.get_for_model(Article)
article_permissions = ['set_activity']


class Command(BaseCommand):

    def handle(self, *args, **options):
        m_group = Group.objects.create(name='manager')
        cm_group = Group.objects.create(name='content_manager')
        for perm in mailing_permissions:
            permission = Permission.objects.get(codename=perm, content_type=content_type_1)
            m_group.permissions.add(permission)
        for perm in user_permissions:
            permission = Permission.objects.get(codename=perm, content_type=content_type_2)
            m_group.permissions.add(permission)
        for perm in article_permissions:
            permission = Permission.objects.get(codename=perm, content_type=content_type_3)
            cm_group.permissions.add(permission)
        m_group.save()
        cm_group.save()
