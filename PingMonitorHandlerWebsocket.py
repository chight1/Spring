import asyncio
import websockets
import datetime
from http.server import SimpleHTTPRequestHandler, HTTPServer
import threading

# store connected clients
connected_clients = set()

async def ping_handler(websocket, path='/'):
	connected_clients.add(websocket)
	try:
		await websocket.wait_closed()
	finally:
		connected_clients.remove(websocket)

# websocket server to handle connections
async def start_ws_server():
	async with websockets.serve(ping_handler, "0.0.0.0", 6789):
		await asyncio.Future() #Run forever

# HTTP Handler for incoming pings
class HTTPPingHandler(SimpleHTTPRequestHandler):
	def do_GET(self):
		if self.path == '/ping':
			timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
			# Send timestamp to all connected websocket clients
			asyncio.run(send_to_clients(timestamp))
			self.send_response(200)
			self.end_headers()
			self.wfile.write(b'Ping received.')
		else:
			super().do_GET()

async def send_to_clients(message):
	if connected_clients:
		await asyncio.gather(*[client.send(message) for client in connected_clients])

def start_http_server():
	httpd = HTTPServer(('0.0.0.0', 8000), HTTPPingHandler)
	print("HTTP endpoint running at port 8000")
	httpd.serve_forever()

if __name__ == '__main__':
	threading.Thread(target=start_http_server, daemon=True).start()
	print("Websocket server running at ws://0.0.0.0:6789")
	asyncio.run(start_ws_server())