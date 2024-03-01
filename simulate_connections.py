import requests
import threading
import time
# Define the URL of your Load Balancer
lb_url = 'http://AppLBCA1-353695464.us-east-1.elb.amazonaws.com/'

# Define the number of concurrent connections to simulate
num_connections = 500000

# Define the function to send requests
def send_request():
    try:
        response = requests.get(lb_url)
        print(f'Response from {lb_url}: {response.status_code}')
    except Exception as e:
        print(f'Error connecting to {lb_url}: {str(e)}')

# Create threads to send requests concurrently
threads = []
for i in range(num_connections):
    thread = threading.Thread(target=send_request)
    threads.append(thread)
    thread.start()
    time.sleep(0)
# Wait for all threads to complete
for thread in threads:
    thread.join()

print('All requests sent.')


