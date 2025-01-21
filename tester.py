from locust import HttpUser, between, task

class WebsiteUser(HttpUser):
    wait_time = between(5, 15)

    def on_start(self):
        self.client.verify = False
        self.client.get("/tasks")

    @task
    def about(self):
        self.client.verify = False
        self.client.get("/")