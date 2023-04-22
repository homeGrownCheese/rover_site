import requests
import dotenv
import os

from django.shortcuts import render

# load the .env file
dotenv.load_dotenv()


API_KEY = os.getenv("API_KEY")


def home(request):
    # get the users selections for sol and camera from the form
    sol = request.GET.get("sol", 1000)
    camera = request.GET.get("camera", "fhaz")
    page = request.GET.get("page", 1)

    if camera == "all":
        url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol={sol}&page={page}&api_key={API_KEY}"
    else:
        url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol={sol}&camera={camera}&page=1&api_key={API_KEY}"
    # make a request to the NASA API

    data = requests.get(url).json()
    # print(data)
    print(API_KEY)
    return render(request, "home/index.html", {"data": data})
