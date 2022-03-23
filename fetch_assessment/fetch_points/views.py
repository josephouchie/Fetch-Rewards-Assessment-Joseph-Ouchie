from django.shortcuts import render
from django.http import HttpResponse
from . import calculations
from .models import Transaction

def add_spend(request):

    new_transaction = Transaction()

    new_transaction.payer = request.POST.get('payer',False) #gets the 'payer' from the HTML Post
    new_transaction.points = request.POST.get('points',False) #gets the 'points' from the HTML Post, WARNING: it still allows for negative values!
    new_transaction.timestamp = request.POST.get('timestamp',False) #gets the 'timestamp' from the HTML Post

    if new_transaction.payer != False: # used to prevent the transaction saving an empty transaction when the website is first pulled up
        new_transaction.save() # enters a new transaction

    new_spend_points = request.POST.get('sp_points', False) # gets the points spent from the spending form
    new_spend_timestamp = request.POST.get('sp_timestamp', False) # gets the timestamp of the new points spent
    if new_spend_points != False:
        new_spend = calculations.spend(int(new_spend_points),new_spend_timestamp) # Calculates the new transactions based on the spending attempt
        # in the case of overspending, the program does nothing... does not give any warning to the user!

    # Calculate again to update
    tot_balances = calculations.find_balances()
    # To calculate the total points from all vendors!
    tot_points = 0
    for bal in tot_balances:
        tot_points += bal['total']

    context = {
        'transactions': Transaction.objects.all(), # allows the transactions data to be passed into the render command
        'balances': tot_balances, # allows the balance data (as a nested dictionary within a list) to be passed into the render command
        'tot_balance': tot_points, # allows the total points data to be passed into the render command
        # allows the HTML template to access the transactions data using its eponymous key
    } 

    return render(request,'fetch_points/home.html',context) # render still returns a HttpResponse, Render passes a dictionary
    # The render() function takes the request object as its first argument, a template name as its second argument, and a dictionary as its optional third argument