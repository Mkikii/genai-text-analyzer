from algoliasearch.search_client import SearchClient
from flask import current_app

class AlgoliaService:
    def __init__(self, app=None):
        self.client = None
        self.index = None
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize with Flask app context"""
        if not app.config.get('ALGOLIA_ENABLED', False):
            return
            
        self.client = SearchClient.create(
            app.config['ALGOLIA_APP_ID'],
            app.config['ALGOLIA_API_KEY']
        )
        self.index = self.client.init_index('vendorsync_index')

    def add_record(self, record):
        if self.index:
            self.index.save_object(record).wait()

    def update_record(self, record):
        if self.index:
            self.index.partial_update_object(record).wait()

    def delete_record(self, object_id):
        if self.index:
            self.index.delete_object(object_id).wait()