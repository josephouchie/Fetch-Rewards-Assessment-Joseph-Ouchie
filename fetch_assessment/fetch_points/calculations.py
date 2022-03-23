from django.db.models import Sum
from .models import Transaction
from collections import Counter

def spend(sp_points,sp_timestamp):
	# To calculate the total points from all vendors!
	tot_balances = find_balances()
	tot_points = 0
	for bal in tot_balances:
	    tot_points += bal['total']
	if int(sp_points) <= tot_points: # prevents overspending
		debits = 0
		for trans in Transaction.objects.all():
			if int(trans.points) < 0:
				debits += abs(trans.points) # calculate the sum of all negative values (i.e. spent points) as a positive number
		ordered = Transaction.objects.all().order_by('timestamp') #re-order from oldest to newest
		# Runs through the whole list to calculate the most recently spent points
		trans_list = []
		rem_spend = sp_points
		for ord_trans in ordered: # for each transaction in the re-ordered database
			if ord_trans.points > 0: # ignore spending/debiting transactions
				if ord_trans.points <= debits:
					debits -= ord_trans.points # this assigns previously spent debits to the points in that transaction
				elif ord_trans.points > debits:
					remain = ord_trans.points - debits
					debits = 0
					if remain < rem_spend:
						trans_list.append((ord_trans.payer,-abs(remain),sp_timestamp))
						rem_spend -= remain
					elif remain == rem_spend:
						trans_list.append((ord_trans.payer,-abs(rem_spend),sp_timestamp))
						break
					else:
						trans_list.append((ord_trans.payer,-abs(rem_spend),sp_timestamp))
						break
		# Aggregate the list of tuples
		trans_point = Counter() # Counter() converts to a dictionary
		for vendor, point, dtime in trans_list: # used 'vendor', 'point', and 'dtime' to avoid variable overlapping/confusion
			trans_point[vendor] += point # this aggregates the total debiting points for each payer

		for name in trans_point:
			Transaction.objects.create(payer=name,points=trans_point[name],timestamp=trans_list[0][2]) 
			# used 'trans_list[0][2]', since the timestamp should be the same for all entries in this particular transaction
		return ('Done!')
	else:
		return ('Error!')

def find_balances():
	# This command filters for each 'payer' and aggregates the points for each transaction entered for that payer
	all_balances = Transaction.objects.filter().values('payer').order_by('payer').annotate(total=Sum('points'))
	# returns a list of nested dictionaries, with each entry having the following format: {'payer': total}
	return all_balances


