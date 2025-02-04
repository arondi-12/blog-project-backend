from app import create_app
import os

# Create the app using the create_app function from __init__.py
app = create_app()

# Run the app
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    print(f"Starting app on 0.0.0.0:{port}")
    app.run(host='0.0.0.0',port=port, debug=True)
