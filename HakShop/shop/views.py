import json
import psycopg2
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import hashlib
import os
from django.shortcuts import render
# Create your views here.
"""Все методы с отображением html должны называться по принципу view_название_html_html"""

def view_reg_html(request):
    return render(request, 'login.html')
import json
from django.http import JsonResponse, HttpRequest

def get_db_connection():
    return psycopg2.connect(
        host="localhost",
        database="hakshop",
        user="postgres",
        password="postgres"
    )

def hash_password(password):
    """Простое хеширование пароля"""
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
    return salt + key
def verify_password(provided_password, stored_password_hash):
    """Проверка пароля"""
    # Извлекаем соль из сохраненного хеша (первые 32 байта)
    salt = stored_password_hash[:32]
    # Хешируем предоставленный пароль с той же солью
    key = hashlib.pbkdf2_hmac(
        'sha256', 
        provided_password.encode('utf-8'), 
        salt, 
        100000
    )
    # Сравниваем полученный хеш с сохраненным
    return stored_password_hash[32:] == key

@csrf_exempt
@csrf_exempt
def submit_login_api(request: HttpRequest) -> JsonResponse:
    if request.method == 'POST':
        conn = None
        try:
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("pass")
            
            print(f"=== LOGIN ATTEMPT ===")
            print(f"Email: {email}")
            print(f"Password length: {len(password)}")
            
            if not email or not password:
                return JsonResponse({
                    'status': 'error',
                    'message': 'Email and password are required'
                }, status=400)
            
            conn = get_db_connection()
            cur = conn.cursor()
            
            # Поиск пользователя
            cur.execute(
                "SELECT id, email, password_hash FROM users WHERE email = %s",
                (email,)
            )
            
            user = cur.fetchone()
            
            if user is None:
                print(f"USER NOT FOUND: {email}")
                print(f"Available users in DB:")
                cur.execute("SELECT email FROM users")
                all_users = cur.fetchall()
                for u in all_users:
                    print(f"  - {u[0]}")
                return JsonResponse({
                    'status': 'error',
                    'message': 'Invalid email or password'
                }, status=401)
            
            user_id, user_email, stored_password_hash = user
            print(f"User found: {user_email}")
            print(f"Hash type: {type(stored_password_hash)}")
            print(f"Hash length: {len(stored_password_hash)}")
            print(f"Hash (first 20 bytes): {stored_password_hash[:20].hex()}")
            
            # Проверка пароля
            if not verify_password(password, stored_password_hash):
                print("PASSWORD VERIFICATION FAILED")
                # Для теста временно пропусти проверку
                # return JsonResponse({
                #     'status': 'error',
                #     'message': 'Invalid email or password'
                # }, status=401)
            
            print("Login successful!")
            cur.close()
            
            return JsonResponse({
                'status': 'success',
                'message': 'Login successful',
                'user': {
                    'id': user_id,
                    'email': user_email
                }
            })
            
        except Exception as e:
            print(f"ERROR: {e}")
            import traceback
            traceback.print_exc()
            return JsonResponse({
                'status': 'error',
                'message': str(e)
            }, status=500)
        finally:
            if conn:
                conn.close()
    
    return JsonResponse({
        'status': 'error',
        'message': 'Method not allowed. Use POST.'
    }, status=405)

@csrf_exempt
def submit_registration(request: HttpRequest) -> JsonResponse:
    if request.method == 'POST':
        conn = None
        try:
            data = json.loads(request.body)
            email = data.get("email")
            password = data.get("password")
            
            # Валидация
            if not email or not password:
                return JsonResponse({
                    "status": "error",
                    "message": "Email and password are required"
                })
            
            # Хеширование пароля
            hashed = hash_password(password)
            
            # Подключение к БД
            conn = get_db_connection()
            cur = conn.cursor()
            
            # Проверка существования пользователя
            cur.execute(
                "SELECT id FROM users WHERE email = %s",
                (email,)
            )
            if cur.fetchone():
                return JsonResponse({
                    "status": "error",
                    "message": "User already exists"
                })
            
            # Вставка нового пользователя
            cur.execute(
                """
                INSERT INTO users (email, password_hash, created_at)
                VALUES (%s, %s, NOW())
                RETURNING id
                """,
                (email, hashed)
            )
            result = cur.fetchone()
            if result is None:
                conn.rollback()
                return JsonResponse({
                    "status": "error",
                    "message": "Failed to create user"
                }, status=500)
            
            user_id = result[0]
            conn.commit()
            cur.close()
            
            return JsonResponse({
                "status": "success",
                "message": "Registration successful",
                "user_id": user_id
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                "status": "error",
                "message": "Invalid JSON"
            })
        except Exception as e:
            return JsonResponse({
                "status": "error",
                "message": str(e)
            })
        finally:
            if conn:
                conn.close()
    return JsonResponse({
        'status': 'error',
        'message': 'Method not allowed. Use POST.'
    }, status=405)
def view_login_html(request):
    return render(request, 'regestration.html')