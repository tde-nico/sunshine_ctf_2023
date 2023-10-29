ct = 'bGVnbGxpaGVwaWNrdD8Ka2V0ZXRpZGls'
o = [5, 1, 3, 4, 7, 2, 6, 0]

chunks = [ct[i:i+4] for i in range(0, len(ct), 4)]
print(chunks)

flag = ''
for i in range(len(o)):
	index = o.index(i)
	flag += chunks[index]

flag = f'sun{{{flag}}}'
print(flag)

# sun{ZGlsbGxpa2V0aGVwaWNrbGVnZXRpdD8K}
