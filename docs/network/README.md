# Network Traffic Analysis

The traffic-data workbook contains TCP packet rows for the chat session. The traffic-analysis workbook contains separate HTTP message examples from the coursework; it is not a decoded chat transcript.

Read the exported worksheet values below or open the CSV tables directly on GitHub. These are snapshots of the values saved in the original Excel files; workbook formatting and charts remain in the downloads.

[Packet capture](server-traffic-capture.pcapng) · [TCP stream screenshot](../images/wireshark-tcp-stream.png)

## Traffic Analysis — group661305-5_http_input

[View all 11 rows as CSV](traffic-analysis-sheet-1.csv) · [Original workbook](traffic-analysis.xlsx)

| msg_id | app_protocol | src_app | dst_app | message | timestamp |
| --- | --- | --- | --- | --- | --- |
| 1 | HTTP | client_browser | web_server | GET /index.html | 1.4999999999999999E-2 |
| 2 | HTTP | web_server | client_browser | HTTP/1.1 200 OK | 0.02 |
| 3 | HTTP | client_browser | web_server | User-Agent: Mozilla/5.0 | 3.5000000000000003E-2 |
| 4 | HTTP | web_server | client_browser | Content-Type: text/html | 0.04 |
| 5 | HTTP | client_browser | web_server | Accept-Language: en-US | 5.5E-2 |
| 6 | HTTP | web_server | client_browser | Server: Apache/2.4.41 | 0.06 |
| 7 | HTTP | client_browser | web_server | Connection: keep-alive | 7.4999999999999997E-2 |
| 8 | HTTP | web_server | client_browser | Date: Mon |  21 Oct 2024 |
| 9 | HTTP | client_browser | web_server | Host: google.com | 9.5000000000000001E-2 |
| 10 | HTTP | web_server | client_browser | Cache-Control: private | 0.1 |

## Traffic Data — traffic_data

[View all 27 rows as CSV](traffic-data-sheet-1.csv) · [Original workbook](traffic-data.xlsx)

| No. | Time | Source | Destination | Protocol | Length | Info |
| --- | --- | --- | --- | --- | --- | --- |
| 997 | 98.906227000000001 | 192.168.1.83 | 192.168.1.73 | TCP | 66 | 57681  >  50000 [SYN] Seq=0 Win=64240 Len=0 MSS=1460 WS=256 SACK_PERM |
| 998 | 98.906435000000002 | 192.168.1.73 | 192.168.1.83 | TCP | 66 | 50000  >  57681 [SYN, ACK] Seq=0 Ack=1 Win=65535 Len=0 MSS=1460 WS=256 SACK_PERM |
| 999 | 98.915390000000002 | 192.168.1.83 | 192.168.1.73 | TCP | 54 | 57681  >  50000 [ACK] Seq=1 Ack=1 Win=262656 Len=0 |
| 1000 | 98.916957999999994 | 192.168.1.73 | 192.168.1.83 | TCP | 66 | 50000  >  57681 [PSH, ACK] Seq=1 Ack=1 Win=65280 Len=12 |
| 1001 | 98.97045 | 192.168.1.83 | 192.168.1.73 | TCP | 54 | 57681  >  50000 [ACK] Seq=1 Ack=13 Win=262656 Len=0 |
| 1002 | 98.970580999999996 | 192.168.1.73 | 192.168.1.83 | TCP | 203 | 50000  >  57681 [PSH, ACK] Seq=13 Ack=1 Win=65280 Len=149 |
| 1003 | 99.034564000000003 | 192.168.1.83 | 192.168.1.73 | TCP | 54 | 57681  >  50000 [ACK] Seq=1 Ack=162 Win=262400 Len=0 |
| 1208 | 124.689628 | 192.168.1.83 | 192.168.1.73 | TCP | 66 | 57681  >  50000 [PSH, ACK] Seq=1 Ack=162 Win=262400 Len=12 |
| 1209 | 124.689993 | 192.168.1.73 | 192.168.1.83 | TCP | 76 | 50000  >  57681 [PSH, ACK] Seq=162 Ack=13 Win=65280 Len=22 |
| 1222 | 124.74615 | 192.168.1.83 | 192.168.1.73 | TCP | 54 | 57681  >  50000 [ACK] Seq=13 Ack=184 Win=262400 Len=0 |
