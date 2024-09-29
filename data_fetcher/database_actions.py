from tools.utils import Logger
import requests

class DatabaseActions:
    def __init__(self, base_url):
        self.logger = Logger(log_file="bot-mattermost.log")
        self.base_url = base_url

    def get_metrics(self, endpoint, headers=None):
        try:
            url = f"{self.base_url}/{endpoint}"
            self.logger.debug(f"GET request to {url}")
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            self.logger.info(f"Metrics successfully obtained from endpoint '{endpoint}'")
            return response.json()
        except requests.exceptions.RequestException as error:
            self.logger.error(f"Error fetching metrics from endpoint '{endpoint}': {error}")
            return None

    def insert_data(self, endpoint, data, headers=None):
        try:
            url = f"{self.base_url}/{endpoint}"
            self.logger.debug(f"POST request to {url} with data {data}")
            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            self.logger.info(f"Data successfully inserted into endpoint '{endpoint}'")
            return response.json()
        except requests.exceptions.RequestException as error:
            self.logger.error(f"Error inserting data into endpoint '{endpoint}': {error}")
            return None
        
    def update_data(self, endpoint, alert_id, updated_data, headers=None):
        try:
            url = f"{self.base_url}/{endpoint}/{alert_id}"
            self.logger.debug(f"PUT request to {url} with data {updated_data}")
            response = requests.put(url, json=updated_data, headers=headers)
            response.raise_for_status()
            self.logger.info(f"Alert ID {alert_id} successfully updated.")
            return response.json()
        except requests.exceptions.RequestException as e:
            self.logger.error(f"Error updating alert ID {alert_id}: {e}")
            return None
