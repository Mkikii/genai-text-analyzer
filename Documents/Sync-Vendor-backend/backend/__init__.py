from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
from backend.config import Config
from backend.services.cloudinary_service import CloudinaryService
from backend.services.email_service import EmailService
from backend.services.algolia_service import AlgoliaService
import os

db = SQLAlchemy()
ma = Marshmallow()
jwt = JWTManager()
migrate = Migrate()

# Initialize services (will be configured with app later)
cloudinary_service = CloudinaryService()
email_service = EmailService()
algolia_service = AlgoliaService()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Get frontend URL from environment or use defaults
    frontend_url = os.getenv('FRONTEND_URL', 'https://chic-kashata-589433.netlify.app')
    
    CORS(app, resources={
        r"/api/*": {
            "origins": [
                frontend_url,
                "http://localhost:3000",
                "http://localhost:5173"
            ],
            "methods": ["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],
            "allow_headers": ["Content-Type", "Authorization"],
            "supports_credentials": True
        }
    })

    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)

    # Initialize services with app context
    with app.app_context():
        cloudinary_service.init_app(app)
        email_service.init_app(app)
        algolia_service.init_app(app)

    # Make services accessible via app
    app.cloudinary_service = cloudinary_service
    app.email_service = email_service
    app.algolia_service = algolia_service

    from backend.resources.auth import Login, Register
    from backend.resources.dashboard import Dashboard
    from backend.resources.document import DocumentResource
    from backend.resources.order import OrderResource, OrderAssignmentResource, OrderVendorResource
    from backend.resources.quote import QuoteResource
    from backend.resources.search import SearchResource
    from backend.resources.user import UserResource
    from backend.resources.vendor import VendorResource
    from backend.resources.requirement import RequirementResource
    from backend.resources.vendor_category import VendorCategoryResource
    from backend.resources.role import RoleResource

    api = Api(app)

    api.add_resource(Login, "/api/login")
    api.add_resource(Register, "/api/register")
    api.add_resource(Dashboard, "/api/dashboard")
    api.add_resource(DocumentResource, "/api/documents")
    api.add_resource(OrderResource, "/api/orders", "/api/orders/<int:id>")
    api.add_resource(OrderAssignmentResource, "/api/order-assignments", "/api/order-assignments/<int:assignment_id>")
    api.add_resource(OrderVendorResource, "/api/vendor-orders")
    api.add_resource(QuoteResource, "/api/quotes", "/api/quotes/<int:id>")
    api.add_resource(SearchResource, "/api/search")
    api.add_resource(UserResource, "/api/users", "/api/users/<int:id>")
    api.add_resource(VendorResource, "/api/vendors", "/api/vendors/<int:id>")
    api.add_resource(RequirementResource, "/api/requirements", "/api/requirements/<int:id>")
    api.add_resource(VendorCategoryResource, "/api/vendor-categories", "/api/vendor-categories/<int:id>")
    api.add_resource(RoleResource, "/api/roles")

    @app.route("/")
    def index():
        return jsonify({
            "message": "Vendor Sync Backend is running!",
            "version": "1.0",
            "endpoints": "/api/health"
        })

    @app.route("/api/health")
    def health_check():
        return jsonify({
            "status": "ok",
            "message": "Backend running successfully",
            "services": {
                "cloudinary": cloudinary_service.configured,
                "sendgrid": email_service.sg is not None,
                "algolia": algolia_service.client is not None
            }
        }), 200

    return app
```

### 5. **Fix `Procfile` (Capital P!)**

Rename `procfile` to `Procfile`:
```
web: gunicorn wsgi:app