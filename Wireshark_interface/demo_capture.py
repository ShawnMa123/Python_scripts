import pyshark

capture = pyshark.LiveCapture(interface='WLAN')
capture.sniff(packet_count=2)

for pkt in capture:
    print(pkt)