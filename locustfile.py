from locust import HttpUser, task, between

from read_csv import get_number_list


class MyUser(HttpUser):
    wait_time = between(1, 2)

    @task
    def my_task(self):
        v_list = []
        for v_id in get_number_list():
            v_list.append(v_id)
        response = self.client.get(f'/Vehicle/{v_list}')
