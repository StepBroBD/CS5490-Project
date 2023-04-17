import scapy.all as scapy


def sniff(iface: str, host: str, port: int) -> None:
    scapy.sniff(
        iface=[],
        prn=lambda x: x.show(),
    )
