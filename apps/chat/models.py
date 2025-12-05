from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

class ThreadManager(models.Manager):
    def by_user(self, user):
        return self.get_queryset().filter(Q(sender=user) | Q(receiver=user)).distinct()

    def get_or_new(self, user, other_username):
        if user.username == other_username:
            return None
        
        # Check if thread exists in either direction (A->B or B->A)
        q_lookup1 = Q(sender=user) & Q(receiver__username=other_username)
        q_lookup2 = Q(sender__username=other_username) & Q(receiver=user)
        
        qs = self.get_queryset().filter(q_lookup1 | q_lookup2).distinct()

        if qs.count() == 1:
            return qs.first(), False
        elif qs.count() > 1:
            return qs.order_by('timestamp').first(), False
        else:
            try:
                other_user = User.objects.get(username=other_username)
                # Create new thread with user as sender
                obj = self.model(sender=user, receiver=other_user)
                obj.save()
                return obj, True
            except User.DoesNotExist:
                return None, False

class Thread(models.Model):
    # Renamed from first_person/second_person to sender/receiver
    sender = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='thread_sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='thread_receiver')
    
    updated = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    objects = ThreadManager()

    class Meta:
        unique_together = ['sender', 'receiver']

    def __str__(self):
        return f'{self.sender} - {self.receiver}'

class ChatMessage(models.Model):
    thread = models.ForeignKey(Thread, null=True, blank=True, on_delete=models.CASCADE, related_name='chatmessage_thread')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False) # New field to track read status

    def __str__(self):
        return f'{self.user.username}: {self.message[:20]}'