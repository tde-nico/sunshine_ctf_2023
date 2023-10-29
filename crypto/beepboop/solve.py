import codecs

with open('./BeepBoop.txt', 'r') as f:
	text = f.read()

text = text.replace('beep', '0').replace('boop', '1').replace(' ', '')

ct = int(text, 2)

rot = ct.to_bytes(41, 'big')[1:]

m = codecs.encode(rot.decode(), 'rot_13')

print(m)

# sun{exterminate-exterminate-exterminate}
