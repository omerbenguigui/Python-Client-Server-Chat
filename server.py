"""Threaded TCP chat server for local and explicitly configured LAN demos."""

import argparse
import logging
import socket
import threading

HOST = "127.0.0.1"
PORT = 50000
logger = logging.getLogger(__name__)

# Active clients: username -> socket
clients = {}
clients_lock = threading.Lock()


def safe_send(sock: socket.socket, text: str) -> bool:
    """Return True if sent, False if failed."""
    try:
        sock.sendall(text.encode("utf-8"))
        return True
    except OSError:
        return False


def send_to_user(username: str, text: str) -> bool:
    with clients_lock:
        sock = clients.get(username)
    if not sock:
        return False
    return safe_send(sock, text)


def broadcast(text: str, exclude: str | None = None) -> None:
    """Send to everyone, optionally excluding a username."""
    with clients_lock:
        items = list(clients.items())

    dead = []
    for name, sock in items:
        if exclude is not None and name == exclude:
            continue
        if not safe_send(sock, text):
            dead.append((name, sock))

    if dead:
        with clients_lock:
            for name, failed_socket in dead:
                if clients.get(name) is failed_socket:
                    try:
                        clients[name].close()
                    except OSError:
                        pass
                    del clients[name]


def build_user_list() -> str:
    with clients_lock:
        names = sorted(clients.keys(), key=lambda s: s.lower())
    return ", ".join(names) if names else "None"


def cleanup_user(username: str, conn: socket.socket) -> None:
    with clients_lock:
        registered = clients.get(username) is conn
        if registered:
            del clients[username]
    conn.close()
    if registered:
        broadcast(f"SYS USER_LEFT {username}\n")
        broadcast(f"SYS ONLINE {build_user_list()}\n")


def handle_client(conn: socket.socket, addr):
    username = None
    try:
        conn.settimeout(60)

        safe_send(conn, "SYS WELCOME\n")
        safe_send(
            conn,
            "SYS PROTOCOL Commands: LOGIN <name> | LIST | ALL <msg> | DM <name> <msg> | QUIT\n",
        )
        safe_send(
            conn, "SYS TIP In client you can type: /all hi, /dm Bob hi, /list, /quit\n"
        )

        buffer = b""
        while True:
            chunk = conn.recv(4096)
            if not chunk:
                break
            buffer += chunk

            while b"\n" in buffer:
                raw_line, buffer = buffer.split(b"\n", 1)
                line = raw_line.decode("utf-8", errors="replace").strip()
                if not line:
                    continue

                parts = line.split(" ", 2)
                cmd = parts[0].upper()

                if cmd == "LOGIN":
                    if username is not None:
                        safe_send(conn, "ERR Already logged in\n")
                        continue
                    if len(parts) != 2:
                        safe_send(conn, "ERR Usage: LOGIN <name>\n")
                        continue

                    requested = parts[1].strip()
                    if (
                        not requested
                        or len(requested) > 20
                        or any(c.isspace() for c in requested)
                    ):
                        safe_send(
                            conn, "ERR Invalid username (1-20 chars, no spaces)\n"
                        )
                        continue

                    with clients_lock:
                        if requested in clients:
                            safe_send(conn, "ERR Username taken\n")
                            continue
                        clients[requested] = conn
                        username = requested

                    conn.settimeout(None)  # after login, no timeout
                    safe_send(conn, f"OK Logged in as {username}\n")
                    broadcast(f"SYS USER_JOINED {username}\n")
                    broadcast(f"SYS ONLINE {build_user_list()}\n")
                    continue

                # All other commands require login
                if username is None:
                    safe_send(conn, "ERR Please LOGIN first\n")
                    continue

                if cmd == "LIST":
                    safe_send(conn, f"SYS ONLINE {build_user_list()}\n")

                elif cmd == "ALL":
                    if len(parts) < 2:
                        safe_send(conn, "ERR Usage: ALL <message>\n")
                        continue
                    msg = line[len("ALL ") :].strip()
                    if not msg:
                        safe_send(conn, "ERR Empty message\n")
                        continue
                    broadcast(f"MSG GROUP {username} {msg}\n")

                elif cmd == "DM":
                    # DM <name> <message>
                    if len(parts) < 3:
                        safe_send(conn, "ERR Usage: DM <name> <message>\n")
                        continue
                    target = parts[1].strip()
                    msg = parts[2].strip()
                    if not msg:
                        safe_send(conn, "ERR Empty message\n")
                        continue

                    if target == username:
                        safe_send(conn, "ERR Cannot DM yourself\n")
                        continue

                    if send_to_user(target, f"MSG DM {username} {msg}\n"):
                        safe_send(conn, f"OK Sent to {target}\n")
                    else:
                        safe_send(conn, f"ERR User not found: {target}\n")

                elif cmd == "QUIT":
                    safe_send(conn, "SYS BYE\n")
                    return

                else:
                    safe_send(conn, "ERR Unknown command. Use LIST | ALL | DM | QUIT\n")

    except OSError as exc:
        logger.info("Connection %s closed: %s", addr, exc)
    finally:
        if username is not None:
            cleanup_user(username, conn)
        else:
            try:
                conn.close()
            except OSError:
                pass


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--host", default=HOST, help="Bind address (default: 127.0.0.1)"
    )
    parser.add_argument(
        "--port", type=int, default=PORT, help="Listen port (default: 50000)"
    )
    args = parser.parse_args()
    if not 1 <= args.port <= 65535:
        parser.error("--port must be between 1 and 65535")
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((args.host, args.port))
    server_socket.listen(10)

    print("======================================")
    print(f" SERVER RUNNING ON {args.host}:{args.port}")
    print("======================================")

    try:
        while True:
            conn, addr = server_socket.accept()
            t = threading.Thread(target=handle_client, args=(conn, addr), daemon=True)
            t.start()
    except KeyboardInterrupt:
        print("\nStopping server.")
    finally:
        server_socket.close()


if __name__ == "__main__":
    main()
