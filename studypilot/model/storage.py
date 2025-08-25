import os, json, platform

def _app_dir():
    sys = platform.system()
    if sys=="Windows":
        base = os.environ.get("APPDATA", os.path.expanduser("~\\AppData\\Roaming"))
    elif sys=="Darwin":
        base = os.path.expanduser("~/Library/Application Support")
    else:
        base = os.path.expanduser("~/.local/share")
    path = os.path.join(base, "StudyPilotLocal")
    os.makedirs(path, exist_ok=True)
    return path

class AppStorage:
    def __init__(self, app_name:str):
        self.base = _app_dir()
        self.users_json = os.path.join(self.base, "users.json")
        if not os.path.exists(self.users_json):
            with open(self.users_json,"w",encoding="utf-8") as f: json.dump({"users":{}}, f)

    def user_dir(self, username:str):
        p = os.path.join(self.base, username)
        os.makedirs(p, exist_ok=True)
        return p

    def load_users(self)->dict:
        with open(self.users_json,"r",encoding="utf-8") as f: return json.load(f)

    def save_users(self, data:dict):
        with open(self.users_json,"w",encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=2)

    def load_user_data(self, username:str)->dict:
        path = os.path.join(self.user_dir(username), "data.json")
        if not os.path.exists(path):
            data = {"subjects":[{"id":"default","name":"Général","color":"#64748b"}],
                    "events":[], "cycleMap":{}, "horaire":{}, "revision":[]}
            self.save_user_data(username, data)
            return data
        with open(path,"r",encoding="utf-8") as f: return json.load(f)

    def save_user_data(self, username:str, data:dict):
        path = os.path.join(self.user_dir(username), "data.json")
        with open(path,"w",encoding="utf-8") as f: json.dump(data, f, ensure_ascii=False, indent=2)
