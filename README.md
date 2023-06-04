# LOGIN PAGE AND API AUTHORIZER BACKEND 

## Description
This is a login page backend built using FastAPI. This page allows users to register themselves, authenticate themselves using their API and get their credentials.

## Routes

<ol>
<li>

```/register```: Registers a user and creates the user in the MongoDB database. It captures the following fields:
- User name  - user input
- Email – user input
- Expiry date – should be 1 year from register date.
- API – create a 10 digit alpha numeric API key for the user and store it encrypted in DB.
</li> 
<li>

```/user/authenticate```: Authenticates the user on login through swagger UI. Endpoint takes the API key as input and returns appropriate message if it is successful in authorizing. otherwise, an error message is displayed.
</li>
<li>

```/getUserData```: Authorises the user on accessing this url and return user name and email address. It handles error scenarios with appropriate status codes in the following ways:
- ```400``` : User does not exist
- ```402``` : Invalid API key
- ```500``` : Key expired 

## Prerequisites for installation

- Python 3 must be pre-installed in your machine

## Installation guide

- Clone this repository
- Open your terminal and Create a virtual environment using the following: 
`python -m venv env`

  If you do not have virtualenv installed then place the following code in your terminal to install it:
`pip install virtualenv`

- Activate the virtual environment using the following code in your terminal:
`.\env\Scripts\activate`

- Install the required dependencies using the following code in your terminal:
`pip install -r requirements.txt`

- Start the application by typing the following in your terminal:
`python main.py`
