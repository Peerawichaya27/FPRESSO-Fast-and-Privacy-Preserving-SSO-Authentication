import requests
import time
from concurrent.futures import ThreadPoolExecutor
import statistics

# Define the number of concurrent users to test
user_counts = [50,100]
num_repeats = 5  # Increase the number of repetitions for more consistency

# Define the URLs for token generation and verification
generate_token_url = 'https://app1-test-hlcp4m5f5q-as.a.run.app/generate_token'
verify_token_url = 'https://app1-test-hlcp4m5f5q-as.a.run.app/verify_token'

# Function to measure latency for token generation
def generate_token():
    start_time = time.time()
    response = requests.get(generate_token_url)
    latency = (time.time() - start_time) * 1000  # Convert to milliseconds
    if response.status_code == 200:
        sso_token = response.json()['sso_token']
        return latency, sso_token
    return latency, None

# Function to measure latency for token verification
def verify_token(sso_token):
    start_time = time.time()
    response = requests.post(verify_token_url, json={'sso_token': sso_token})
    latency = (time.time() - start_time) * 1000  # Convert to milliseconds
    return latency, response.status_code

# Function to run the test for a given number of users for token verification
def run_verify_token_test(user_count, sso_token):
    latencies = []
    with ThreadPoolExecutor(max_workers=user_count) as executor:
        futures = [executor.submit(verify_token, sso_token) for _ in range(user_count)]
        for future in futures:
            latency, status_code = future.result()
            if status_code == 200:
                latencies.append(latency)
    return latencies

# Run the test for each user count
for user_count in user_counts:
    print(f"\nTesting token verification for {user_count} users...")

    # Generate a single token for verification tests
    _, sso_token = generate_token()
    if sso_token is None:
        print(f'Failed to generate token for {user_count} users')
        continue

    # Test token verification
    all_verify_latencies = []
    for _ in range(num_repeats):
        latencies = run_verify_token_test(user_count, sso_token)
        if latencies:
            all_verify_latencies.extend(latencies)
    
    if all_verify_latencies:
        avg_verify_latency = statistics.mean(all_verify_latencies)
        print(f'Average token verification latency for {user_count} users: {avg_verify_latency:.2f} ms')
    else:
        print(f'No successful token verification for {user_count} users')
