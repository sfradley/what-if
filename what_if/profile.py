from tinydb import TinyDB, Query
from what_if.prompt import prompt


class ProfileService:
    def __init__(self, db='session.json') -> None:
        self.tdb = TinyDB(db)
        self.user = Query()

    def create_user(self, name):
        self.tdb.insert({'name': name,
                         'chat': prompt.copy(),
                         })

    def check_user(self, name):
        if self.tdb.search(self.user.name == name):
            return
        else:
            self.create_user(name)

    def read_chat(self, name):
        self.check_user(name)
        result = list()
        for item in self.tdb.search(self.user.name == name)[0]['chat']:
            if item['content']:
                result.append(item)
        return result

    def update_chat(self, name, chat):
        self.check_user(name)
        messages = self.tdb.search(self.user.name == name)[0]['chat']
        messages.append(chat)
        self.tdb.update({'chat': messages}, self.user.name == name)

    def update_background(self, name, background):
        self.check_user(name)
        messages = self.tdb.search(self.user.name == name)[0]['chat']
        for i, message in enumerate(messages):
            if message['role'] == 'user':
                messages[i]['user'] = "Background: " + background
                break
        self.tdb.update({'chat': messages},
                        self.user.name == name)

    def reset_chat(self, name):
        self.tdb.remove(self.user.name == name)
