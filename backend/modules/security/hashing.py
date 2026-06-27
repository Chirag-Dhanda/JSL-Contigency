import bcrypt

class PasswordHasher:
    """Enterprise secure password hashing service."""
    
    def hash_password(self, password: str) -> str:
        """Hashes a plain text password using bcrypt."""
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed.decode('utf-8')
        
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verifies a plain text password against a hash."""
        return bcrypt.checkpw(
            plain_password.encode('utf-8'), 
            hashed_password.encode('utf-8')
        )
