import requests
import time
from concurrent.futures import ThreadPoolExecutor
import statistics

# Define the number of concurrent users to test
user_counts = [10,50,100,500,1000]
num_repeats = 3  # Number of times to repeat each test

# Define the login URL and protected URL
login_url = 'https://app1-hlcp4m5f5q-as.a.run.app/login'
protected_url = 'https://app1-hlcp4m5f5q-as.a.run.app/protected'

# Define the login payload
login_payload = {
    "username": "user1",
    "password": "pass1"
}

# Function to login and measure verification latency
def login_and_verify():
    with requests.Session() as session:
        # Perform login
        login_response = session.post(login_url, data=login_payload)
        if login_response.status_code == 200:
            # Measure latency for verification
            start_time = time.time()
            verify_response = session.get(protected_url)
            latency = (time.time() - start_time) * 1000  # Convert to milliseconds
            return latency
        return None

# Function to run the test for a given number of users
def run_test(user_count):
    latencies = []
    with ThreadPoolExecutor(max_workers=user_count) as executor:
        futures = [executor.submit(login_and_verify) for _ in range(user_count)]
        for future in futures:
            latency = future.result()
            if latency is not None:
                latencies.append(latency)
    return latencies

# Run the test for each user count
for user_count in user_counts:
    all_latencies = []
    for _ in range(num_repeats):
        latencies = run_test(user_count)
        if latencies:
            all_latencies.extend(latencies)
    
    if all_latencies:
        avg_latency = statistics.mean(all_latencies)
        print(f'Average latency for {user_count} users: {avg_latency:.2f} ms')
    else:
        print(f'No successful logins for {user_count} users')
