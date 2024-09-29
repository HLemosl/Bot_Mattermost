from tools.utils import Logger

class MessageGenerator:
    def __init__(self):
        self.logger = Logger(log_file="bot-mattermost.log")
        pass

    def generate_message(self, data):
        print(data)
        try:
            project_name = data['data']['project_name']
            creator_name = data['data']['creator_name']
            instance_name = data['data']['instance_name']
            instance_id = data['data']['instance_id']
            flavor_name = data['data']['flavor_name']
            uptime = data['data']['uptime']
            alert = data['data']['alert_reason']

            message = (
                f"**Instance(s) of project '{project_name}' with resource wastage:**\n\n"
                f"**Created by:** {creator_name}\n"
                f"**Instance Name:** {instance_name}\n"
                f"**ID:** {instance_id}\n"
                f"**Flavor:** {flavor_name}\n"
                f"**Uptime:** {uptime}\n"
                f"**Alert:** {alert}\n"
            )

            return message
        except KeyError as e:
            self.logger.error(f"Error generating message: missing key {e}")
            return None
