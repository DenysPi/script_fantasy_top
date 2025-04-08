from requests import request
url = 'https://api.aicraft.fun/feeds/orders/67f2a8c644ff1fa0c98f70ab/confirm'
headers = {
    'Authorization': 'Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InVzZXJfMHg2Ql9DMjc3MTUiLCJyZWZDb2RlIjoiSjNJUVhSWTZNMCIsImlhdCI6MTc0Mzg2MzM2OSwiZXhwIjoxNzQ0NDY4MTY5fQ.O22dWFby1PVp9jzfcLpA0Eu_WTbPSzgblJXaOgy6OjU',
    'Content-Type': 'application/json',
}
payload = {
    'refCode': 'AS1UYLUZT2',
    'transactionHash': '0x29387e40ad1fbdfa3ea02d0e3360bc82f3d24aced866bee056497b2fc64beb75'
}

response = requests.post(url, json=payload, headers=headers)
print(response.json())