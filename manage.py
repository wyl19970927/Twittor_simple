from flask_script import Manager
from flask_migrate import MigrateCommand
from twittor import create_app

app = create_app
manager = Manager(app)
manager.add_command('db',MigrateCommand ) #在使用db这个命令（command）之前，需要用MigrateCommand将db集成进来

if __name__ == '__main__':
    manager.run()