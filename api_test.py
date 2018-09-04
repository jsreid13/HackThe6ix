import requests

url = "https://264egqriu1.execute-api.ca-central-1.amazonaws.com/default/shopfast"
data = {"shopping_list": ["pasta", "beer"]}

response = requests.get(url, params=data)
print(response.text)
