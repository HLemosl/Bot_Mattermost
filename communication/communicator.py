from tools.utils import Logger
import requests

class Communicator:
    def __init__(self, token, base_url):
        self.logger = Logger(log_file="bot-mattermost.log")
        self.base_url = base_url
        self.headers = {'Authorization': f'Bearer {token}'}

    def get_team_id(self, search_term):
        try:
            url = f"{self.base_url}/api/v4/teams/name/{search_term}"
            self.logger.debug(f"Searching for team with term '{search_term}'")
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            self.logger.info(f"Team '{search_term}' found")
            team = response.json()
            self.logger.info(f"Team ID for '{search_term}' obtained successfully")
            return team['id']
        except requests.exceptions.RequestException as error:
            self.logger.error(f"Error searching for team '{search_term}': {error}")
            return None

    def get_channel_id(self, search_term, team_name):
        try:
            team_id = self.get_team_id(team_name)
            url = f"{self.base_url}/api/v4/teams/{team_id}/channels"
            self.logger.debug(f"Searching for channel with term '{search_term}'")
            response = requests.get(url, headers=self.headers, params={'name': search_term})
            response.raise_for_status()
            channels = response.json()

            for channel in channels:
                if channel['name'] == search_term or channel['display_name'] == search_term:
                    self.logger.info(f"Channel ID for '{search_term}' obtained successfully")
                    return channel['id']
            self.logger.error(f"Channel ID for '{search_term}' were not found")
            return None
        except requests.exceptions.RequestException as error:
            self.logger.error(f"Error searching for channel '{search_term}': {error}")
            return None

    def send_message_to_channel(self, channel_id, message):
        try:
            url = f"{self.base_url}/api/v4/posts"
            payload = {'channel_id': channel_id, 'message': message}
            self.logger.debug(f"Sending message to channel ID '{channel_id}'")
            response = requests.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            self.logger.info(f"Message sent to channel ID '{channel_id}'")
            return response.json()
        except requests.exceptions.RequestException as error:
            self.logger.error(f"Error sending message to channel '{channel_id}': {error}")
            return None
