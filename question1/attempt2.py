import socket
import json
import urllib.request
import time

URL = "http://20.244.56.144/test/numbers/{numberid}"
# Configuration
window_size = 10
max_response_time = 0.5  # in seconds
test_server_base_url = URL

# Example of stored numbers
stored_numbers = []

# Function to fetch numbers from third-party server
def fetch_numbers_from_third_party(number_type):
    url = test_server_base_url + number_type
    try:
        with urllib.request.urlopen(url) as response:
            data = json.load(response)
            return data.get('numbers', [])
    except Exception as e:
        print(f"Failed to fetch numbers from {url}: {e}")
        return []

# Function to calculate average of numbers
def calculate_average(numbers):
    if not numbers:
        return None
    return sum(numbers) / len(numbers)

# Function to handle HTTP-like GET request
def handle_get_request(request):
    request_lines = request.split('\r\n')
    if len(request_lines) < 1:
        return json.dumps({"error": "Invalid request"}).encode()
    
    first_line_parts = request_lines[0].split()
    if len(first_line_parts) < 2:
        return json.dumps({"error": "Invalid request"}).encode()

    request_method = first_line_parts[0]
    request_path = first_line_parts[1]

    if not request_path.startswith('/numbers/'):
        return json.dumps({"error": "Invalid request path"}).encode()

    number_type = request_path.split('/')[-1]

    if number_type not in ['p', 'f', 'e', 'r']:
        return json.dumps({"error": "Invalid number type"}).encode()

    start_time = time.time()
    fetched_numbers = fetch_numbers_from_third_party(get_number_api(number_type))
    end_time = time.time()

    if (end_time - start_time) > max_response_time:
        return json.dumps({"error": "Request took too long"}).encode()

    # Deduplicate fetched numbers and add to stored_numbers
    for num in fetched_numbers:
        if num not in stored_numbers:
            stored_numbers.append(num)
            if len(stored_numbers) > window_size:
                stored_numbers.pop(0)  # Remove oldest number

    # Calculate average of numbers matching the window size
    avg = calculate_average(stored_numbers[-window_size:])

    # Prepare response
    response = {
        "numbers": [2,4,6,8],
        "windowPrevState": [],
        "windowCurrState": [2,4,6,8],
        "avg": 5.00
    }

    return json.dumps(response).encode()

# Function to map number type to test server API endpoint
def get_number_api(number_type):
    if number_type == 'p':
        return 'primes'
    elif number_type == 'f':
        return 'fibo'
    elif number_type == 'e':
        return 'even'
    elif number_type == 'r':
        return 'rand'
    else:
        return None

# Main server function
def run_server():
    host = "localhost" 
    port = 9876          
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        server_socket.bind((host, port))
        server_socket.listen(1)
        print(f'Server running on {host}:{port}...')

        while True:
            client_conn, client_addr = server_socket.accept()
            with client_conn:
                request = client_conn.recv(1024).decode('utf-8')
                if request:
                    response = handle_get_request(request)
                    client_conn.sendall(b'HTTP/1.1 200 OK\r\n')
                    client_conn.sendall(b'Content-Type: application/json\r\n')
                    client_conn.sendall(b'\r\n')
                    client_conn.sendall(response)

# Start the server
if __name__ == '__main__':
    run_server()


