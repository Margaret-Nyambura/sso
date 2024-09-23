from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import Permission
from .models import CustomUser 
from .permissions import CoachPermissions, AgentPermissions

@receiver(post_save, sender=CustomUser)
def handle_user_created_or_updated(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'coach':
            permissions = CoachPermissions().get_permissions('POST')
            for perm in permissions:
                permission = Permission.objects.get(codename=perm)
                instance.user_permissions.add(permission)
            print(f'Coach permissions assigned: {permissions}')
        elif instance.role == 'agent':
            permissions = AgentPermissions().get_permissions('GET')
            for perm in permissions:
                permission = Permission.objects.get(codename=perm)
                instance.user_permissions.add(permission)
            print(f'Agent permissions assigned: {permissions}')
    else:
        print(f'User {instance.username} updated. Current permissions: {instance.get_user_permissions()}')

@receiver(post_delete, sender=CustomUser)
def handle_user_deleted(sender, instance, **kwargs):
    print(f'User {instance.username} deleted')

 
