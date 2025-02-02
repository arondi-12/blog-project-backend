from app import create_app

# Create the app using the create_app function from __init__.py
app = create_app()

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
