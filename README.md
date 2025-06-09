# task-tracker
A DevOps exploration project building a containerized task tracker using FastAPI, Nginx, and Docker. Focused on CI/CD, microservices, and modern tooling.

# Progress
- [ ] task-service (The API for task-related actions)
    - [x] Add basic functionalities (listing, adding, deleting)
    - [x] Add database integration (Postgresql)
    - [ ] Add timestamp for deadline feature
    - [ ] Add notification system for tasks nearing deadlines
- [ ] user-service (The API for authentication, still unsure if feature is needed, especially if it is made for my own use)
- [ ] Hosting? Perhaps in the long run for personal use
- [ ] Frontend (Current implementation uses curl to send requests)
    - [ ] Maybe can start with simple CLI script

# How to run
Current implementation only has API for listing, adding and deleting tasks with Postgresql for database integration.

In root directory, run `docker-compose up --build`