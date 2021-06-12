# Omni Ecommerce

## Prerequisites

- Python v3.9
- Docker v19
- Docker Compose v1.26

## Docker Installation

- Create environment variables:

  - Create `env` files into `envs/local/` directory:

    ```sh
    cp envs/local/.app.env.example envs/local/.app.env && cp envs/local/.db.env.example envs/local/.db.env
    ```
    - Replace default values to the `.envs` values.

- Build services:

  ```sh
  docker-compose build
  ```

- Startup services:

  ```sh
  docker-compose up
  ```

- Create superuser

  ```sh
  docker exec -it django_app python manage.py createsuperuser
  ```