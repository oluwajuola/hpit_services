import os
from hpit.server.app import ServerApp
app_instance = ServerApp.get_instance()
app = app_instance.app
db = app_instance.db
mongo = app_instance.mongo

from hpit.management.settings_manager import SettingsManager
settings = SettingsManager.get_server_settings()

class Command:
    description = "Indexes the Mongo Database."
    
    def __init__(self, manager, parser):
        self.manager = manager

    def run(self, arguments, configuration):
        self.arguments = arguments
        self.configuration = configuration

        with app.app_context():
            mongo.db.plugin_messages.create_index('receiver_entity_id')
            mongo.db.sent_messages_and_transactions.create_index([
                ("receiver_entity_id", -1),
                ("message_id", 1)
            ])
            mongo.db.responses.create_index('receiver_entity_id')

        print("DONE! - Indexed the mongo database.")