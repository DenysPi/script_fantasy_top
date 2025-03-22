import requests

url = "https://auth.privy.io/api/v1/oauth/request"

headers = {
    "Content-Type": "application/json",
    "Accept": "application/json",
    "Origin": "https://monad.fantasy.top",
    "Referer": "https://monad.fantasy.top/",
    "Privy-App-Id": "cm6ezzy660297zgdk7t3glcz5",
    "User-Agent": "Mozilla/5.0",
}

payload = {
    "provider": "google",
    "redirect_to": "https://monad.fantasy.top/login"
}

resp = requests.post(url, headers=headers, json=payload)

print("STATUS CODE:", resp.status_code)
print("RESPONSE TEXT:", resp.text)