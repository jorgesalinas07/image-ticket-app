# Image-ticket-app
This application assists users in creating tickets that trigger image uploads to a cloud server provider.

## Setup environment

### Requirements
- **Make**: Please refer to the installation instructions for your operating system.
- **Docker**: Docker Desktop can be a useful tool as well.
- **Docker-compose**

### Add variables

In the root directory, create a file named `.env` with the following values:

```
CLOUDINARY_URL=<insert_CLOUDINARY_API_environment_variable>
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=image_ticket_db
REDIS_URL=redis://redis:6379/0
```
These are the recommended environment variables. It is advisable to use these variables, however, if you choose to change the `REDIS_URL` or `POSTGRES_DB`, please ensure to update these names in the Docker Compose file, specifically in the Redis and database container configurations.

### Development :whale:
In the root of the project, run the following command:
```
make start_project
```
After the command completes, verify that all containers are running as shown in
the following image:

![<docker-compose>](https://i.ibb.co/M1dhN30/docker-compose.png)

This image is taken from docker-desktop.

#### Run database migrations
Once the project is running with Docker, execute the following Docker command to run the migrations:
```
docker exec -it image-ticket-app-backend python3 manage.py migrate
```
You are now ready to proceed.

#### Running Tests
To verify the behavior and functionality of the application, and to identify any errors or potential issues, please run the tests:
```
make test
```

#### API documentation
After the project is running and migrations have been applied, access the API documentation at the following endpoint:
```
http://localhost:8000/docs/
```
This will take you to the Swagger API documentation page. It should appear as shown in the following image:

![swagger-documentation](https://i.ibb.co/516SMfT/swagger-documentation.png)

You can now interact with the application. The documentation contains important information about how to use the app. Please make sure to start by creating a user in the sign-up endpoint and then use the retrieved token to be able to interact with the other endpoints. Otherwise, the endpoints won't be available.

#### Conventional Commit
Please adhere to the following commit message format:

* **Commit**
    ```
    feat: Message Description
    ```
    Example:
    ```
    feat: Implement Create method for Client Status
    ```

- `feat`: Introduce a new feature or modify an existing one
- `fix`: Resolve an issue in the branch
- `docs`: Documentation updates
- `test`: Add new tests
- `refactor`: Technical debt


Please take a look at the merge PR descriptions. You'll find some other functionalities documentations.

Thank you for following these guidelines. I started the project on may 12 2024.
