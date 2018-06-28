from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from flask_socketio import SocketIO
from application.app import app, db, socketio

migrate = Migrate(app, db)
manager = Manager(app)

# migrations
manager.add_command('db', MigrateCommand)


@manager.command
def create_db():
    """Creates the db tables."""
    db.create_all()


if __name__ == '__main__':
    app.config['SECRET_KEY'] = 'secret!'
    socketio.run(app)
