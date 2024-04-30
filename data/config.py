from environs import Env

# environs kutubxonasidan foydalanish
env = Env()
env.read_env()

# .env fayl ichidan quyidagilarni o'qiymiz
BOT_TOKEN = env.str("BOT_TOKEN")  # Bot toekn

ADMINS_FROM = env.list("ADMINS")  # adminlar ro'yxati
ADMINS=[]
for admin in ADMINS_FROM:
    try:
        # Convert element to integer if it's a string
        ADMINS.append(int(admin) if isinstance(admin, str) else admin)

    except Exception as e:
        # Handle the case where conversion is not possible
        print(f"Cannot convert {admin} to integer.")
USERS_FROM = env.list("USERS") #userlar ro'yxati
USERS = []
for user in USERS_FROM:
    try:
        # Convert element to integer if it's a string
        USERS.append(int(user) if isinstance(user, str) else user)

    except Exception as e:
        # Handle the case where conversion is not possible
        print(f"Cannot convert {user} to integer.")
IP = env.str("ip")  # Xosting ip manzili
