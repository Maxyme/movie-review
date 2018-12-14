"""manage.py previously used by flask-script. Not sure this is still needed."""
from app import create_app

app = create_app()
app.run()
