# Python TCP Chat

A terminal chat application built with Python sockets and threads for a networking study project. One server handles multiple clients, with group messages, direct messages and an online-user list.

The repository also contains a packet capture, traffic-analysis workbooks, screenshots and a project report.

## How it works

```text
Client A ---- TCP ----+
                     |
                  Server ---- shared client registry
                     |
Client B ---- TCP ----+
```

The server creates a thread for each connection. A lock protects the username-to-socket registry. Messages are UTF-8 text delimited by newlines; receive loops retain incomplete lines between socket reads.

## Run locally

Requires **Python 3.10 or newer**. Both programs use only the standard library, so no pip packages are needed.

For a demo on one computer, set these constants before running:

- In `client.py`: `SERVER_IP = "127.0.0.1"`
- In `server.py`: `HOST = "127.0.0.1"`

The checked-in client address is from the original local network. Both programs use port `50000`; the server's checked-in `0.0.0.0` address listens on all network interfaces.

Start the server:

```bash
python server.py
```

Open two more terminals and run this in each:

```bash
python client.py
```

Choose a different username for each client. For the existing client's direct-message behavior, use uppercase names such as `ALICE` and `BOB`.

## Client commands

| Input | Behavior |
| --- | --- |
| `Hello everyone` | Sends a group message, preserving its case |
| `/list` | Lists connected users |
| `/dm BOB Hello` | Sends a direct message to BOB |
| `/quit` | Closes the client |

The server protocol accepts `LOGIN <name>`, `LIST`, `ALL <message>`, `DM <name> <message>` and `QUIT`. Responses use `SYS`, `OK`, `ERR` and `MSG` prefixes.

**Client limitation:** slash commands currently uppercase the entire line, including the direct-message recipient and message body. Usernames are case-sensitive on the server. Ordinary messages avoid this conversion.

## Repository contents

| File | Purpose |
| --- | --- |
| [server.py](server.py) | Connection handling, user registry and message routing |
| [client.py](client.py) | Terminal input and background receive loop |
| [Packet capture](ServerCapture%20%281%29.pcapng) | Capture included with the networking project |
| [Traffic analysis workbook](traffic_analysis.csv.xlsx) | Analysis workbook in Excel format |
| [Traffic data workbook](traffic_data.xlsx) | Supporting traffic data |
| [Project report](דוח%20פרויקט%20שקד%20ועומר.docx) | Hebrew report accompanying the project |

The PNG files in the repository show the original project sessions. The capture can be opened in Wireshark; the workbooks and report are supporting materials, not application dependencies.

## Scope and next steps

This is a local networking exercise. It has no encryption, password authentication, persistent message history or automated test suite. A username identifies a connection; it does not verify a person's identity.

The next improvements would be to preserve command arguments, make host and port configurable at launch, add protocol tests, and report connection errors instead of suppressing them.

[More projects](https://github.com/omerbenguigui)
