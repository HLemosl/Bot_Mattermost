from tools.utils import Logger
from data_fetcher.database_actions import DatabaseActions

class AlertGenerator:
    def __init__(self, aux_database_url):
        self.logger = Logger(log_file="bot-mattermost.log")
        self.aux_database_actions = DatabaseActions(aux_database_url)

    def generate_alert(self, data):
        try:
            self.logger.info(f"Generating new alert for instance ID: {data['instance_id']}.")
            alert_entry = {
                'status': 'alert',
                'data': data
            }

            self.aux_database_actions.insert_data("api/alerts", alert_entry)
            self.logger.info(f"Alert successfully generated for instance ID: {data['instance_id']}")

        except Exception as e:
            self.logger.error(f"Error generating alert for instance ID: {data['instance_id']}: {e}")
