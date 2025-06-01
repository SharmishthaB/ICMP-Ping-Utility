import tkinter as tk
from tkinter import messagebox
import socket
import struct
import os
import time

class PingUtility:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("ICMP Based Ping Utility")

        self.root.configure(bg="#1A1D23")  
        self.entry_color = "#2B2F3B"  
        self.button_color = "#34C759"  
        self.text_color = "#00FF00"  

        tk.Label(self.root, text="Hostname/IP Address:", bg="#1A1D23", fg=self.text_color, font=("Consolas", 12)).grid(row=0, column=0, sticky="ew")
        self.hostname_entry = tk.Entry(self.root, bg=self.entry_color, fg=self.text_color, font=("Consolas", 12), insertbackground=self.text_color)
        self.hostname_entry.grid(row=0, column=1, sticky="ew")

      
        tk.Button(self.root, text="Start Ping", command=self.start_ping, bg=self.button_color, fg="#1A1D23", font=("Consolas", 12)).grid(row=1, column=0, columnspan=2, sticky="ew")

        
        self.result_text = tk.Text(self.root, bg=self.entry_color, fg=self.text_color, font=("Consolas", 12), insertbackground=self.text_color)
        self.result_text.grid(row=2, column=0, columnspan=2, sticky="nsew")

        self.root.grid_rowconfigure(0, weight=0)
        self.root.grid_rowconfigure(1, weight=0)
        self.root.grid_rowconfigure(2, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

    def start_ping(self):
        hostname = self.hostname_entry.get()
        if not hostname:
            messagebox.showerror("Error", "Please enter a hostname/IP address")
            return

        try:
            ip = socket.gethostbyname(hostname)
        except socket.gaierror:
            messagebox.showerror("Error", "Invalid hostname/IP address")
            return

        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, f"ICMP Based Pinging {hostname} ({ip})\n")

        num_packets = 4
        successes = 0
        rtts = []

        for seq in range(num_packets):
            packet = self.create_packet(seq)
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            sock.sendto(packet, (ip, 1))
            start_time = time.time()
            sock.settimeout(1)
            try:
                data, addr = sock.recvfrom(1024)
                end_time = time.time()
                rtt = (end_time - start_time) * 1000
                self.result_text.insert(tk.END, f"Reply from {ip}: icmp_seq={seq} bytes={len(data)} time={rtt:.2f} ms\n")
                successes += 1
                rtts.append(rtt)
            except socket.timeout:
                self.result_text.insert(tk.END, f"Request timed out.\n")
            sock.close()

        self.result_text.insert(tk.END, f"\nPing statistics for {ip}:\n")
        self.result_text.insert(tk.END, f"Packets: Sent = {num_packets}, Received = {successes}, Lost = {num_packets - successes} ({(num_packets - successes) / num_packets * 100:.0f}% loss)\n")
        if rtts:
            self.result_text.insert(tk.END, f"Approximate round trip times in milli-seconds:\n")
            self.result_text.insert(tk.END, f"Minimum = {min(rtts):.2f}ms, Maximum = {max(rtts):.2f}ms, Average = {sum(rtts) / len(rtts):.2f}ms\n")

    def create_packet(self, seq):
        packet_id = os.getpid() & 0xFFFF
        header = struct.pack("!BBHHH", 8, 0, 0, packet_id, seq)
        payload = bytes([x & 0xff for x in range(56)])
        checksum_val = self.checksum(header + payload)
        header = struct.pack("!BBHHH", 8, 0, checksum_val, packet_id, seq)
        return header + payload

    def checksum(self, data):
        s = sum((data[i] << 8) + data[i+1] for i in range(0, len(data)-1, 2))
        if len(data) % 2:
            s += data[-1] << 8
        s = (s >> 16) + (s & 0xffff)
        s += (s >> 16)
        return ~s & 0xffff

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    ping_utility = PingUtility()
    ping_utility.run()