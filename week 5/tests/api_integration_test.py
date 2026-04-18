import requests
import json
import time

BASE_URL = "http://127.0.0.1:8000"

def test_api():
    print("Waiting for server to be ready...")
    for _ in range(10):
        try:
            r = requests.get(f"{BASE_URL}/health")
            if r.status_code == 200:
                print("Server is UP!")
                break
        except Exception:
            time.sleep(1)
            
    # 1. Test Root
    r = requests.get(f"{BASE_URL}/")
    print(f"Root endpoint: {r.status_code} {r.json()}")
    
    # 2. Login as Finance User
    print("\nLogging in as Finance User...")
    payload = {"username": "finance_user", "password": "pass123"}
    r = requests.post(f"{BASE_URL}/auth/login", json=payload)
    if r.status_code != 200:
        print(f"Login failed: {r.text}")
        return
        
    token = r.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    print("Login success. Token received.")
    
    # 3. Test Authorized Query (Finance -> Finance Doc)
    print("\nTesting Authorized Query (Finance -> Finance Doc)...")
    q_payload = {"query": "Q4 revenue"}
    r = requests.post(f"{BASE_URL}/query/finance", json=q_payload, headers=headers)
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        res = r.json()
        print(f"Results Found: {len(res.get('results', []))}")
        if res.get('results'):
             print(f"First result: {res['results'][0]['content'][:50]}...")
    else:
        print(f"Error: {r.text}")

    # 4. Test Unauthorized Query (Finance -> HR Doc)
    # The endpoint /query/hr requires "hr" or "c-level". Finance user should strictly fail.
    print("\nTesting Unauthorized Endpoint (Finance -> HR Endpoint)...")
    r = requests.post(f"{BASE_URL}/query/hr", json=q_payload, headers=headers)
    print(f"Status: {r.status_code} (Expected 403)")
    if r.status_code == 403:
        print("PASS: Access Denied as expected.")
    else:
        print(f"FAIL: Unexpected status {r.status_code}")

    # 5. Test C-Level (All Access)
    print("\nLogging in as Admin (C-Level)...")
    payload = {"username": "admin", "password": "admin123"}
    r = requests.post(f"{BASE_URL}/auth/login", json=payload)
    admin_token = r.json()["access_token"]
    admin_headers = {"Authorization": f"Bearer {admin_token}"}
    
    print("Testing HR Query as Admin...")
    r = requests.post(f"{BASE_URL}/query/hr", json=q_payload, headers=admin_headers)
    print(f"Status: {r.status_code} (Expected 200)")
    
if __name__ == "__main__":
    test_api()
