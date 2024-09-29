from communication.communicator import Communicator
from data_fetcher.database_actions import DatabaseActions
from message.message_generator import MessageGenerator
from message.alert_checker import AlertChecker
from message.alert_generator import AlertGenerator
from tools.utils import Logger
from analysis.analyser_simulation import ram_analyser

class Bot:
    def __init__(self, token, base_url, external_database_url, auxiliary_database_url, team_mattermost):
        self.communicator = Communicator(token, base_url)
        self.external_database = DatabaseActions(external_database_url)
        self.auxiliary_database = DatabaseActions(auxiliary_database_url)
        self.message_generator = MessageGenerator()
        self.alert_generator = AlertGenerator(auxiliary_database_url)
        self.alert_checker = AlertChecker(auxiliary_database_url)
        self.logger = Logger(log_file="bot-mattermost.log")
        self.team_mattermost = team_mattermost

    def analyse(self):
        alert_cases = ram_analyser(self.external_database)
        if alert_cases is None:
            self.logger.info("No resource waste occurrences found.")
            return []
        return alert_cases

    def generate_alert(self, alert_cases):
        for case in alert_cases:
            self.alert_generator.generate_alert(case)
            True

    def check_alerts(self):
        alerts = self.alert_checker.check_alerts()
        if not alerts:
            self.logger.info("No alerts to report.")
            return []
        return alerts

    def send_alerts(self, alerts):
        for alert in alerts:
            message = self.message_generator.generate_message(alert)
            if message:
                channel_name = f"project-{alert['data']['project_name']}"
                channel_id = self.communicator.get_channel_id(channel_name, self.team_mattermost)
                self.communicator.send_message_to_channel(channel_id, message)
                self.logger.info(f"Message sent: {message}")

                updated_data = {
                    'status': 'sent',
                    'data': alert['data']
                }

                response = self.auxiliary_database.update_data(
                    endpoint='api/alerts',
                    alert_id=alert['id'],
                    updated_data=updated_data,
                    headers={"Content-Type": "application/json"}
                )

                if response:
                    self.logger.info(f"Alert with ID {alert['id']} updated successfully.")
                else:
                    self.logger.error(f"Failed to update alert with ID {alert['id']}.")


    def start(self):
        alert_cases = self.analyse()
        if not alert_cases:
            return

        self.generate_alert(alert_cases)
        pending_alerts = self.check_alerts()
        if not pending_alerts:
            return

        self.send_alerts(pending_alerts)
