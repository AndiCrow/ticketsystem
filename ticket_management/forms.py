from django import forms
from .models import Ticket, TicketNote

class TicketForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['title', 'description', 'category']


class NoteForm(forms.ModelForm):
    class Meta:
        model = TicketNote
        fields = ['content']
        

class TicketStatusForm(forms.ModelForm):
    class Meta:
        model = Ticket
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
        }
        