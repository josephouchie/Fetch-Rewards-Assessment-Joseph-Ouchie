from django.test import TestCase
from .models import Transaction
from . import calculations
from . import views

"""
class test_ui(TestCase):

	def test_
"""

class test_spend(TestCase):

	def test_og_spend(self):
		# Test the original situation outlined in the instruction document
		Transaction.objects.create(payer='DANNON',points=1000,timestamp='2020-11-02T14:00:00Z')
		Transaction.objects.create(payer='UNILEVER',points=200,timestamp='2020-10-31T11:00:00Z')
		Transaction.objects.create(payer='DANNON',points=-200,timestamp='2020-10-31T15:00:00Z')
		Transaction.objects.create(payer='MILLER COORS',points=10000,timestamp='2020-11-01T14:00:00Z')
		Transaction.objects.create(payer='DANNON',points=300,timestamp='2020-10-31T10:00:00Z')

		new_spend = 5000
		new_timestamp = '2022-01-31T10:00:00Z'
		new_spend_status = calculations.spend(int(new_spend),new_timestamp)
		new_balances = calculations.find_balances()

		for bal in new_balances:
			if bal['payer'] == 'DANNON':
				new_dannon_bal = bal['total']
			if bal['payer'] == 'UNILEVER':
				new_unilever_bal = bal['total']
			if bal['payer'] == 'MILLER COORS':
				new_millercoors_bal = bal['total']

		dannon_trans = Transaction.objects.get(id=6) # WARNING 'id's do not start from zero!
		unilever_trans = Transaction.objects.get(id=7)
		millercoors_trans = Transaction.objects.get(id=8)

		# test correct payer names
		self.assertEqual(dannon_trans.payer, 'DANNON')
		self.assertEqual(unilever_trans.payer, 'UNILEVER')
		self.assertEqual(millercoors_trans.payer, 'MILLER COORS')
		# test correct point amounts
		self.assertEqual(-abs(dannon_trans.points), -100)
		self.assertEqual(-abs(unilever_trans.points), -200)
		self.assertEqual(-abs(millercoors_trans.points), -4700)
		# test correct timestamp
		self.assertEqual(dannon_trans.timestamp, '2022-01-31T10:00:00Z') # timestamps should be the stamp for a single spending attempt
		self.assertEqual(unilever_trans.timestamp, '2022-01-31T10:00:00Z')
		self.assertEqual(millercoors_trans.timestamp, '2022-01-31T10:00:00Z')
		# test correct balances
		self.assertEqual(new_dannon_bal, 1000)
		self.assertEqual(new_unilever_bal, 0)
		self.assertEqual(new_millercoors_bal, 5300)

	def test_multiple_trans_sequential(self):
		# Test to see if the program reacts properly to multiple transactions of the same 'payer' in a row
		Transaction.objects.create(payer='UNILEVER',points=1000,timestamp='2020-11-02T14:00:00Z')
		Transaction.objects.create(payer='DANNON',points=200,timestamp='2020-10-31T11:00:00Z') #2nd
		Transaction.objects.create(payer='DANNON',points=300,timestamp='2020-10-31T15:00:00Z')	#3rd
		Transaction.objects.create(payer='MILLER COORS',points=10000,timestamp='2020-11-01T14:00:00Z')
		Transaction.objects.create(payer='DANNON',points=100,timestamp='2020-10-31T10:00:00Z') # DANNON has 3 transactions in a row

		new_spend = 500
		new_timestamp = '2022-01-31T10:00:00Z'
		new_spend_status = calculations.spend(int(new_spend),new_timestamp)
		new_balances = calculations.find_balances()

		for bal in new_balances:
			if bal['payer'] == 'DANNON':
				new_dannon_bal = bal['total']
			if bal['payer'] == 'UNILEVER':
				new_unilever_bal = bal['total']
			if bal['payer'] == 'MILLER COORS':
				new_millercoors_bal = bal['total']

		dannon_trans = Transaction.objects.get(id=6) # WARNING 'id's do not start from zero!

		# test correct payer names
		self.assertEqual(dannon_trans.payer, 'DANNON')

		# test correct point amounts
		self.assertEqual(-abs(dannon_trans.points), -500)

		# test correct timestamp
		self.assertEqual(dannon_trans.timestamp, '2022-01-31T10:00:00Z')

		# test correct balances
		self.assertEqual(new_dannon_bal, 100) # 100 + 200 + 300 - 500 = 100 
		self.assertEqual(new_unilever_bal, 1000)
		self.assertEqual(new_millercoors_bal, 10000)

	def test_multiple_spend_before(self):
		# Test to see how the program reacts to multiple spending periods before the new spend
		Transaction.objects.create(payer='DANNON',points=-100,timestamp='2020-11-02T14:00:00Z') # spent another 100 points
		Transaction.objects.create(payer='UNILEVER',points=1000,timestamp='2020-10-31T11:00:00Z')
		Transaction.objects.create(payer='DANNON',points=-200,timestamp='2020-10-31T15:00:00Z') # spent 200 points
		Transaction.objects.create(payer='MILLER COORS',points=10000,timestamp='2020-11-01T14:00:00Z')
		Transaction.objects.create(payer='DANNON',points=1300,timestamp='2020-10-31T10:00:00Z')

		new_spend = 5000
		new_timestamp = '2022-01-31T10:00:00Z'
		new_spend_status = calculations.spend(int(new_spend),new_timestamp)
		new_balances = calculations.find_balances()

		for bal in new_balances:
			if bal['payer'] == 'DANNON':
				new_dannon_bal = bal['total']
			if bal['payer'] == 'UNILEVER':
				new_unilever_bal = bal['total']
			if bal['payer'] == 'MILLER COORS':
				new_millercoors_bal = bal['total']

		dannon_trans = Transaction.objects.get(id=6) # WARNING 'id's do not start from zero!
		unilever_trans = Transaction.objects.get(id=7)
		millercoors_trans = Transaction.objects.get(id=8)

		# test correct payer names
		self.assertEqual(dannon_trans.payer, 'DANNON')
		self.assertEqual(unilever_trans.payer, 'UNILEVER')
		self.assertEqual(millercoors_trans.payer, 'MILLER COORS')
		# test correct point amounts
		self.assertEqual(-abs(dannon_trans.points), -1000)
		self.assertEqual(-abs(unilever_trans.points), -1000)
		self.assertEqual(-abs(millercoors_trans.points), -3000)
		# test correct timestamp
		self.assertEqual(dannon_trans.timestamp, '2022-01-31T10:00:00Z') # timestamps should be the stamp for a single spending attempt
		self.assertEqual(unilever_trans.timestamp, '2022-01-31T10:00:00Z')
		self.assertEqual(millercoors_trans.timestamp, '2022-01-31T10:00:00Z')
		# test correct balances
		self.assertEqual(new_dannon_bal, 0) # 1300 - 200 - 100 - 1000 = 0
		self.assertEqual(new_unilever_bal, 0) # 1000 - 1000 = 0
		self.assertEqual(new_millercoors_bal, 7000) # 10000 - 3000 = 0

	def test_multiple_spends(self):
		# Test to see how the program reacts to multiple spending attempts
		Transaction.objects.create(payer='DANNON',points=1000,timestamp='2020-11-02T14:00:00Z') # OG transactions
		Transaction.objects.create(payer='UNILEVER',points=200,timestamp='2020-10-31T11:00:00Z')
		Transaction.objects.create(payer='DANNON',points=-200,timestamp='2020-10-31T15:00:00Z')
		Transaction.objects.create(payer='MILLER COORS',points=10000,timestamp='2020-11-01T14:00:00Z')
		Transaction.objects.create(payer='DANNON',points=300,timestamp='2020-10-31T10:00:00Z')

		# 1st spending attempt
		new_spend_1 = 1000
		new_timestamp_1 = '2022-01-31T10:00:00Z'
		new_spend_status_1 = calculations.spend(int(new_spend_1),new_timestamp_1)
		
		# 2nd spending attempt

		new_spend_2 = 2000
		new_timestamp_2 = '2022-02-31T10:00:00Z'
		new_spend_status_2 = calculations.spend(int(new_spend_2),new_timestamp_2)

		new_balances = calculations.find_balances()

		for bal in new_balances:
			if bal['payer'] == 'DANNON':
				new_dannon_bal = bal['total']
			if bal['payer'] == 'UNILEVER':
				new_unilever_bal = bal['total']
			if bal['payer'] == 'MILLER COORS':
				new_millercoors_bal = bal['total']

		dannon_trans_1 = Transaction.objects.get(id=6) # WARNING 'id's do not start from zero!
		unilever_trans_1 = Transaction.objects.get(id=7)
		millercoors_trans_1 = Transaction.objects.get(id=8)

		millercoors_trans_2 = Transaction.objects.get(id=9)	# Miller Coors should be the only transaction in the 2nd spending attempt	

		# test correct payer names
		self.assertEqual(dannon_trans_1.payer, 'DANNON')
		self.assertEqual(unilever_trans_1.payer, 'UNILEVER')
		self.assertEqual(millercoors_trans_1.payer, 'MILLER COORS')

		self.assertEqual(millercoors_trans_2.payer, 'MILLER COORS')

		# test correct point amounts
		self.assertEqual(-abs(dannon_trans_1.points), -100)
		self.assertEqual(-abs(unilever_trans_1.points), -200)
		self.assertEqual(-abs(millercoors_trans_1.points), -700)

		self.assertEqual(-abs(millercoors_trans_2.points), -2000)

		# test correct timestamp
		self.assertEqual(dannon_trans_1.timestamp, '2022-01-31T10:00:00Z')
		self.assertEqual(unilever_trans_1.timestamp, '2022-01-31T10:00:00Z')
		self.assertEqual(millercoors_trans_1.timestamp, '2022-01-31T10:00:00Z')

		self.assertEqual(millercoors_trans_2.timestamp, '2022-02-31T10:00:00Z')

		# test correct balances
		self.assertEqual(new_dannon_bal, 1000) # 1300 - 200 - 100 = 1000
		self.assertEqual(new_unilever_bal, 0) # 200 - 200 = 0
		self.assertEqual(new_millercoors_bal, 7300) # 10000 - 700 - 2000 = 7300

	def test_liquidate_before(self):
		# Test to see how the program reacts to a 'payer' being liquidated before the new spend
		Transaction.objects.create(payer='UNILEVER',points=200,timestamp='2020-10-31T11:00:00Z')
		Transaction.objects.create(payer='DANNON',points=-300,timestamp='2020-10-31T15:00:00Z') #DANNON gets liquidated
		Transaction.objects.create(payer='MILLER COORS',points=10000,timestamp='2020-11-01T14:00:00Z')
		Transaction.objects.create(payer='DANNON',points=300,timestamp='2020-10-31T10:00:00Z')

		new_spend = 5000
		new_timestamp = '2022-01-31T10:00:00Z'
		new_spend_status = calculations.spend(int(new_spend),new_timestamp)
		new_balances = calculations.find_balances()

		for bal in new_balances:
			if bal['payer'] == 'DANNON':
				new_dannon_bal = bal['total']
			if bal['payer'] == 'UNILEVER':
				new_unilever_bal = bal['total']
			if bal['payer'] == 'MILLER COORS':
				new_millercoors_bal = bal['total']

		unilever_trans = Transaction.objects.get(id=5)
		millercoors_trans = Transaction.objects.get(id=6)

		# test correct payer names
		self.assertEqual(unilever_trans.payer, 'UNILEVER')
		self.assertEqual(millercoors_trans.payer, 'MILLER COORS')
		# test correct point amounts
		self.assertEqual(-abs(unilever_trans.points), -200)
		self.assertEqual(-abs(millercoors_trans.points), -4800)
		# test correct timestamp
		self.assertEqual(unilever_trans.timestamp, '2022-01-31T10:00:00Z')
		self.assertEqual(millercoors_trans.timestamp, '2022-01-31T10:00:00Z')
		# test correct balances
		self.assertEqual(new_dannon_bal, 0) # 300 - 300 = 0
		self.assertEqual(new_unilever_bal, 0) # 200 - 200 = 0
		self.assertEqual(new_millercoors_bal, 5200) # 10000 - 4800 = 5200

	def test_multiple_liquidate_before(self):
		# Test to see how the program reacts to multiple 'payers' being liquidated prior to the new spend
		Transaction.objects.create(payer='UNILEVER',points=-200,timestamp='2020-11-02T14:00:00Z') # UNILEVER Liquidated
		Transaction.objects.create(payer='UNILEVER',points=200,timestamp='2020-10-31T11:00:00Z')
		Transaction.objects.create(payer='DANNON',points=-300,timestamp='2020-10-31T15:00:00Z') # DANNON Liquidated
		Transaction.objects.create(payer='MILLER COORS',points=10000,timestamp='2020-11-01T14:00:00Z')
		Transaction.objects.create(payer='DANNON',points=300,timestamp='2020-10-31T10:00:00Z')

		new_spend = 5000
		new_timestamp = '2022-01-31T10:00:00Z'
		new_spend_status = calculations.spend(int(new_spend),new_timestamp)
		new_balances = calculations.find_balances()

		for bal in new_balances:
			if bal['payer'] == 'DANNON':
				new_dannon_bal = bal['total']
			if bal['payer'] == 'UNILEVER':
				new_unilever_bal = bal['total']
			if bal['payer'] == 'MILLER COORS':
				new_millercoors_bal = bal['total']

		millercoors_trans = Transaction.objects.get(id=6) # Miller Coors should be the only transaction; the only balance left!

		# test correct payer names
		self.assertEqual(millercoors_trans.payer, 'MILLER COORS')
		# test correct point amounts
		self.assertEqual(-abs(millercoors_trans.points), -5000)
		# test correct timestamp
		self.assertEqual(millercoors_trans.timestamp, '2022-01-31T10:00:00Z')
		# test correct balances
		self.assertEqual(new_dannon_bal, 0) # 300 - 300 = 0
		self.assertEqual(new_unilever_bal, 0) # 200 - 200 = 0
		self.assertEqual(new_millercoors_bal, 5000) # 10000 - 5000 = 5000

	def test_multiple_liquidate(self):
		# Test to see how the program reacts to multiple 'payers' being liquidated during the new spend
		Transaction.objects.create(payer='UNILEVER',points=1000,timestamp='2020-10-31T11:00:00Z')
		Transaction.objects.create(payer='MILLER COORS',points=10000,timestamp='2020-11-01T14:00:00Z')
		Transaction.objects.create(payer='DANNON',points=500,timestamp='2020-10-31T10:00:00Z')

		new_spend = 5000
		new_timestamp = '2022-01-31T10:00:00Z'
		new_spend_status = calculations.spend(int(new_spend),new_timestamp)
		new_balances = calculations.find_balances()

		for bal in new_balances:
			if bal['payer'] == 'DANNON':
				new_dannon_bal = bal['total']
			if bal['payer'] == 'UNILEVER':
				new_unilever_bal = bal['total']
			if bal['payer'] == 'MILLER COORS':
				new_millercoors_bal = bal['total']

		dannon_trans_1 = Transaction.objects.get(id=4)
		unilever_trans_1 = Transaction.objects.get(id=5)
		millercoors_trans_1 = Transaction.objects.get(id=6)

		# test correct payer names
		self.assertEqual(dannon_trans_1.payer, 'DANNON')
		self.assertEqual(unilever_trans_1.payer, 'UNILEVER')
		self.assertEqual(millercoors_trans_1.payer, 'MILLER COORS')

		# test correct point amounts
		self.assertEqual(-abs(dannon_trans_1.points), -500)
		self.assertEqual(-abs(unilever_trans_1.points), -1000)
		self.assertEqual(-abs(millercoors_trans_1.points), -3500)

		# test correct timestamp
		self.assertEqual(dannon_trans_1.timestamp, '2022-01-31T10:00:00Z')
		self.assertEqual(unilever_trans_1.timestamp, '2022-01-31T10:00:00Z')
		self.assertEqual(millercoors_trans_1.timestamp, '2022-01-31T10:00:00Z')

		# test correct balances
		self.assertEqual(new_dannon_bal, 0) # 500 - 500 = 0
		self.assertEqual(new_unilever_bal, 0) # 1000 - 1000 = 0
		self.assertEqual(new_millercoors_bal, 6500) # 10000 - 3500 = 6500

	def test_all_liquidate(self):
		# Test to see how the program reacts to all 'payers' being liquidated during the new spend
		Transaction.objects.create(payer='DANNON',points=1000,timestamp='2020-11-02T14:00:00Z')
		Transaction.objects.create(payer='UNILEVER',points=200,timestamp='2020-10-31T11:00:00Z')
		Transaction.objects.create(payer='DANNON',points=-200,timestamp='2020-10-31T15:00:00Z')
		Transaction.objects.create(payer='MILLER COORS',points=10000,timestamp='2020-11-01T14:00:00Z')
		Transaction.objects.create(payer='DANNON',points=300,timestamp='2020-10-31T10:00:00Z')

		new_spend = 11300 # total balance of all points: 300 - 200 + 200 + 10000 + 1000 = 11300
		new_timestamp = '2022-01-31T10:00:00Z'
		new_spend_status = calculations.spend(int(new_spend),new_timestamp)
		new_balances = calculations.find_balances()

		for bal in new_balances:
			if bal['payer'] == 'DANNON':
				new_dannon_bal = bal['total']
			if bal['payer'] == 'UNILEVER':
				new_unilever_bal = bal['total']
			if bal['payer'] == 'MILLER COORS':
				new_millercoors_bal = bal['total']

		dannon_trans = Transaction.objects.get(id=6) # WARNING 'id's do not start from zero!
		unilever_trans = Transaction.objects.get(id=7)
		millercoors_trans = Transaction.objects.get(id=8)

		# test correct payer names
		self.assertEqual(dannon_trans.payer, 'DANNON')
		self.assertEqual(unilever_trans.payer, 'UNILEVER')
		self.assertEqual(millercoors_trans.payer, 'MILLER COORS')
		# test correct point amounts
		self.assertEqual(-abs(dannon_trans.points), -1100)
		self.assertEqual(-abs(unilever_trans.points), -200)
		self.assertEqual(-abs(millercoors_trans.points), -10000)
		# test correct timestamp
		self.assertEqual(dannon_trans.timestamp, '2022-01-31T10:00:00Z')
		self.assertEqual(unilever_trans.timestamp, '2022-01-31T10:00:00Z')
		self.assertEqual(millercoors_trans.timestamp, '2022-01-31T10:00:00Z')
		# test correct balances: all should be liquideated (i.e. "0")
		self.assertEqual(new_dannon_bal, 0)
		self.assertEqual(new_unilever_bal, 0)
		self.assertEqual(new_millercoors_bal, 0)
		
	def test_overspend(self):
		# Test to if the program rejects overspending points
		Transaction.objects.create(payer='DANNON',points=1000,timestamp='2020-11-02T14:00:00Z')
		Transaction.objects.create(payer='UNILEVER',points=200,timestamp='2020-10-31T11:00:00Z')
		Transaction.objects.create(payer='DANNON',points=-200,timestamp='2020-10-31T15:00:00Z')
		Transaction.objects.create(payer='MILLER COORS',points=10000,timestamp='2020-11-01T14:00:00Z')
		Transaction.objects.create(payer='DANNON',points=300,timestamp='2020-10-31T10:00:00Z')

		new_spend = 20000 # total balance of all points: 300 - 200 + 200 + 10000 + 1000 = 11300, this is overspending
		new_timestamp = '2022-01-31T10:00:00Z'
		new_spend_status = calculations.spend(int(new_spend),new_timestamp)
		new_balances = calculations.find_balances()

		for bal in new_balances:
			if bal['payer'] == 'DANNON':
				new_dannon_bal = bal['total']
			if bal['payer'] == 'UNILEVER':
				new_unilever_bal = bal['total']
			if bal['payer'] == 'MILLER COORS':
				new_millercoors_bal = bal['total']

		# test if new_spend_status == 'Error', which means the program successfully rejected the overspending attempt
		self.assertEqual(new_spend_status, 'Error!')

		# test correct balances, the balances should not have changed!
		self.assertEqual(new_dannon_bal, 1100) # 300 - 200 + 1000 = 1100
		self.assertEqual(new_unilever_bal, 200)
		self.assertEqual(new_millercoors_bal, 10000)

	def test_overspend_no_entries(self):
		# Test to if the program rejects overspending points with no previous entries entered

		new_spend = 5000
		new_timestamp = '2022-01-31T10:00:00Z'
		new_spend_status = calculations.spend(int(new_spend),new_timestamp)
		new_balances = calculations.find_balances()

		# test if new_spend_status == 'Error', which means the program successfully rejected the overspending attempt
		self.assertEqual(new_spend_status, 'Error!')

	def test_trans_after_one_liquidate(self):
		# Test to see how the program reacts a new transaction (gaining points) after that 'payer' was liquidated
		Transaction.objects.create(payer='DANNON',points=1000,timestamp='2020-11-02T14:00:00Z')
		Transaction.objects.create(payer='UNILEVER',points=200,timestamp='2020-10-31T11:00:00Z')
		Transaction.objects.create(payer='DANNON',points=-200,timestamp='2020-10-31T15:00:00Z')
		Transaction.objects.create(payer='MILLER COORS',points=10000,timestamp='2020-11-01T14:00:00Z')
		Transaction.objects.create(payer='DANNON',points=300,timestamp='2020-10-31T10:00:00Z')

		new_spend = 5000
		new_timestamp = '2022-01-31T10:00:00Z'
		new_spend_status = calculations.spend(int(new_spend),new_timestamp)

		# new transaction, UNILEVER was previously liqidated, so we attempt to bring it back!
		Transaction.objects.create(payer='UNILEVER',points=1000,timestamp='2022-02-31T10:00:00Z')

		new_balances = calculations.find_balances()

		for bal in new_balances:
			if bal['payer'] == 'DANNON':
				new_dannon_bal = bal['total']
			if bal['payer'] == 'UNILEVER':
				new_unilever_bal = bal['total']
			if bal['payer'] == 'MILLER COORS':
				new_millercoors_bal = bal['total']

		unilever_trans = Transaction.objects.get(id=9)

		# test correct payer names
		self.assertEqual(unilever_trans.payer, 'UNILEVER')
		# test correct transaction point amounts
		self.assertEqual(unilever_trans.points, 1000)
		# test correct timestamp
		self.assertEqual(unilever_trans.timestamp, '2022-02-31T10:00:00Z')
		# test correct balances
		self.assertEqual(new_dannon_bal, 1000) # 300 - 200 + 1000 - 100 = 0
		self.assertEqual(new_unilever_bal, 1000) # 200 - 200 + 1000 = 1000
		self.assertEqual(new_millercoors_bal, 5300) # 10000 - 4700 = 5300

	def test_trans_after_multiple_liquidate(self):
		# Test to see how the program reacts a new transaction (gaining points) after multiple 'payers' were liquidated
		Transaction.objects.create(payer='DANNON',points=1000,timestamp='2020-11-02T14:00:00Z')
		Transaction.objects.create(payer='UNILEVER',points=200,timestamp='2020-10-31T11:00:00Z')
		Transaction.objects.create(payer='DANNON',points=-200,timestamp='2020-10-31T15:00:00Z')
		Transaction.objects.create(payer='MILLER COORS',points=10000,timestamp='2020-11-01T14:00:00Z')
		Transaction.objects.create(payer='DANNON',points=300,timestamp='2020-10-31T10:00:00Z')

		new_spend = 10300 # UNILEVER and MILLER COORS get eliminated
		new_timestamp = '2022-01-31T10:00:00Z'
		new_spend_status = calculations.spend(int(new_spend),new_timestamp)
		new_balances = calculations.find_balances()

		# new transaction
		Transaction.objects.create(payer='UNILEVER',points=1000,timestamp='2022-02-31T10:00:00Z')
		Transaction.objects.create(payer='MILLER COORS',points=2000,timestamp='2022-03-01T14:00:00Z')

		for bal in new_balances:
			if bal['payer'] == 'DANNON':
				new_dannon_bal = bal['total']
			if bal['payer'] == 'UNILEVER':
				new_unilever_bal = bal['total']
			if bal['payer'] == 'MILLER COORS':
				new_millercoors_bal = bal['total']

		unilever_trans = Transaction.objects.get(id=9)
		millercoors_trans = Transaction.objects.get(id=10)

		# test correct payer names
		self.assertEqual(unilever_trans.payer, 'UNILEVER')
		self.assertEqual(millercoors_trans.payer, 'MILLER COORS')
		# test correct transaction point amounts
		self.assertEqual(unilever_trans.points, 1000)
		self.assertEqual(millercoors_trans.points, 2000)
		# test correct timestamp
		self.assertEqual(unilever_trans.timestamp, '2022-02-31T10:00:00Z')
		self.assertEqual(millercoors_trans.timestamp, '2022-03-01T14:00:00Z')
		# test correct balances
		self.assertEqual(new_dannon_bal, 1000) # 300 - 200 + 1000 - 100 = 1000
		self.assertEqual(new_unilever_bal, 1000) # 200 - 200 + 1000 = 1000
		self.assertEqual(new_millercoors_bal, 2000) # 10000 - 10000 + 2000 = 2000

	def test_trans_after_all_liquidate(self):
		# Test to see how the program reacts a new transaction (gaining points) after all 'payers' were liquidated
		Transaction.objects.create(payer='DANNON',points=1000,timestamp='2020-11-02T14:00:00Z')
		Transaction.objects.create(payer='UNILEVER',points=200,timestamp='2020-10-31T11:00:00Z')
		Transaction.objects.create(payer='DANNON',points=-200,timestamp='2020-10-31T15:00:00Z')
		Transaction.objects.create(payer='MILLER COORS',points=10000,timestamp='2020-11-01T14:00:00Z')
		Transaction.objects.create(payer='DANNON',points=300,timestamp='2020-10-31T10:00:00Z')

		new_spend = 11300 # total balance of all points: 300 - 200 + 200 + 10000 + 1000 = 11300
		new_timestamp = '2022-01-31T10:00:00Z'
		new_spend_status = calculations.spend(int(new_spend),new_timestamp)
		new_balances = calculations.find_balances()

		# new transactions, re-seed all the payers
		Transaction.objects.create(payer='DANNON',points=2000,timestamp='2022-02-02T14:00:00Z')
		Transaction.objects.create(payer='UNILEVER',points=3000,timestamp='2022-02-31T10:00:00Z')
		Transaction.objects.create(payer='MILLER COORS',points=4000,timestamp='2022-03-01T14:00:00Z')

		for bal in new_balances:
			if bal['payer'] == 'DANNON':
				new_dannon_bal = bal['total']
			if bal['payer'] == 'UNILEVER':
				new_unilever_bal = bal['total']
			if bal['payer'] == 'MILLER COORS':
				new_millercoors_bal = bal['total']

		dannon_trans = Transaction.objects.get(id=9)
		unilever_trans = Transaction.objects.get(id=10)
		millercoors_trans = Transaction.objects.get(id=11)

		# test correct payer names
		self.assertEqual(dannon_trans.payer, 'DANNON')
		self.assertEqual(unilever_trans.payer, 'UNILEVER')
		self.assertEqual(millercoors_trans.payer, 'MILLER COORS')

		# test correct transaction point amounts
		self.assertEqual(dannon_trans.points, 2000)
		self.assertEqual(unilever_trans.points, 3000)
		self.assertEqual(millercoors_trans.points, 4000)
		# test correct timestamp
		self.assertEqual(dannon_trans.timestamp, '2022-02-02T14:00:00Z')
		self.assertEqual(unilever_trans.timestamp, '2022-02-31T10:00:00Z')
		self.assertEqual(millercoors_trans.timestamp, '2022-03-01T14:00:00Z')
		# test correct balances
		self.assertEqual(new_dannon_bal, 2000) # 300 - 200 + 1000 - 1100 + 2000 = 0
		self.assertEqual(new_unilever_bal, 3000) # 200 - 200 + 3000 = 3000
		self.assertEqual(new_millercoors_bal, 4000) # 10000 - 10000 + 4000 = 4000

	def test_multiple_trans_and_spend(self):
		# Test to see how the program multiple (3) transactions (gaining points) and multiple (3) spending attempts
		Transaction.objects.create(payer='DANNON',points=1000,timestamp='2020-11-02T14:00:00Z')
		Transaction.objects.create(payer='UNILEVER',points=200,timestamp='2020-10-31T11:00:00Z')
		Transaction.objects.create(payer='DANNON',points=-200,timestamp='2020-10-31T15:00:00Z')
		Transaction.objects.create(payer='MILLER COORS',points=10000,timestamp='2020-11-01T14:00:00Z')
		Transaction.objects.create(payer='DANNON',points=300,timestamp='2020-10-31T10:00:00Z')

		new_spend_1 = 5000
		new_timestamp_1 = '2022-01-31T10:00:00Z'
		new_spend_status_1 = calculations.spend(int(new_spend_1),new_timestamp_1)

		Transaction.objects.create(payer='DANNON',points=2000,timestamp='2022-02-02T14:00:00Z')

		new_spend_2 = 2500
		new_timestamp_2 = '2022-02-03T10:00:00Z'
		new_spend_status_2 = calculations.spend(int(new_spend_2),new_timestamp_2)

		new_spend_3 = 4000
		new_timestamp_3 = '2022-02-23T10:00:00Z'
		new_spend_status_3 = calculations.spend(int(new_spend_3),new_timestamp_3)

		Transaction.objects.create(payer='UNILEVER',points=3000,timestamp='2022-02-31T11:00:00Z')
		Transaction.objects.create(payer='MILLER COORS',points=4000,timestamp='2022-03-01T14:00:00Z')


		new_balances = calculations.find_balances()

		for bal in new_balances:
			if bal['payer'] == 'DANNON':
				new_dannon_bal = bal['total']
			if bal['payer'] == 'UNILEVER':
				new_unilever_bal = bal['total']
			if bal['payer'] == 'MILLER COORS':
				new_millercoors_bal = bal['total']

		# 1st OG transaction/spend
		dannon_trans_1 = Transaction.objects.get(id=6) # WARNING 'id's do not start from zero!
		unilever_trans_1 = Transaction.objects.get(id=7)
		millercoors_trans_1 = Transaction.objects.get(id=8)

		# 2nd transaction
		dannon_trans_2 = Transaction.objects.get(id=9)

		# 2nd spend
		millercoors_trans_2 = Transaction.objects.get(id=10)

		# 3rd spend
		millercoors_trans_3 = Transaction.objects.get(id=11)
		dannon_trans_3 = Transaction.objects.get(id=12)

		# 3rd transaction
		unilever_trans_2 = Transaction.objects.get(id=13)
		millercoors_trans_4 = Transaction.objects.get(id=14)


		# test correct payer names
		self.assertEqual(dannon_trans_1.payer, 'DANNON')
		self.assertEqual(unilever_trans_1.payer, 'UNILEVER')
		self.assertEqual(millercoors_trans_1.payer, 'MILLER COORS')
		self.assertEqual(dannon_trans_2.payer, 'DANNON')
		self.assertEqual(millercoors_trans_2.payer, 'MILLER COORS')
		self.assertEqual(millercoors_trans_3.payer, 'MILLER COORS')
		self.assertEqual(dannon_trans_3.payer, 'DANNON')
		self.assertEqual(unilever_trans_2.payer, 'UNILEVER')
		self.assertEqual(millercoors_trans_4.payer, 'MILLER COORS')
		# test correct point amounts
		self.assertEqual(-abs(dannon_trans_1.points), -100)
		self.assertEqual(-abs(unilever_trans_1.points), -200)
		self.assertEqual(-abs(millercoors_trans_1.points), -4700)
		self.assertEqual(dannon_trans_2.points, 2000)
		self.assertEqual(-abs(millercoors_trans_2.points), -2500)
		self.assertEqual(-abs(millercoors_trans_3.points), -2800)
		self.assertEqual(-abs(dannon_trans_3.points), -1200)
		self.assertEqual(unilever_trans_2.points, 3000)
		self.assertEqual(millercoors_trans_4.points, 4000)
		# test correct timestamp
		self.assertEqual(dannon_trans_1.timestamp, '2022-01-31T10:00:00Z')
		self.assertEqual(unilever_trans_1.timestamp, '2022-01-31T10:00:00Z')
		self.assertEqual(millercoors_trans_1.timestamp, '2022-01-31T10:00:00Z')
		self.assertEqual(dannon_trans_2.timestamp, '2022-02-02T14:00:00Z')
		self.assertEqual(millercoors_trans_2.timestamp, '2022-02-03T10:00:00Z')
		self.assertEqual(millercoors_trans_3.timestamp, '2022-02-23T10:00:00Z')
		self.assertEqual(dannon_trans_3.timestamp, '2022-02-23T10:00:00Z')
		self.assertEqual(unilever_trans_2.timestamp, '2022-02-31T11:00:00Z')
		self.assertEqual(millercoors_trans_4.timestamp, '2022-03-01T14:00:00Z')
		# test correct balances
		self.assertEqual(new_dannon_bal, 1800) # 300 - 200 + 1000 - 100 + 2000 - 1200 = 1800
		self.assertEqual(new_unilever_bal, 3000) # 200 - 200 + 3000 = 3000
		self.assertEqual(new_millercoors_bal, 4000) # 10000 - 4700 - 2500 - 2800 + 4000 = 4000