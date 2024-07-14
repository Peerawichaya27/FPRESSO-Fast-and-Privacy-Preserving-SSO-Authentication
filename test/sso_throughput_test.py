import concurrent.futures
import requests
import time
import statistics

# Configuration
base_url = 'https://app1-hlcp4m5f5q-as.a.run.app'
protected_url = f'{base_url}/protected'
sso_token = 'liG85FKW68TAxKGG9fc3ZQB5n-m5-6-4Deffj4hQPlS81CIfTMdTqzDjPrZUDcOnQ2Zx6rsUCDCM-2by5v-LdebEWP2UNCvhjtA3iGJwFlHxLw617bSOqqHInM6ZHlyWGKckWkQMVOClGQIYZPIWO7r664nFT4dyMx-hexoV1kJleUpoYkdjaU9pSklVekkxTmlJc0luUjVjQ0k2SWtwWFZDSjkuZXlKMWMyVnlTVVFpT2lKMWMyVnlNU0lzSW5KdmJHVnpJanA3SW1Gd2NERWlPaUl6TldFek56RTJaRE0wTXpBME1HTTJOalpoTURjeE5EYzNOREkzTlRNMVlXUmhOekJtTnpSalpXVmxPR0k1WkRrd05UaGtORFF4TW1OaVpUUXdZelV5SWl3aVlYQndNaUk2SWpCaU16VmlPVEl5Wm1ReFl6VTROVE5qWmpZMVlqY3pOMlkwT1dNME9XUTRaV1kzTlRBNU5EWmlOVGt6T1RRME16QTFObVE1TkdJellUTTFNVEJrWXpZaUxDSmhjSEF6SWpvaU1HSXpOV0k1TWpKbVpERmpOVGcxTTJObU5qVmlOek0zWmpRNVl6UTVaRGhsWmpjMU1EazBObUkxT1RNNU5EUXpNRFUyWkRrMFlqTmhNelV4TUdSak5pSjlMQ0p3WlhKdGFYTnphVzl1Y3lJNmV5SmhjSEF4SWpvaU1UTTRZelJpTUdJNU5tTXdNV0l3TnpFMVpEZzNNR014TVdNd09EVXpOVGt5WVdFek1qRXpOMk0wTWpGbE56TTRNamM0TWpGbVpURTBZemxoWVdJMlpTSXNJbUZ3Y0RJaU9pSXdaREV5Tnpsak1tVXpOekpqWmpGak9HUmpZelJpWldZd1kyWXlORE14WldGaVkySTJNV1JrWkRVeVkyUTJNVE0yTnpOak1UVmxZakpqWWpoaE9UVTRJaXdpWVhCd015STZJamRsTmpSaE56VTJZVEF4T0RnNE4ySTJNemMzTm1RNE5Ua3lPRFZqWkdNNU1UQXhNbVUwT0RNMFpEYzBaREV4TXpObE1qWTFNR1ptTmpjeU56Y3daRFlpZlN3aVpYaHdJam94TnpFNU5qa3hNVFF3ZlEudVg2eGZXTXdqQ3M3NGVsS3JWVFRmdGdIOGtYelc5TUJObmY0VVB2SndVdy40OTQ4Y2IzZTgxZGQ5OGQzZDRiMTc5MDQ3OGZkNmRhNGQ1ODE5ZjUzNzhlNWQ0MWI2MTQzYzBjZGFhMTA3ZDFlZjQyNjM5ZTFlMzgzNzkyMjkzOTM4Y2ExM2Y2ZTI0NGI4NDk4ZGQ0MTNlN2IzMjQzY2U1MTA2ZDA1NmVlMmNhZDMyZWEzMmZhOWM2Yjk3YjYwMzQzZjJiOTAzZjA2YjVhODg4ZmEzNzU2YzI2M2M4OWNlM2EyZWQ1MGMxMDMxYzI4ZmU3ODZmZDk0ZGMyZDllMGZiZjU3MDM3Y2FmYWM4MWYzYzk1MWM2NjQ0M2JiNWZiYzJlYTcxODMwOGFiYjYxMmY0MjI1ZTNlOWM1ZDFmOGVhM2MyNmE2MDMyMjAyZGY5Njg0ODQ1MjVkODlhMmE1NGRhMTA1MDJiNTc2ZTg3NTA0NTdhODNkOWViZGRmNzA2YWYzMmE4YTIzMDUzOTJiOGZkZmRiMWU3YmM1ZDUxZTI3YjM1MzU1MGIzYjRkMTNjMGRkZDE1NDFiYmRjMmRhZWY3MTVkNTRkMjM5ZTA3MmM5NjZlZjNlZjU5ZjljMjk2ZDIxNTI3NGNlNDUyYjlmZmM3YTUzYjAwZjI4ZjZhNGRkZjhmOGJkY2ZlNjgwOTUxYTdhZWNjMjBhN2FjNDY2NzlkZmE2YTNhOTY1MzJmZqNZ7gLsTHM29IraQe4SaE1kLEJngUbqlLe8YeyrADCJaG_9iW12Osrvk0tgpeLQSRecGFrcYejfEwvf-bGDh426gPgED2rabmCdqqfHdv1w2cdJXmkLVUEIwETLzpx9ZC5b_ew2u0WXEBefFdMZGpwh8eKRWeyf7fskc2AUhawD'  # Replace with your actual SSO token
num_repeats = 3  # Number of times to repeat each test

def access_protected_route():
    """Access the protected route with the provided SSO token."""
    headers = {'Cookie': f'sso_token={sso_token}'}
    response = requests.get(protected_url, headers=headers)
    return response.status_code

def simulate_user():
    """Simulate a single user accessing the protected route."""
    status_code = access_protected_route()
    if status_code != 200:
        print(f'Error: Received status code {status_code}')

def run_test(num_requests):
    """Run the test with the specified number of requests."""
    start_time = time.time()

    with concurrent.futures.ThreadPoolExecutor(max_workers=num_requests) as executor:
        futures = [executor.submit(simulate_user) for _ in range(num_requests)]
        concurrent.futures.wait(futures)

    end_time = time.time()
    elapsed_time = end_time - start_time
    return elapsed_time

def warm_up():
    """Warm up the application before running tests."""
    print("Warming up...")
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        futures = [executor.submit(simulate_user) for _ in range(100)]
        concurrent.futures.wait(futures)
    print("Warm-up complete.")

def main():
    """Main function to run tests for different request counts."""
    request_counts = [10, 50, 100, 500, 1000]
    warm_up()

    for count in request_counts:
        elapsed_times = []
        for _ in range(num_repeats):
            elapsed_time = run_test(count)
            elapsed_times.append(elapsed_time)
        
        average_time = statistics.mean(elapsed_times)
        throughput = count / average_time
        print(f'\nResults for {count} requests:')
        print(f'Average time: {average_time:.2f} seconds')
        print(f'Throughput: {throughput:.2f} requests/second')

if __name__ == '__main__':
    main()