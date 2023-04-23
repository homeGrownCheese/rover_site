import requests
import dotenv
import os
import json


from django.shortcuts import render

# load the .env file
dotenv.load_dotenv()


API_KEY = os.getenv("API_KEY")


def home(request):
    # check if the API key is present in the form data
    if "api_key" in request.GET:
        # save the API key to a cookie
        api_key = request.GET["api_key"]
        response = render(request, "home/index.html")
        response.set_cookie("api_key", api_key)

    # load the API key from the cookie or use the default key
    api_key = request.COOKIES.get("api_key", os.getenv("API_KEY"))

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
    remaining = headers["X-RateLimit-Remaining"]
    print(f"Remaining requests: {remaining}")

    data = requests.get(url).json()
    if data == []:
        print("No photos found")

    return render(
        request,
        "home/index.html",
        {
            "data": data,
            "remaining": remaining,
        },
    )
