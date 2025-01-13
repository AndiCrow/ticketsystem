from django.db import models
from django.contrib.auth.models import User, Group

class Category(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Ticket(models.Model):
    STATUS_CHOICES = [
        ('open', 'Offen'),
        ('in_progress', 'In Bearbeitung'),
        ('closed', 'Geschlossen'),
    ]

    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="tickets")
    created_by = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def can_view(self, user):
        if user.is_superuser:  
            return True
        if self.created_by == user:  
            return True
        if user.groups.filter(name='Ticket-Viewer').exists():  
            return True
        return False
    

class TicketNote(models.Model):
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name="notes")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Notiz von {self.created_by} am {self.created_at.strftime('%d.%m.%Y %H:%M')}"