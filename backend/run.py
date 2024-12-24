from app import create_app  # Import create_app function from __init__.py

app = create_app()  # Create the Flask app instance

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)  # Run the app, ensure this uses values we want