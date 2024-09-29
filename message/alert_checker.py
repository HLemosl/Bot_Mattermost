from tools.utils import Logger
from data_fetcher.database_actions import DatabaseActions

class AlertChecker:
    def __init__(self, aux_database_url):
        self.logger = Logger(log_file="bot-mattermost.log")
        self.database_actions = DatabaseActions(aux_database_url)

    def check_alerts(self):
        try:
            self.logger.info("Checking for pending alerts...")
            alerts = self.database_actions.get_metrics("api/alerts")
            pending_alerts = []

            for alert in alerts:
                if alert['status'] in ['alert', 'error']:
                    alert_data = {
                        'id': alert['id'],
                        'status': alert['status'],
                        'data': alert['data']
                    }
                    pending_alerts.append(alert_data)

            if pending_alerts:
                self.logger.info(f"Found {len(pending_alerts)} alerts pending.")
            else:
                self.logger.info("No pending alerts found.")

            return pending_alerts

        except Exception as e:
            self.logger.error(f"Error checking alerts: {e}")
            return []
