import os
import unittest

from cryptography.fernet import Fernet

os.environ.setdefault("MYSQL_HOST", "127.0.0.1")
os.environ.setdefault("MYSQL_PORT", "3306")
os.environ.setdefault("MYSQL_DATABASE", "test_db")
os.environ.setdefault("MYSQL_USER", "test_user")
os.environ.setdefault("MYSQL_PASSWORD", "test_password")
os.environ.setdefault("SECRET_KEY", "test-jwt-secret-key-that-is-at-least-32-chars")
os.environ.setdefault("ENCRYPTION_KEY", Fernet.generate_key().decode())
os.environ.setdefault("SSO_SECRET_KEY", "test-sso-secret-key-that-is-at-least-32-chars")
os.environ.setdefault("FRONTEND_URL", "http://localhost:5173")
os.environ.setdefault("DEFAULT_ADMIN_LOGIN", "admin")
os.environ.setdefault("DEFAULT_ADMIN_PASSWORD", "admin-password")

from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.auth.dependencies import get_current_user
from src.auth.router import router as auth_router
from src.credentials.router import router as credentials_router, validate_totp_secret
from src.credentials.schemas import MyAccessCredential
from src.database import get_db
from src.models import User
from src.security import decrypt_password, encrypt_password, verify_password
from src.users.router import router as users_router


class SecurityControlTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.employee = User(
            user_id=42,
            login="employee",
            role="user",
            status="active",
            auth_version=0,
        )
        cls.app = FastAPI()
        cls.app.include_router(auth_router, prefix="/api")
        cls.app.include_router(credentials_router, prefix="/api")
        cls.app.include_router(users_router, prefix="/api")

        async def current_employee():
            return cls.employee

        async def unused_db():
            yield None

        cls.app.dependency_overrides[get_current_user] = current_employee
        cls.app.dependency_overrides[get_db] = unused_db
        cls.client = TestClient(cls.app)

    @classmethod
    def tearDownClass(cls):
        cls.client.close()

    def test_employee_cannot_read_service_secret_detail(self):
        response = self.client.get("/api/services/1/detail")
        self.assertEqual(response.status_code, 403)

    def test_employee_cannot_list_credential_access_users(self):
        response = self.client.get("/api/services/1/credentials/1/access")
        self.assertEqual(response.status_code, 403)

    def test_employee_cannot_change_own_login_or_password(self):
        response = self.client.put("/api/auth/profile", json={"password": "new-password"})
        self.assertEqual(response.status_code, 403)

    def test_employee_cannot_read_another_users_login_password(self):
        response = self.client.get("/api/users/1/login-password")
        self.assertEqual(response.status_code, 403)

    def test_employee_access_list_schema_has_no_secrets(self):
        fields = MyAccessCredential.model_fields
        self.assertNotIn("password", fields)
        self.assertNotIn("protected_password", fields)
        self.assertNotIn("totp_secret", fields)

    def test_fernet_supports_long_unicode_passwords(self):
        password = "пароль" * 100
        protected = encrypt_password(password)
        self.assertGreater(len(protected), 255)
        self.assertEqual(decrypt_password(protected), password)
        self.assertTrue(verify_password(protected, password))
        self.assertFalse(verify_password(protected, "wrong-password"))

    def test_valid_unpadded_base32_totp_secret_is_accepted(self):
        self.assertTrue(validate_totp_secret("JBSWY3DPEHPK3PXP"))


if __name__ == "__main__":
    unittest.main()