from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
import jwt

app = FastAPI(title="Company CRM (Тестовий клієнт)")

# ВАЖЛИВО: Цей ключ має бути ІДЕНТИЧНИМ до SSO_SECRET_KEY у вашому Менеджері паролів!
SSO_SECRET_KEY = "a9JgyK6sedNPWk2qcFKu9N1fyWnMIXOBktXTTsdTbCw="

# 1. Головна сторінка CRM (Перевіряє, чи авторизований працівник)
@app.get("/", response_class=HTMLResponse)
async def crm_dashboard(request: Request):
    # Перевіряємо наявність локальної сесії в cookies
    user_login = request.cookies.get("crm_session_user")

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
            <p>Авторизований користувач: <b>{user_login}</b></p>
            <p>Вхід виконано без пароля за допомогою одноразового SSO-токена.</p>
            <br>
            <a href="/logout" style="padding: 10px 20px; background: #dc3545; color: white; text-decoration: none; border-radius: 5px;">
                Вийти з CRM
            </a>
        </body>
    </html>
    """

# 2. Ендпоінт прийому перепустки (Callback) від Менеджера паролів
@app.get("/auth/callback")
async def sso_callback(sso_token: str = None):
    if not sso_token:
        raise HTTPException(status_code=400, detail="Відсутній SSO токен")

    try:
        # Розшифровуємо та перевіряємо підпис і час життя токена (ті самі 30 секунд)
        payload = jwt.decode(sso_token, SSO_SECRET_KEY, algorithms=["HS256"])

        # Перевіряємо, що токен видав саме наш Менеджер паролів
        if payload.get("iss") != "corporate-password-manager":
            raise HTTPException(status_code=403, detail="Невідоме джерело токена")

        user_login = payload.get("sub")

        # Токен валідний! Перенаправляємо на головну сторінку CRM і ставимо куку сесії
        response = RedirectResponse(url="/")
        response.set_cookie(key="crm_session_user", value=user_login, httponly=True)
        return response

    except jwt.ExpiredSignatureError:
        return HTMLResponse(
            "<h1>⏳ Час дії токена вичерпано (30 сек). Спробуйте увійти знову.</h1>",
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
