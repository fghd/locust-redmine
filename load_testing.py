from locust import HttpLocust, TaskSet, task
from pyquery import PyQuery
import random

class UserBehavior(TaskSet):

    def on_start(self):
        r = self.client.get("/")
        pq = PyQuery(r.content)
        #parse token on form
        token_input = pq("form input").eq(1)
        token = token_input.attr("value")
        self.client.post("/login", {"username":"username","password":"password","authenticity_token":token})
        self.project_links = ['/projects/testproject', '/projects/newproject']



    @task
    def get_issues(self):
        url = random.choice(self.project_links)+"/issues"
        return self.client.get(url)

    @task(5)
    def show_issue(self):
        issue_list = ['/issues/1', '/issues/2']
        issue = random.choice(issue_list)
        self.client.get(issue)




class WebsuiteUser(HttpLocust):
    task_set = UserBehavior
    min_wait = 3000
    max_wait = 9000
