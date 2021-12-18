import requests

print("Hello World!")
print("Fetching HTML of python homepage...")
r = requests.get("http://www.python.org")

print(f"Status was: {r.status_code}")
print(f"Does Python appear on the page? {'Yes!' if 'Python' in r.text else 'Nope!'}")
