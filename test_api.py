import requests

url = "http://127.0.0.1:5000/predict"
file = {'image': open('test.jpg', 'rb')}  # make sure test.jpg is in the same folder

response = requests.post(url, files=file)
print(response.json())
