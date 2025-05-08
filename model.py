class index_model:
    def __init__(self, events, user, avatar, menu: str):
        self.events = events
        self.user = user
        self.avatar = avatar
        self.menu = menu
    
    def to_dict(self):
        return {
            "events": self.events,
            "user": self.user,
            "avatar": self.avatar,
            "menu": self.menu
        }
    
class detail_model:
    def __init__(self, event, user, avatar, execute):
        self.event = event
        self.user = user
        self.avatar = avatar
        self.execute = execute
    def to_dict(self):
        return {
            "event": self.event,
            "user": self.user,
            "avatar": self.avatar,
            "execute": self.execute
        }

class login_model:
    def __init__(self, session_data, error :str = ''):
        self.error = error
        self.username = session_data.get('username', '')
        self.password = session_data.get('password', '')
        self.remember = session_data.get('remember', False)

    def to_dict(self):
        return {
            "error": self.error,
            "username": self.username,
            "password": self.password,
            "remember": self.remember
        }
    
class notification_model:
    def __init__(self, events, user, avatar):
        self.events = events
        self.user = user
        self.avatar = avatar
        
    def to_dict(self):
        return {
            "events": self.events,
            "user": self.user,
            "avatar": self.avatar
        }

    