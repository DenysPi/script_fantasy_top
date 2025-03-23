# import requests

# # Define the URL
# url = 'https://secret-api.fantasy.top/hero/feed?pagination.limit=20&pagination.page=1&topHeroes=5000&banger=true'

# # Define the headers as per the information you provided
# headers = {
#     'Accept': 'application/json, text/plain, */*',
#     'Authorization': 'Bearer eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IjdQNzVsMHZVbEkwemJBU1RPbnpfTDhPcXhIN0VQYUlsUWNHalNyMGxqM3cifQ.eyJjciI6IjE3Mzk5ODQyMzYiLCJsaW5rZWRfYWNjb3VudHMiOiJbe1widHlwZVwiOlwiZ29vZ2xlX29hdXRoXCIsXCJzdWJqZWN0XCI6XCIxMTMyNjc5MDk2NTg2OTkxNDgzNjlcIixcImVtYWlsXCI6XCJkZW5pc3BpZGR1Ym5pajlAZ21haWwuY29tXCIsXCJuYW1lXCI6XCJEZW55cyBQaWRkdWJueWlcIixcImx2XCI6MTc0Mjc1OTE0OH0se1widHlwZVwiOlwid2FsbGV0XCIsXCJhZGRyZXNzXCI6XCIweEFjMDNlRTRFMmIyM2Y0ODYyNjQwNkZlOTNBYzIzNGY2ZmFkNzcxNDNcIixcImNoYWluX3R5cGVcIjpcImV0aGVyZXVtXCIsXCJ3YWxsZXRfY2xpZW50X3R5cGVcIjpcInByaXZ5XCIsXCJsdlwiOjE3Mzk5ODQyNDB9XSIsImlzcyI6InByaXZ5LmlvIiwiaWF0IjoxNzQyNzU5MTQ4LCJhdWQiOiJjbTZlenp5NjYwMjk3emdkazd0M2dsY3o1Iiwic3ViIjoiZGlkOnByaXZ5OmNtN2M1b3RqNjAybGlubDBqMHp2dGcweTAiLCJleHAiOjE3NDI3NjI3NDh9.QF_N5kFZk3VUD_0CGu0pwXtsZjYgEL6N0DVg-waVBOGdii_8deNpkrr1Lv4sXqYgko9NNeoiXpnBDFL_F5ITQg',
#     'Referer': 'https://monad.fantasy.top/',
#     'Sec-CH-UA': '"Chromium";v="134", "Not:A-Brand";v="24", "Google Chrome";v="134"',
#     'Sec-CH-UA-Mobile': '?0',
#     'Sec-CH-UA-Platform': '"Windows"',
#     'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36',
# }

# # Send the GET request
# response = requests.get(url, headers=headers)

# # Check if the request was successful
# if response.status_code == 200:
#     print("Request was successful!")
#     print("Response Data:", response.json())  # Assuming the response is JSON
# else:
#     print(f"Request failed with status code {response.status_code}")
