# Python Client-Server Chat

A terminal chat application built with Python sockets and threads for a networking study project. One server handles multiple clients, with group messages, direct messages and an online-user list.

Browse the [project report](docs/tcp-chat-project-report.md), [network analysis](docs/network/README.md) directly on GitHub. Word, Excel and packet-capture files are also available.

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

Both programs default to `127.0.0.1:50000`, so the demo runs on one computer without editing the source code.

Start the server:

```bash
python server.py
```

Open two more terminals and run this in each:

```bash
python client.py
```

Choose a different username for each client, such as `Alice` and `Bob`. Usernames are case-sensitive; commands preserve the recipient's name and message text.

To choose another port, use `python server.py --port 50500` and `python client.py --port 50500`. For a trusted local-network demo, bind the server to its LAN address with `--host` and pass that same address to each client. Use `--help` to see the available options. The application does not encrypt traffic.

## Client commands

| Input | Behavior |
| --- | --- |
| `Hello everyone` | Sends a group message, preserving its case |
| `/list` | Lists connected users |
| `/dm Bob Hello` | Sends a direct message to Bob without changing the message case |
| `/quit` | Closes the client |

The server protocol accepts `LOGIN <name>`, `LIST`, `ALL <message>`, `DM <name> <message>` and `QUIT`. Responses use `SYS`, `OK`, `ERR` and `MSG` prefixes.

Only the command word is case-insensitive. Both receive loops buffer bytes until a complete line arrives, preserving UTF-8 text even when a character is split between socket reads. If the server disconnects while the terminal is waiting for input, press Enter to exit.

## Tests

Run the standard-library test suite with:

```bash
python -m unittest discover -s tests -v
```

Tests cover login, duplicate usernames, group and direct messages, username validation, clean and abrupt disconnections, reconnection, and fragmented UTF-8 messages. GitHub Actions runs the suite on Windows and Linux with Python 3.10 and 3.13.

## Repository contents

| File | Purpose |
| --- | --- |
| [server.py](server.py) | Connection handling, user registry and message routing |
| [client.py](client.py) | Terminal input and background receive loop |
| [Project report](docs/tcp-chat-project-report.md) | Read the original Hebrew report in the browser |
| [Network analysis](docs/network/README.md) | Worksheet previews and CSV tables that open on GitHub |
| [Word report](docs/tcp-chat-project-report.docx) | Report with neutral example usernames |
| [Packet capture](docs/network/server-traffic-capture.pcapng) | Original capture for Wireshark |
| [Traffic analysis workbook](docs/network/traffic-analysis.xlsx) | Excel workbook with HTTP message examples |
| [Traffic data workbook](docs/network/traffic-data.xlsx) | Original Excel workbook with TCP packet data |

The report and worksheet previews need no download. Word and Excel versions are also available; the packet capture requires a tool such as Wireshark. These materials are not application dependencies.

## Scope and next steps

This is a local networking exercise. It has no encryption, password authentication or persistent message history. A username identifies a connection; it does not verify a person's identity.

Possible next steps include TLS, authenticated accounts, message-size limits and per-client send queues for slow connections.

[More projects](https://github.com/omerbenguigui)
