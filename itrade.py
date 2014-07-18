## Coded by Rojer97
### Want to join the game?? Register now! http://www.erepublik.com/en/referrer/Rojer97
# (please do register with the above link xD)
## Check me on eRepublik: http://www.erepublik.com/en/citizen/profile/6328829

import hashlib
import json
import argparse
import datetime
from time import sleep

VERSION = "1.0 Beta"

print("Welcome!!")
sleep(0.5)
print("""  _ _____              _           
 (_)_   _| __ __ _  __| | ___ _ __ 
 | | | || '__/ _` |/ _` |/ _ \ '__|
 | | | || | | (_| | (_| |  __/ |   
 |_| |_||_|  \__,_|\__,_|\___|_|   
                                   """)
#ASCII artwork @ http://patorjk.com/software/taag/#p=display&f=Standard&t=iTrader
print("Version {}".format(VERSION))
print("This nice program was brought to you by Rojer97!")
print("A donation of 1 gold would be enough to motivate me to keep improving this program!")
sleep(5)
input("hit return to start")

PROMPT = "iTrader(beta)$ "

def DEBUG(g, l, e):
	'''Debugging function to be called when errors were expected.
	Receives as arguments the locals() and globals() of the scope in which the
error was to be raised, just as the error. The error gets printed and a loop
runs until the debugger exits with \'exit(X)\''''
	# <g> and <l> are both the globals and locals from which the debugging
	#function was called! This lets me play around with the problems
	print("You just entered the debugger")
	print("The error that took you here was:")
	print(e)
	print("#"*40)
	while True:
		try:
			exec(input("[debugger] > "), g, l)
		except Exception as error:
			print("[Error...]")
			print(error)

def SAVE(file_name, data):
	try:
		with open(file_name, "w") as f:
			json.dump(data, f, sort_keys=True, indent=8)
	except Exception as e:
		print("Error while saving:")
		print(e)
		return False
	return True

def LOAD(file_name):
	try:
		with open(file_name, "r") as f:
			unparsed_data = f.read()
	except IOError:
		print("Could not load data.")
		return False
	try:
		data = json.loads(unparsed_data)
	except Exception as e:
		print("Error loading data...")
		print(file_name)
		DEBUG(globals(), locals(), e)
	return data
		
def LOG(file_name, data):
	try:
		with open(file_name, "a") as f:
			f.write(str(data))
	except IOError:
		print("Could not open logging file.")
		return False
	return True
	
main_parser = argparse.ArgumentParser()

main_parser.add_argument("action", help="Define the action to execute. Type <help> for a complete help.",
			choices=["trade", "register", "calc", "exit", "print", "check",
				"search", "help", "log", "convert"], metavar="action")
main_parser.add_argument("args", nargs=argparse.REMAINDER, metavar="arguments",
						help="The arguments for the action")

FILE_INFO = "itrade.data"
FILE_LOG = "itrade_trades.log"
FILE_TRADERS = "itrade_traders.data"

itrade_info = LOAD(FILE_INFO)
if itrade_info == False:
	del itrade_info
	itrade_info = dict()
	open(FILE_INFO, "w").close()
	print("Type in your name:")
	name = input(PROMPT)
	itrade_info["name"] = name
	itrade_info["stock"] = {}
	itrade_info["profit"] = 0
	success = SAVE(FILE_INFO, itrade_info)
	if not(success):
		print("Problem saving...")
		DEBUG(globals(), locals(), "")
	
traders = LOAD(FILE_TRADERS)
if traders == False:
	traders = {}
	open(FILE_TRADERS, "w").close()
	success = SAVE(FILE_TRADERS, traders)
	if not(success):
		print("Problem saving the traders...")
		print(globals(), locals(), "")
				
d = {"buy": ["bought", "spending"], "sell": ["sold", "gaining"]}
items = {"wq6": "Weapons Q6", "wq7": "Weapons Q7", "wq5": "Weapons Q5", "wq4": "Weapons Q4",
	"wq3": "Weapons Q3", "wq2": "Weapons Q2", "wq1": "Weapons Q1", "fq1": "Food Q1",
	"fq2": "Food Q2", "fq3": "Food Q3", "fq4": "Food Q4", "fq5": "Food Q5", "fq6": "Food Q6",
	"fq7": "Food Q7", "wrm": "Weapon Raw Material", "frm": "Food Raw Material", "gold": "Gold"}
						
while True:
	inp = input(PROMPT).split()
	try:
		data = main_parser.parse_args(inp)
	except SystemExit:
		continue
		
	if data.action == "help":
		print("<action> explanation:")
		print("<calc> does simple maths. +-*/^ are the operators.")
		print("<search> searches for the given keyword(s) in the traders database.")
		print("<check> checks if a given ID is registered.")
		print("<print> either prints your stock or a given IDs information.")
		print("<trade> logs a trade and computes stock/profit.")
		print("<info> registers an ID or updates it.")
		print("<convert> \"transforms\" profit CC into gold.")
		print("For a more comprehensive help in each command you can type <command> <-h>")
	
	elif data.action == "calc":
		print(eval("".join(data.args)))
		
	elif data.action == "exit":
		SAVE(FILE_TRADERS, traders)
		SAVE(FILE_INFO, itrade_info)
		import sys
		sys.exit(0)
		
	elif data.action == "convert":
		convert_parser = argparse.ArgumentParser()
		convert_parser.add_argument("gold", type=int, help="Amount of gold "\
			"bought.", metavar="gold")
		convert_parser.add_argument("cc", type=float, help="Amount of cc "\
			"converted into gold.", metavar="CC")
		
		try:
			data = convert_parser.parse_args(data.args)
		except SystemExit:
			continue
			
		itrade_info["profit"] -= data.cc
		itrade_info["stock"]["gold"] += data.gold
		
		print("Converted {}cc into {} gold.".format(data.cc, data.gold))
		
	elif data.action == "log":
		log_parser = argparse.ArgumentParser()
		log_parser.add_argument("n", help="Number of logs to show.", metavar="N")
		
		try:
			data = log_parser.parse_args(data.args)
		except SystemExit:
			continue
			
		data.n = data.n.lower()
		if data.n == "all":
			with open(FILE_LOG, "r") as f:
				reads = f.read()
			print(reads)
		else:
			try:
				n = int(data.n)
			except ValueError:
				print("***\tN has to be a number or <all>")
				continue
			with open(FILE_LOG, "r") as f:
				reads = f.read()
			logs = reads.split("Registered ")[1:]
			n = -1*n
			if abs(n) >= len(logs):
				print(reads)
			elif n < 0:
				if abs(n) >= len(logs):
					for log in logs[::-1]:
						print(log)
				else:
					for i in range(1, abs(n)+1):
						print(logs[-i])
			else:
				for i in range(n):
					print(logs[i])
		
	elif data.action == "search":
		crit = " ".join(data.args).lower()
		for key in traders.keys():
			# do specific search for +v users
			if crit=="voice":
				if traders[key]["voice"] == "True":
					print("* match found: ({}) {}".format(key, traders[key]["nick"]))
			else:
				info = key+traders[key]["nick"]+traders[key]["irc"]+traders[key]["info"]
				if crit in info.lower():
					print("* match found: ({}) {}".format(key, traders[key]["nick"]))
		
	elif data.action == "print":
		print_parser = argparse.ArgumentParser()
		print_parser.add_argument("player", nargs="*", metavar="player",
			help="Type the player ID/name to search for")
			
		try:
			data = print_parser.parse_args(data.args)
		except SystemExit:
			continue
			
		if data.player != []:
			try:
				int(data.player[0])
				is_n = True
			except ValueError:
				is_n = False
			if is_n:
				if data.player[0] not in traders.keys():
					print("***\tUnregistered ID.")
					continue
				else:
					print("{}".format(json.dumps(traders[data.player[0]], indent=4)[2:-2]))
			else:
				print("***\tID must be a ~7-digit long number.")
		else:
			print("Stocks:")
			for key in itrade_info["stock"]:
				if itrade_info["stock"][key] != 0:
					print("\t"+items[key]+": "+str(itrade_info["stock"][key]))
			print("Overall profit = {}cc.".format(itrade_info["profit"]))
		
	elif data.action == "check":
		check_parser = argparse.ArgumentParser()
		check_parser.add_argument("id_number", metavar="id", help="ID to check.")
	   
		try:
			data = check_parser.parse_args(data.args)
		except SystemExit:
			continue
		
		if data.id_number in traders.keys():
			print("Registered ID: {}".format(traders[data.id_number]["nick"]))
		else:
			print("***\tUnregistered ID.")
		
	elif data.action == "trade":
		trade_parser = argparse.ArgumentParser()
		trade_parser.add_argument("transaction", metavar="transaction", 
help="The type of transaction. [buy | sell]", choices = ["buy", "sell"])
		trade_parser.add_argument("id_number", metavar="id", help="The id of "\
			"the player with whom you traded.")
		trade_parser.add_argument("item", metavar="item", help="The item that "\
			"was traded.")
		trade_parser.add_argument("amount", metavar="amount", help="The amount"\
			" that was traded.", type=int)
		trade_parser.add_argument("price", metavar="price", help="The total "\
			"price paid for those items.", type=float)
		
		try:
			data = trade_parser.parse_args(data.args)
		except SystemExit:
			continue
		if data.transaction == "buy":
			itrade_info["profit"] -= data.price
			itrade_info["stock"][data.item] += data.amount
		else:
			itrade_info["profit"] += data.price
			itrade_info["stock"][data.item] -= data.amount
			if itrade_info["stock"][data.item] <= 0:
				print("***\tYou are out of stock of "+items[data.item]+" !!")
				print("Your current stock is " + str(itrade_info["stock"][data.item]))
		if data.id_number in traders.keys():
			print("***\tKnown trader: " + traders[data.id_number]["nick"])
			know = "a registered"
			other = data.id_number + " ("+traders[data.id_number]["nick"]+")"
		else:
			print("***\tUnknown trader with id " + data.id_number)
			know = "an unregistered"
			other = data.id_number
			
		s = """Registered transaction between ${my_name}$ and ${other}$ at {time}
	{act} {amount:,g} {item} for the total price of {money:,g}.
	This gives a rate of {r:.3f} / each piece.
	The transaction was made with {know} trader in our database.
	After this, your "{item}" stock is {stock:,g} and you have an overall profit of {profit:,g}cc\n\n""".format(
			act=d[data.transaction][0].capitalize(), amount=data.amount, item=items[data.item],
			r=data.price/data.amount, idn=data.id_number, act2=d[data.transaction][1],
			money=data.price, my_name=itrade_info["name"], stock=itrade_info["stock"][data.item],
			profit=itrade_info["profit"], know=know, time=str(datetime.datetime.now())[:-7], other=other)

		LOG(FILE_LOG, s)
		print(s[:-1])
		SAVE(FILE_INFO, itrade_info)
	  
	elif data.action == "register":
		info_parser = argparse.ArgumentParser()
		info_parser.add_argument("id_number", metavar="id_number", help="The "\
			"id of the trader.")
		info_parser.add_argument("nick", metavar="nick", help="The trader's "\
			"eRepublik nick.", nargs="+")
		info_parser.add_argument("-n", "--nick", metavar="irc", help="The nick "\
			"in IRC.", nargs=1, dest="irc", default="-")
		info_parser.add_argument("-u", metavar="update", dest="u", const=True,
			default=False, action="store_const", help="Update switch.")
		info_parser.add_argument("-i", "--info", metavar="info", dest="info",
			help="Additional info about the trader.", nargs="+", default="")
		info_parser.add_argument("-v", metavar="voice", dest="v", help="Flag "\
			"if trader has voice in #itrade.", const="True", default="False",
			action="store_const")
			
		try:
			data = info_parser.parse_args(data.args)
		except SystemExit:
			continue
			
		if data.id_number in traders.keys():
			if data.u:
				traders[data.id_number] = {"nick": " ".join(data.nick), "info": 
					" ".join(data.info), "irc": " ".join(data.irc), "voice":data.v}
				print("***\tID registered.""")
			else:
				print("***\tYou already registered that ID.")
				print("To update use the update switch.")
		else:
			traders[data.id_number] = {"nick": " ".join(data.nick), "info": 
					" ".join(data.info), "irc": " ".join(data.irc), "voice":data.v}
			print("***\tID registered.""")
			
		SAVE(FILE_TRADERS, traders)
