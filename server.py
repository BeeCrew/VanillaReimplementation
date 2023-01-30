"""
A vanilla reimplementation made using BeeMineAPI.
This should NOT be used in Production.
It is not complete.
"""
from beemineapi import BeeProtocol, BeeFactory, BeeAPI, reactor
import sys
true, false = True, False
c = '§'
beeapi = BeeAPI()
allowed_protocols = [759, 760, 761]

def exit(exit_code: int=0):
	try:
		sys.exit(exit_code)
	except:
		quit()

def packet_chat_message(self, buff):
	p_text = buff.unpack_string()
	fmt = f"<{self.display_name}> {p_text}"
	print(f'[CHAT] {fmt}')
	beeapi.sendMessage(fmt)
	buff.discard()

def getHelpMsg():
	return f"{c}cThis is a placeholder."

def packet_chat_command(self, buff):
	command = buff.unpack_string()
	commands = command.split()
	cmd = commands[0]
	args = commands
	args.remove(cmd)
	returned = 0
	if cmd == "help":
		beeapi.sendMessage(getHelpMsg(), self)
		returned = 1
	elif cmd == "eval":
		beeapi.sendMessage(f'{c}7Executing...', self)
		executes = ''
		for arg in args:
			executes += f' {arg}'
		try:
			got = eval(executes)
		except Exception as e:
			exname = str(type(e)).replace(' ', '').replace('<', '>').replace('>', '').replace('class', '').replace('\'', '')
			beeapi.sendMessage(f'{c}c{exname}: {e}', self)
		returned = 1
	else:
		beeapi.sendMessage(f'{c}cInvalid Command! Use /help for help.', self)
		returned = 1
	if returned == 1:
		print(f"{self.displayname} executed command: {command}")
	buff.discard()

def getBadVersionKick(version: int):
	return f"Minecraft Protocol {version} is not allowed."

def player_joined(self):
	super().player_joined()
	if not self.protocol_version in allowed_protocols:
		self.close(getBadVersionKick(self.protocol_version))

class VanillaFactory(BeeFactory):
	protocol = BeeProtocol
	motd = f'A Minecraft Server\n{c}eBeeMineAPI Vanilla Reimplementation'
	icon_path = "./server.png"
	protocol.player_joined = player_joined
	protocol.packet_chat_message = packet_chat_message
	protocol.packet_chat_command = packet_chat_command

try:
	factory = VanillaFactory()
	host, port="", 25565
	addr=(host, port)
	beeapi = BeeAPI(factory)
	factory.listen(*addr)
	reactor.run()
except Exception as e:
	exit()