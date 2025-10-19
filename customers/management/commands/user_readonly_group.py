from django.core.management.base import BaseCommand
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from customers.models import Customer

class Command(BaseCommand):
    help = 'Create user_readonly_group with view permission for Customer'

    def handle(self, *args, **kwargs):
        ct = ContentType.objects.get_for_model(Customer)
        codename = f'view_{ct.model}'
        perm, created_perm = Permission.objects.get_or_create(
            codename=codename,
            content_type=ct,
            defaults={'name': f'Can view {ct.name}'}
        )
        if created_perm:
            self.stdout.write(self.style.SUCCESS(f'Permission {codename} was created.'))
        else:
            self.stdout.write(f'Permission {codename} exists.')

        group_name = 'macallan_readonly'
        group, created_group = Group.objects.get_or_create(name=group_name)
        group.permissions.add(perm)
        if created_group:
            self.stdout.write(self.style.SUCCESS(f'Group "{group_name}" created and permission added.'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Group "{group_name}" updated with permission.'))
