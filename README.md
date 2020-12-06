# boston-transportation

## set up your .env file
We use a .env file to manage our secrets so they are not shared to the public. Currently, the secret that we want to protect is our API KEY. Follow the steps below to set up your api key.
    1. Copy the content of .env.demo file to a file called .env:
        ```
            cp .env.demo .env
        ```
    2. Update the value of BOSTON_API_KEY to your API Key. If you don't have one, be sure to generate it from [MBTA documentation](https://api-v3.mbta.com/docs/swagger/swagger.json) website.
