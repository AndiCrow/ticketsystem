from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Ticket, Category, TicketNote
from .forms import TicketForm, NoteForm, TicketStatusForm
from django.contrib import messages

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # Automatisches Einloggen nach Registrierung
            return redirect('ticket_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


@login_required
def ticket_list(request):
    tickets = Ticket.objects.all()  
    visible_tickets = [ticket for ticket in tickets if ticket.can_view(request.user)]

   
    for ticket in visible_tickets:
        print(f"DEBUG: Ticket ID: {ticket.id}, Title: {ticket.title}")

    return render(request, 'ticket_management/ticket_list.html', {'tickets': visible_tickets})



@login_required
def create_ticket(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            ticket = form.save(commit=False)
            ticket.created_by = request.user
            ticket.save()
            return redirect('ticket_list')
    else:
        form = TicketForm()
    return render(request, 'ticket_management/create_ticket.html', {'form': form})

@login_required
def ticket_detail(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)
    if not ticket.can_view(request.user):
        return render(request, 'ticket_management/ticket_detail.html', {'ticket': ticket})
    notes = ticket.notes.all()
    return render(request, 'ticket_management/ticket_detail.html', {'ticket': ticket, 'notes': notes})


def logout_view(request):
    logout(request)
    return redirect('registration/login.html')

@login_required
def edit_ticket(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    if not ticket.can_view(request.user):
        return render(request, '403.html')  

    if request.method == 'POST':
     
        ticket_form = TicketForm(request.POST, instance=ticket)
        if ticket_form.is_valid():
            ticket_form.save()
        
      
        note_form = NoteForm(request.POST)
        if note_form.is_valid():
            note = note_form.save(commit=False)
            note.ticket = ticket
            note.created_by = request.user
            note.save()

        return redirect('ticket_detail', ticket_id=ticket.id)
    else:
        ticket_form = TicketForm(instance=ticket)
        note_form = NoteForm()

    return render(request, 'ticket_management/edit_ticket.html', {
        'ticket': ticket,
        'ticket_form': ticket_form,
        'note_form': note_form,

    })

@login_required
def change_ticket_status(request, ticket_id):
    ticket = get_object_or_404(Ticket, id=ticket_id)

    # Zugriffskontrolle: Nur der Ersteller, Admins oder bestimmte Gruppen dürfen den Status ändern
    if not ticket.can_view(request.user):
        return render(request, '403.html')  # Zugriff verweigert

    if request.method == 'POST':
        form = TicketStatusForm(request.POST, instance=ticket)
        if form.is_valid():
            form.save()  # Status wird aktualisiert
            messages.success(request, f"Status für das Ticket '{ticket.title}' wurde geändert.")
            return redirect('ticket_detail', ticket_id=ticket.id)
    else:
        form = TicketStatusForm(instance=ticket)

    return render(request, 'ticket_management/change_status.html', {
        'ticket': ticket,
        'form': form,
    })
