import cloudinary
import cloudinary.uploader
from flask import current_app

class CloudinaryService:
    def __init__(self, app=None):
        self.configured = False
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize with Flask app context"""
        if not all([
            app.config.get('CLOUDINARY_CLOUD_NAME'),
            app.config.get('CLOUDINARY_API_KEY'),
            app.config.get('CLOUDINARY_API_SECRET')
        ]):
            print("Warning: Cloudinary not configured - missing credentials")
            return
            
        cloudinary.config(
            cloud_name=app.config['CLOUDINARY_CLOUD_NAME'],
            api_key=app.config['CLOUDINARY_API_KEY'],
            api_secret=app.config['CLOUDINARY_API_SECRET']
        )
        self.configured = True

    def upload_file(self, file_path, folder=None):
        if not self.configured:
            print("Error: Cloudinary not configured")
            return None
            
        try:
            options = {}
            if folder:
                options['folder'] = folder
            
            response = cloudinary.uploader.upload(file_path, **options)
            return response['secure_url']
        except Exception as e:
            print(f"Error uploading to Cloudinary: {e}")
            return None