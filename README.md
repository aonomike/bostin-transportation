# boston-transportation
This repository is an implementation of a client side that reads the  Boston transportation system API.

## How to run the program

- Clone this repo from the github repository.
- [Get setup with python version 3 and pip](https://realpython.com/installing-python/)
- Install the dependencies using the command `pip install -r requirements.txt'
- Run the program by typing the following code on your command `python subway_routes.py`

## Set up your .env file
We use a .env file to manage our secrets so they are not shared to the public. Currently, the secret that we want to protect is our API KEY. Follow the steps below to set up your api key.
    1. Copy the content of .env.demo file to a file called .env:
        ```
            cp .env.demo .env
        ```
    2. Update the value of BOSTON_API_KEY to your API Key. If you don't have one, be sure to generate it from [MBTA documentation](https://api-v3.mbta.com/docs/swagger/swagger.json) website.


