from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

    def __str__(self):
        return self.user.username

    def friends(self):
        return [rel.peer for rel in self.relationships.filter(status=Relationship.RelationshipStatus.FRIEND).prefetch_related('peer')]

class Relationship(models.Model):
    class Meta:
        unique_together = ('user', 'peer')

    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='relationships')
    peer = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='rev_relationships')

    class RelationshipStatus(models.TextChoices):
        BLOCKED = "B", "Blocked"
        FRIEND = "F", "Friend"

    status = models.CharField(
        max_length=2,
        choices=RelationshipStatus.choices,
    )

    def __str__(self):
        return f'{self.user} - {self.peer}: {self.status}'
