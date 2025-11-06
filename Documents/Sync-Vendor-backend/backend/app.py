from backend import create_app, db

app = create_app()

if __name__ == "__main__":
    # Move debug config inside here (only for local development)
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    app.config['DEBUG_TB_PORT'] = 5000
    app.config['DEBUG_TB_HOST'] = 'localhost'
    app.config['DEBUG_TB_ENABLED'] = True
    
    with app.app_context():
        db.create_all()
    app.run(host="0.0.0.0", port=5000, debug=True)