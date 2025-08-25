import secrets, hashlib
from .storage import AppStorage

class AuthManager:
    def __init__(self, storage:AppStorage):
        self.storage = storage

    def _hash(self, password:str, salt:bytes=None):
        if salt is None: salt = secrets.token_bytes(16)
        dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 200_000, dklen=32)
        return salt.hex()+"$"+dk.hex()

    def _verify(self, password:str, stored:str)->bool:
        try:
            salt_hex, dk_hex = stored.split("$")
            salt = bytes.fromhex(salt_hex)
            dk2 = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 200_000, dklen=32).hex()
            return secrets.compare_digest(dk2, dk_hex)
        except Exception:
            return False

    def list_users(self):
        data = self.storage.load_users()
        return sorted(list(data.get("users", {}).keys()))

    def create_user(self, username:str, password:str):
        username = username.strip()
        if not username: raise ValueError("Nom vide")
        data = self.storage.load_users()
        if username in data.get("users", {}): raise ValueError("Existe déjà")
        data["users"][username] = {"pass": self._hash(password)}
        self.storage.save_users(data)

    def delete_user(self, username:str):
        data = self.storage.load_users()
        if username in data.get("users", {}):
            del data["users"][username]
            self.storage.save_users(data)

    def verify_password(self, username:str, password:str)->bool:
        data = self.storage.load_users()
        rec = data.get("users", {}).get(username)
        if not rec: return False
        return self._verify(password, rec.get("pass",""))
