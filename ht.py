from http.server import BaseHTTPRequestHandler, HTTPServer
# Define the API request handler
class APIServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Set the response status code
        self.send_response(200)

        # Set the response headers
        self.send_header("Content-type", "application/json")
        self.end_headers()

        # Construct the response body
        response = {
            "message": "Hello, API!",
        }

        # Convert the response to JSON and send it
        self.wfile.write(bytes(json.dumps(response), "utf-8"))

# Set the host and port for the server
host = ""
port = 

# Create the HTTP server
server = HTTPServer((host, port), APIServerHandler)

# Start the server
print(f"Starting server at http://{host}:{port}")
server.serve_forever()
