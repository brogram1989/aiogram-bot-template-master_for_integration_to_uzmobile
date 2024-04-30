from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
#BOT_TOKEN = env.str("BOT_TOKEN")  # Bot token
#yuqoridagisi localhost uchun, quyidagisi railway uchun
BOT_TOKEN = '6478730802:AAFQAqoHhinx4XLOMzcAXu82GhlibsrNMLA'  # Bot token
#localhost uchun adminlar ro'yxati
#ADMINS_FROM = env.list("ADMINS")  # adminlar ro'yxati
#railway app uchun qismi
ADMINS_FROM = [7065729817,524229810,7148487281]
ADMINS=[]
for admin in ADMINS_FROM:
    try:
        # Convert element to integer if it's a string
        ADMINS.append(int(admin) if isinstance(admin, str) else admin)

    except Exception as e:
        # Handle the case where conversion is not possible
        print(f"Cannot convert {admin} to integer.")

#localhost uchun userlar ro'yxati
#USERS_FROM = env.list("USERS") #userlar ro'yxati
#railway app uchun qismi
USERS_FROM = [7065729817,524229810,7148487281]
USERS = []
for user in USERS_FROM:
    try:
        # Convert element to integer if it's a string
        USERS.append(int(user) if isinstance(user, str) else user)

    except Exception as e:
        # Handle the case where conversion is not possible
        print(f"Cannot convert {user} to integer.")
IP = env.str("ip")  # Xosting ip manzili
