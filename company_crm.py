import html
import os
import threading
import time
from urllib.parse import parse_qs

from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
import jwt

app = FastAPI(title="Company CRM (Тестовий клієнт)")

SSO_SECRET_KEY = os.environ["SSO_SECRET_KEY"]
SSO_AUDIENCE = os.environ.get("SSO_AUDIENCE", "http://localhost:8001/auth/callback")
used_tokens: dict[str, float] = {}
used_tokens_lock = threading.Lock()

# 1. Головна сторінка CRM (Перевіряє, чи авторизований працівник)
@app.get("/", response_class=HTMLResponse)
async def crm_dashboard(request: Request):
    # Перевіряємо наявність локальної сесії в cookies
    session_token = request.cookies.get("crm_session_user")
    user_login = None
    if session_token:
        try:
            session = jwt.decode(
                session_token,
                SSO_SECRET_KEY,
                algorithms=["HS256"],
                audience="company-crm-session",
                issuer="company-crm",
                options={"require": ["exp", "aud", "iss", "sub"]},
            )
            user_login = session.get("sub")
        except jwt.InvalidTokenError:
            user_login = None

    if not user_login:
        # Якщо сесії немає — показуємо заглушку (звичайний вхід за паролем вимкнено!)
        return """
        <html>
            <body style="font-family: sans-serif; text-align: center; margin-top: 100px;">
                <h1 style="color: #d9534f;">⛔ Доступ до Company CRM закрито</h1>
                <p>Прямий вхід за логіном та паролем заборонено політикою безпеки.</p>
                <p>Будь ласка, увійдіть через ваш <b>Корпоративний Менеджер Паролів</b>.</p>
            </body>
        </html>
        """

    # Якщо сесія валідна — пускаємо всередину
    return f"""
    <html>
        <body style="font-family: sans-serif; text-align: center; margin-top: 100px;">
            <h1 style="color: #28a745;">✅ Ви успішно увійшли в Company CRM!</h1>
            <p>Авторизований користувач: <b>{html.escape(user_login or '')}</b></p>
            <p>Вхід виконано без пароля за допомогою одноразового SSO-токена.</p>
            <br>
            <a href="/logout" style="padding: 10px 20px; background: #dc3545; color: white; text-decoration: none; border-radius: 5px;">
                Вийти з CRM
            </a>
        </body>
    </html>
    """

# 2. Ендпоінт прийому перепустки (Callback) від Менеджера паролів
@app.post("/auth/callback")
async def sso_callback(request: Request):
    form = parse_qs((await request.body()).decode("utf-8"))
    sso_token = form.get("sso_token", [None])[0]
    if not sso_token:
        raise HTTPException(status_code=400, detail="Відсутній SSO токен")

    try:
        payload = jwt.decode(
            sso_token,
            SSO_SECRET_KEY,
            algorithms=["HS256"],
            audience=SSO_AUDIENCE,
            issuer="corporate-password-manager",
            options={"require": ["exp", "aud", "iss", "sub", "jti"]},
        )
        jti = payload["jti"]
        now = time.time()
        with used_tokens_lock:
            for token_id, expires in list(used_tokens.items()):
                if expires <= now:
                    del used_tokens[token_id]
            if jti in used_tokens:
                raise HTTPException(status_code=403, detail="SSO токен уже використано")
            used_tokens[jti] = float(payload["exp"])

        session_token = jwt.encode(
            {
                "sub": payload["sub"],
                "iss": "company-crm",
                "aud": "company-crm-session",
                "exp": int(now + 8 * 60 * 60),
            },
            SSO_SECRET_KEY,
            algorithm="HS256",
        )
        response = RedirectResponse(url="/", status_code=303)
        response.set_cookie(
            key="crm_session_user",
            value=session_token,
            httponly=True,
            secure=os.environ.get("COOKIE_SECURE", "false").lower() == "true",
            samesite="lax",
            max_age=8 * 60 * 60,
        )
        return response

    except jwt.ExpiredSignatureError:
        return HTMLResponse(
            "<h1>⏳ Час дії токена вичерпано. Спробуйте увійти знову.</h1>",
            status_code=401
        )
    except jwt.InvalidTokenError:
        return HTMLResponse(
            "<h1>❌ Недійсний або підроблений SSO токен!</h1>",
            status_code=403
        )

# 3. Вихід із системи
@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie("crm_session_user")
    return response
