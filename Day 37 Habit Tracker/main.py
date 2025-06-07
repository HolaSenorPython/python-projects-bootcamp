import requests
import datetime as dt
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

USERNAME = os.getenv("PIXELA_USERNAME")
TOKEN = os.getenv("PIXELA_TOKEN")
GRAPH_ID = "graph1"

pixela_endpoint = "https://pixe.la/v1/users"

user_parameters = {
    "token": TOKEN,
    "username": USERNAME,
    "agreeTermsOfService": "yes",
    "notMinor": "yes",
}

# To create a user (run once)
# response = requests.post(url=pixela_endpoint, json=user_parameters)
# print(response.text)

graph_endpoint = f"{pixela_endpoint}/{USERNAME}/graphs"
graph_parameters = {
    "id": GRAPH_ID,
    "name": "Productivity Graph",
    "unit": "minutes",
    "type": "int",
    "color": "shibafu",
}

headers = {
    "X-USER-TOKEN": TOKEN,
}

# To create the graph (run once)
# response = requests.post(url=graph_endpoint, json=graph_parameters, headers=headers)
# print(response.text)

pixel_add_endpoint = f"{graph_endpoint}/{GRAPH_ID}"
today = dt.datetime.now()
pixel_params = {
    "date": today.strftime("%Y%m%d"),
    "quantity": input("How many minutes did you spend doing something productive today? "),
}

response = requests.post(url=pixel_add_endpoint, json=pixel_params, headers=headers)
print(response.text)

# Optional: edit an entry
pixel_edit_endpoint = f"{pixel_add_endpoint}/{pixel_params['date']}"
edited_pixel_params = {
    "quantity": "45",
}
# response = requests.put(url=pixel_edit_endpoint, json=edited_pixel_params, headers=headers)
# print(response.text)

# Optional: delete an entry
pixel_delete_endpoint = f"{pixel_add_endpoint}/{pixel_params['date']}"
# response = requests.delete(url=pixel_delete_endpoint, headers=headers)
# print(response.text)
