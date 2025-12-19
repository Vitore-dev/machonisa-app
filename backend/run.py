from app import create_app, db
from flask_migrate import Migrate

app = create_app()
migrate = Migrate(app, db)

from app import db, create_app
app = create_app()
with app.app_context():
    db.create_all()

@app.route('/test')
def test_route():
    return "Flask is working!"



if __name__ == '__main__':
    app.run(debug=True)
