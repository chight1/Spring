import asyncio
import websockets
import datetime
from http.server import BaseHTTPRequestHandler, HTTPServer
import threading

pings = []

class PingMonitorHandler(BaseHTTPRequestHandler):
	def do_GET(self):
		global pings
		if self.path == '/ping':
			pings.append(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
			self.send_response(200)
			self.end_headers()
			self.wfile.write(b'Ping received.')
		else:
			self.send_response(200)
			self.send_header('Content-type', 'text/html')
			self.end_headers()
			pings_list = "<br>".join(pings[-20:])
			html = f"""
			<html>
				<head>
					<meta http-equiv="refresh" content="5">
					<title>Ping Monitor</title>
				</head>
				<body>
					<h2>Recent Pings:</h2>
					{pings_list if pings else 'No pings yet.'}
				</body>
			</html>
			"""
			self.wfile.write(html.encode('utf-8'))

if __name__ == "__main__":
	server_address = ('', 8000)
	httpd = HTTPServer(server_address, PingMonitorHandler)
	print("Ping Monitor Running at http://0.0.0.0:8000")
	httpd.serve_forever()