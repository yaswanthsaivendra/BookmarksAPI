# BookmarksAPI

An API for all your bookmarks ;)

# Documentation
Base URI of the API : [BookmarksAPI](https://bookmarks-restapi.herokuapp.com/api/v1/) <br>
Base URI : `/api/v1`
 # Authentication
 1. Login : `/api/v1/auth/login`                POST<br>
    JSON Request body:
    ```
    {
    "email":"testuser@mail.com",
    "password":"testuser"
    }
    ```
2. Registration : `/api/v1/auth/register`          POST<br>
    JSON Request body:
    ```
    {
    "username":"testuser",
    "password":"testuser",
    "email":"testuser@mail.com"
    }
    ```
 1. User Personal details : `/api/v1/auth/me`       GET
 2. To get User Refresh token : `/api/v1/auth/token/refresh`        GET
 # Bookmarks


## Local Deployment
1. clone the repo and install the requirements.
2. Setup these enivronment variables :
```
export SECRET_KEY="ThisisT0pS3cr3t"
export JWT_SECRET_KEY="D0ntR3v3alit"
```
3. Run the server :
```
flask run
```

### TODO

API Documentation