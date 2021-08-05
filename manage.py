from os import name
from app import create_app
from models import Actor, Movie, db
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand

app = create_app()
migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)


@manager.command
def seed():
    actor1 = Actor(name='Nemo', age='29', gender='Female')
    actor2 = Actor(name='Basil', age='22', gender='Male')
    actor1.insert()
    actor2.insert()

    movie1 = Movie(title='Ice Land', releaseDate='2020/1/1')
    movie2 = Movie(title='Fire', releaseDate='2014/4/3')
    movie1.insert()
    movie2.insert()


if __name__ == '__main__':
    manager.run()
