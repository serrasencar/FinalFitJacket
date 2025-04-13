from django.db import models
from django.conf import settings

class Friendship(models.Model):
    # Ensure user1 has the lower ID to avoid duplicates
    user1 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="friendship_user1")
    user2 = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="friendship_user2")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user1', 'user2')  # Prevent duplicate entries

    def save(self, *args, **kwargs):
        # Swap user1/user2 to ensure user1.id < user2.id
        if self.user1.id > self.user2.id:
            self.user1, self.user2 = self.user2, self.user1
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user1.username} ↔ {self.user2.username}"