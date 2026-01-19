import socket


def find_available_port(start_port: int, end_port: int):
    for port in range(start_port, end_port + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(("localhost", port))
                return port
        except OSError:
            continue
    raise Exception(f"No available port in range {start_port} - {end_port}")
