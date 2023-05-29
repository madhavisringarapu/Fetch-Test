import yaml
import requests
import time

def check_health(endpoints):
    availability = {}

    for endpoint in endpoints:
        name = endpoint['name']
        url = endpoint['url']
        availability[name] = {'up_count': 0, 'total_count': 0}

    while True:
        for endpoint in endpoints:
            name = endpoint['name']
            url = endpoint['url']
            method = endpoint.get('method', 'GET')
            headers = endpoint.get('headers', {})
            body = endpoint.get('body')

            start_time = time.time()
            response = requests.request(method, url, headers=headers, json=body)
            end_time = time.time()

            response_time = (end_time - start_time) * 1000  # Convert to milliseconds

            if response.ok and response_time < 500:
                availability[name]['up_count'] += 1

            availability[name]['total_count'] += 1

        print_availability(availability)
        time.sleep(15)

def print_availability(availability):
    for name, stats in availability.items():
        percentage = (stats['up_count'] / stats['total_count']) * 100
        print(f"{name} has {percentage}% availability percentage")

if __name__ == "__main__":
    file_path = input("Enter the path to the YAML file: ")

    with open(file_path, 'r') as f:
        endpoints = yaml.safe_load(f)

    check_health(endpoints)

