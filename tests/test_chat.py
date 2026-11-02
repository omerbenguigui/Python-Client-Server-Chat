import contextlib
import io
import socket
import threading
import unittest

import client
import server


class Peer:
    def __init__(self):
        self.sock, connection = socket.socketpair()
        self.sock.settimeout(2)
        self.buffer = b""
        self.thread = threading.Thread(
            target=server.handle_client, args=(connection, "test")
        )
        self.thread.start()
        self.until("SYS TIP")

    def send(self, text):
        self.sock.sendall(text.encode("utf-8"))

    def until(self, prefix):
        for _ in range(30):
            while b"\n" not in self.buffer:
                data = self.sock.recv(4096)
                if not data:
                    raise AssertionError("Connection closed before " + prefix)
                self.buffer += data
            line, self.buffer = self.buffer.split(b"\n", 1)
            text = line.decode("utf-8")
            if text.startswith(prefix):
                return text
        raise AssertionError("Response not found: " + prefix)

    def login(self, name):
        self.send("LOGIN " + name + "\n")
        return self.until("OK Logged in")

    def close(self):
        try:
            self.sock.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        self.sock.close()
        self.thread.join(2)
        assert not self.thread.is_alive()


class ChatTests(unittest.TestCase):
    def setUp(self):
        self.peers = []

    def tearDown(self):
        for peer in self.peers:
            peer.close()
        self.assertEqual(server.clients, {})

    def peer(self):
        peer = Peer()
        self.peers.append(peer)
        return peer

    def test_client_preserves_recipient_case_and_message(self):
        self.assertEqual(
            client.encode_message("/dm Bob Hello World"), b"DM Bob Hello World\n"
        )
        self.assertEqual(client.encode_message("/all Mixed CASE"), b"ALL Mixed CASE\n")
        self.assertEqual(client.encode_message("Hello World"), b"ALL Hello World\n")
        self.assertEqual(client.encode_message("/LiSt"), b"LIST\n")

    def test_login_list_and_duplicate_username(self):
        alice, other = self.peer(), self.peer()
        alice.login("Alice")
        other.send("LOGIN Alice\n")
        self.assertEqual(other.until("ERR"), "ERR Username taken")
        other.login("Bob")
        alice.send("LIST\n")
        self.assertEqual(alice.until("SYS ONLINE Alice, Bob"), "SYS ONLINE Alice, Bob")

    def test_group_and_private_messages(self):
        alice, bob = self.peer(), self.peer()
        alice.login("Alice")
        bob.login("Bob")
        alice.sock.sendall(client.encode_message("Hello Everyone"))
        self.assertEqual(bob.until("MSG GROUP"), "MSG GROUP Alice Hello Everyone")
        alice.sock.sendall(client.encode_message("/dm Bob Hello שלום"))
        self.assertEqual(bob.until("MSG DM"), "MSG DM Alice Hello שלום")
        self.assertEqual(alice.until("OK Sent"), "OK Sent to Bob")

    def test_validation_and_login_requirement(self):
        peer = self.peer()
        peer.send("LIST\n")
        self.assertEqual(peer.until("ERR"), "ERR Please LOGIN first")
        peer.send("LOGIN Two Names\n")
        self.assertEqual(peer.until("ERR"), "ERR Usage: LOGIN <name>")
        peer.login("Alice")
        peer.send("DM Missing Hello\n")
        self.assertEqual(peer.until("ERR"), "ERR User not found: Missing")

    def test_quit_notifies_other_clients_and_allows_reconnect(self):
        alice, bob = self.peer(), self.peer()
        alice.login("Alice")
        bob.login("Bob")
        alice.send("QUIT\n")
        self.assertEqual(alice.until("SYS BYE"), "SYS BYE")
        self.assertEqual(bob.until("SYS USER_LEFT"), "SYS USER_LEFT Alice")
        self.assertEqual(bob.until("SYS ONLINE Bob"), "SYS ONLINE Bob")
        self.peer().login("Alice")

    def test_abrupt_disconnect_removes_user(self):
        alice, bob = self.peer(), self.peer()
        alice.login("Alice")
        bob.login("Bob")
        alice.close()
        self.peers.remove(alice)
        self.assertEqual(bob.until("SYS USER_LEFT"), "SYS USER_LEFT Alice")

    def test_stale_cleanup_does_not_remove_new_connection(self):
        old, old_peer = socket.socketpair()
        new, new_peer = socket.socketpair()
        try:
            server.clients["Alice"] = new
            server.cleanup_user("Alice", old)
            self.assertIs(server.clients["Alice"], new)
        finally:
            server.clients.clear()
            for sock in (old, old_peer, new, new_peer):
                sock.close()


class FragmentedSocket:
    def __init__(self, payload):
        self.chunks = iter(bytes([byte]) for byte in payload)
        self.sent = []

    def recv(self, size):
        return next(self.chunks, b"")

    def sendall(self, data):
        self.sent.append(data)

    def settimeout(self, timeout):
        pass

    def close(self):
        pass


class FramingTests(unittest.TestCase):
    def test_server_handles_utf8_split_between_bytes(self):
        sock = FragmentedSocket("LOGIN Alice\nALL שלום\nQUIT\n".encode())
        server.handle_client(sock, "fragmented-test")
        self.assertIn("MSG GROUP Alice שלום\n".encode(), sock.sent)
        self.assertEqual(server.clients, {})

    def test_client_handles_utf8_split_between_bytes(self):
        sock = FragmentedSocket("MSG GROUP Alice שלום\nSYS BYE\n".encode())
        output = io.StringIO()
        done = threading.Event()
        with contextlib.redirect_stdout(output):
            client.recv_loop(sock, done)
        self.assertIn("MSG GROUP Alice שלום", output.getvalue())
        self.assertIn("SYS BYE", output.getvalue())
        self.assertTrue(done.is_set())


if __name__ == "__main__":
    unittest.main()
