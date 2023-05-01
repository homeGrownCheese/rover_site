import requests
import dotenv
import os
import json


from django.shortcuts import render

# load the .env file
dotenv.load_dotenv()


API_KEY = os.getenv("API_KEY")


def home(request):
    # If the request is a post request, then the user has submitted the form for their api key, and it needs to be saved in a session
    if request.method == "POST":
        api_key = request.POST.get("api_key")
        request.session["api_key"] = api_key
        print(f"api_key: {api_key}")

    # if the user has a session, use their api key, otherwise use the default
    if "api_key" in request.session:
        api_key = request.session["api_key"]
        print("Using session api key")
    else:
        api_key = API_KEY

    # get the users selections for sol and camera from the form
    sol = request.GET.get("sol", 1000)
    camera = request.GET.get("camera", "fhaz")
    page = request.GET.get("page", 1)

    # in case the user has an invalid api key or the cookie is invalid, try to search using theirs first, then fall back to the default

    if camera == "all":
        url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol={sol}&page={page}&api_key={api_key}"
    else:
        url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/curiosity/photos?sol={sol}&camera={camera}&page={page}&api_key={api_key}"
    # make a request to the NASA API
    # print the headers
    headers = requests.get(url).headers
    print(headers)
    remaining = headers["X-RateLimit-Remaining"]
    print(f"Remaining requests: {remaining}")

    data = requests.get(url).json()

    return render(
        request,
        "home/index.html",
        {
            "data": data,
            "remaining": remaining,
        },
    )
