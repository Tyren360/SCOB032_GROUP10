import json
import requests

CONTROLLER = "http://10.10.6.204"
USERNAME = "sdnadmin"
PASSWORD = "<REDACTED>"

ticket_url = CONTROLLER + "/api/v1/ticket"
devices_url = CONTROLLER + "/api/v1/network-device"

print("UL SMART CAMPUS SDN MONITOR")
print("Connecting to controller:", CONTROLLER)

login_data = {
    "username": USERNAME,
    "password": PASSWORD
}

login_headers = {
    "content-type": "application/json"
}

login_response = requests.post(
    ticket_url,
    data=json.dumps(login_data),
    headers=login_headers,
    timeout=30
)

print("Authentication status:", login_response.status_code)

if login_response.status_code not in (200, 201):
    print("Authentication failed.")
    print(login_response.text)
    raise SystemExit

ticket_data = login_response.json()
ticket = ticket_data["response"]["serviceTicket"]

print("Authentication successful.")

device_headers = {
    "x-auth-token": ticket,
    "content-type": "application/json"
}

device_response = requests.get(
    devices_url,
    headers=device_headers,
    timeout=30
)

print("Device request status:", device_response.status_code)

if device_response.status_code != 200:
    print("Could not retrieve managed devices.")
    print(device_response.text)
    raise SystemExit

device_data = device_response.json()
devices = device_data["response"]

print("Managed devices found:", len(devices))
print("--------------------------------")

for device in devices:
    print("Hostname:", device.get("hostname", "Unknown"))
    print("Management IP:", device.get("managementIpAddress", "Unknown"))
    print("Device type:", device.get("type", "Unknown"))
    print("Reachability:", device.get("reachabilityStatus", "Unknown"))
    print("Collection status:", device.get("collectionStatus", "Unknown"))
    print("--------------------------------")

print("SDN monitoring completed successfully.")