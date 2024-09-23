from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group, Permission
from .models import CustomUser

@receiver(post_save, sender=CustomUser)
def assign_user_permissions(sender, instance, created, **kwargs):
    if created:
        if instance.role == "coach":
            # Assign coach group and permissions
            coach_group, _ = Group.objects.get_or_create(name="Coach")
            instance.groups.add(coach_group)
            coach_permissions = Permission.objects.filter(
                codename__in=[
                    "can_add_team",
                    "can_add_player",
                    "can_upload_videos",
                    "can_view_metrics",
                ]
            )
            instance.user_permissions.set(coach_permissions)

        elif instance.role == "agent":
            # Assign agent group and permissions
            agent_group, _ = Group.objects.get_or_create(name="Agent")
            instance.groups.add(agent_group)
            agent_permissions = Permission.objects.filter(
                codename__in=[
                    "can_view_player",
                    "can_view_videos",
                    "can_view_teams",
                ]
            )
            instance.user_permissions.set(agent_permissions)

        instance.save()
