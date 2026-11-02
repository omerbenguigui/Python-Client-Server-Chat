"""Terminal client for the newline-delimited TCP chat protocol."""

import argparse
import socket
import threading

SERVER_IP = "127.0.0.1"
PORT = 50000


def encode_message(message: str) -> bytes:
    """Normalize only the command, preserving usernames and message text."""
    if message.startswith("/"):
        command, separator, arguments = message[1:].partition(" ")
        message = command.upper() + separator + arguments
    else:
        message = "ALL " + message
    return (message + "\n").encode("utf-8")


def recv_loop(sock, disconnected):
    try:
        buffer = b""
        while True:
            data = sock.recv(4096)
            if not data:
                print("[Disconnected]")
                break

            buffer += data
            while b"\n" in buffer:
                line, buffer = buffer.split(b"\n", 1)
                if line.strip():
                    print(line.decode("utf-8", errors="replace").strip())
    except OSError as exc:
        if not disconnected.is_set():
            print(f"Receive failed: {exc}")
    finally:
        disconnected.set()
        print("[Press Enter to exit]")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--host", default=SERVER_IP, help="Server address (default: 127.0.0.1)"
    )
    parser.add_argument(
        "--port", type=int, default=PORT, help="Server port (default: 50000)"
    )
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("--port must be between 1 and 65535")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    disconnected = threading.Event()

    try:
        sock.settimeout(10)
        sock.connect((args.host, args.port))
        sock.settimeout(None)
        print("Connected to server")
    except OSError as e:
        print("Connection failed:", e)
        sock.close()
        return

    try:
        username = input("Enter username: ").strip()
        if not username or len(username) > 20 or any(c.isspace() for c in username):
            print("Username must contain 1-20 characters without whitespace.")
            return
        sock.sendall(f"LOGIN {username}\n".encode())
        threading.Thread(
            target=recv_loop, args=(sock, disconnected), daemon=True
        ).start()
        while not disconnected.is_set():
            msg = input()
            if disconnected.is_set():
                break
            if not msg:
                continue
            payload = encode_message(msg)
            sock.sendall(payload)
            if payload.strip() == b"QUIT":
                break
    except (KeyboardInterrupt, EOFError):
        print("\nClosing chat.")
    except OSError as exc:
        print(f"Connection error: {exc}")
    finally:
        disconnected.set()
        try:
            sock.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        sock.close()


if __name__ == "__main__":
    main()
