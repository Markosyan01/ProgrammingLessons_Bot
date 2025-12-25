from telebot import TeleBot, types
import sqlite3
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv('TOKEN')
bot = TeleBot(TOKEN)

db = sqlite3.connect("courses.db", check_same_thread=False)
cur = db.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS courses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    center TEXT,
    city TEXT,
    language TEXT,
    direction TEXT,
    price INTEGER,
    duration INTEGER,
    format TEXT
)
""")

cur.execute("DELETE FROM courses")

data = [
    ("PicsArt Academy", "Yerevan", "Python", "Machine Learning", 450000, 5, "Offline"),
    ("Armenian Code Academy", "Yerevan", "Python", "Machine Learning", 520000, 6, "Hybrid"),
    ("EPAM Training Center", "Yerevan", "Python", "Data Science", 0, 4, "Offline"),
    ("ISTC Foundation", "Online", "Python", "Data Science", 300000, 3, "Online"),
    ("DevCenter", "Yerevan", "Python", "Web Development", 400000, 5, "Offline"),
    ("TechLabs", "Online", "Python", "Automation", 350000, 4, "Online"),
    ("DevOps Academy", "Yerevan", "Python", "DevOps", 480000, 6, "Hybrid"),
    ("SysAdmin Institute", "Yerevan", "Python", "Scripting", 420000, 5, "Offline"),

    ("PicsArt Academy", "Yerevan", "JavaScript", "Web Development", 400000, 5, "Offline"),
    ("Armenian Code Academy", "Yerevan", "JavaScript", "Frontend", 450000, 6, "Hybrid"),
    ("EPAM Training Center", "Yerevan", "JavaScript", "Backend", 0, 4, "Offline"),
    ("ISTC Foundation", "Online", "JavaScript", "Backend", 200000, 3, "Online"),
    ("DevCenter", "Yerevan", "JavaScript", "Fullstack", 500000, 6, "Offline"),
    ("TechLabs", "Online", "JavaScript", "Mobile Development", 350000, 4, "Online"),
    ("DevOps Academy", "Yerevan", "JavaScript", "DevOps", 480000, 6, "Hybrid"),
    ("SysAdmin Institute", "Yerevan", "JavaScript", "Testing", 420000, 5, "Offline"),

    ("PicsArt Academy", "Yerevan", "Java", "Backend", 480000, 5, "Offline"),
    ("Armenian Code Academy", "Yerevan", "Java", "Backend", 500000, 6, "Hybrid"),
    ("EPAM Training Center", "Yerevan", "Java", "Android Development", 0, 4, "Offline"),
    ("ISTC Foundation", "Online", "Java", "Android Development", 300000, 3, "Online"),
    ("DevCenter", "Yerevan", "Java", "Spring Framework", 450000, 5, "Offline"),
    ("TechLabs", "Online", "Java", "Microservices", 350000, 4, "Online"),
    ("DevOps Academy", "Yerevan", "Java", "DevOps", 480000, 6, "Hybrid"),
    ("SysAdmin Institute", "Yerevan", "Java", "Testing", 420000, 5, "Offline"),
]

cur.executemany("""
INSERT INTO courses (center, city, language, direction, price, duration, format)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", data)

db.commit()

TEXT = {
    "start": {
        "en": "Choose language:",
        "ru": "Выберите язык:",
        "am": "Ընտրեք լեզուն․"
    },
    "choose_branch": {
        "en": "Choose a field:",
        "ru": "Выберите направление:",
        "am": "Ընտրեք ուղղությունը․"
    },
    "choose_lang": {
        "en": "Choose programming language:",
        "ru": "Выберите язык программирования:",
        "am": "Ընտրեք ծրագրավորման լեզուն․"
    },
    "choose_dir": {
        "en": "Choose direction:",
        "ru": "Выберите направление:",
        "am": "Ընտրեք ուղղությունը․"
    },
    "top": {
        "en": "🏆 Top courses in Armenia:",
        "ru": "🏆 Лучшие курсы в Армении:",
        "am": "🏆 Լավագույն դասընթացները Հայաստանում․"
    },
    "no_courses": {
        "en": "No courses found.",
        "ru": "Курсы не найдены.",
        "am": "Դասընթացներ չեն գտնվել։"
    }
}

user_lang = {}

@bot.message_handler(commands=["start"])
def start(message):
    kb = types.InlineKeyboardMarkup()
    kb.add(
        types.InlineKeyboardButton("🇬🇧 English", callback_data="lang_en"),
        types.InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
        types.InlineKeyboardButton("🇦🇲 Հայերեն", callback_data="lang_am")
    )
    bot.send_message(message.chat.id, TEXT["start"]["en"], reply_markup=kb)

@bot.callback_query_handler(func=lambda c: c.data.startswith("lang_"))
def set_language(call):
    lang = call.data.split("_")[1]
    user_lang[call.from_user.id] = lang

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("💻 Programming", callback_data="programming"))

    bot.send_message(
        call.message.chat.id,
        TEXT["choose_branch"][lang],
        reply_markup=kb
    )

@bot.callback_query_handler(func=lambda c: c.data == "programming")
def choose_language(call):
    lang = user_lang.get(call.from_user.id, "en")

    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("🐍 Python", callback_data="python"))
    kb.add(types.InlineKeyboardButton("🟨 JavaScript", callback_data="javascript"))
    kb.add(types.InlineKeyboardButton("☕ Java", callback_data="java"))

    bot.send_message(
        call.message.chat.id,
        TEXT["choose_lang"][lang],
        reply_markup=kb
    )

@bot.callback_query_handler(func=lambda c: c.data in ["python", "javascript", "java"])
def choose_direction(call):
    lang = user_lang.get(call.from_user.id, "en")

    kb = types.InlineKeyboardMarkup()
    if call.data == "python":
        kb.add(types.InlineKeyboardButton("🤖 Machine Learning", callback_data="ml"))
        kb.add(types.InlineKeyboardButton("🧪 Data Science", callback_data="ds"))
        kb.add(types.InlineKeyboardButton("🌐 Web Development", callback_data="webdev_py"))
        kb.add(types.InlineKeyboardButton("⚙️ Automation", callback_data="automation_py"))
        kb.add(types.InlineKeyboardButton("🛠 DevOps", callback_data="devops_py"))
        kb.add(types.InlineKeyboardButton("📜 Scripting", callback_data="scripting_py"))
    elif call.data == "javascript":
        kb.add(types.InlineKeyboardButton("🌐 Web Development", callback_data="webdev_js"))
        kb.add(types.InlineKeyboardButton("🎨 Frontend", callback_data="frontend_js"))
        kb.add(types.InlineKeyboardButton("🖥 Backend", callback_data="backend_js"))
        kb.add(types.InlineKeyboardButton("📱 Mobile Development", callback_data="mobile_js"))
        kb.add(types.InlineKeyboardButton("🛠 DevOps", callback_data="devops_js"))
        kb.add(types.InlineKeyboardButton("🧪 Testing", callback_data="testing_js"))
    elif call.data == "java":
        kb.add(types.InlineKeyboardButton("🖥 Backend", callback_data="backend_java"))
        kb.add(types.InlineKeyboardButton("🤖 Android Development", callback_data="android_java"))
        kb.add(types.InlineKeyboardButton("🌱 Spring Framework", callback_data="spring_java"))
        kb.add(types.InlineKeyboardButton("⚙️ Microservices", callback_data="microservices_java"))
        kb.add(types.InlineKeyboardButton("🛠 DevOps", callback_data="devops_java"))
        kb.add(types.InlineKeyboardButton("🧪 Testing", callback_data="testing_java"))

    bot.send_message(
        call.message.chat.id,
        TEXT["choose_dir"][lang],
        reply_markup=kb
    )

@bot.callback_query_handler(func=lambda c: c.data in [
    "ml", "ds", "webdev_py", "automation_py", "devops_py", "scripting_py",
    "webdev_js", "frontend_js", "backend_js", "mobile_js", "devops_js", "testing_js",
    "backend_java", "android_java", "spring_java", "microservices_java", "devops_java", "testing_java"
])
def show_courses(call):
    lang = user_lang.get(call.from_user.id, "en")

    direction_map = {
        "ml": "Machine Learning",
        "ds": "Data Science",
        "webdev_py": "Web Development",
        "automation_py": "Automation",
        "devops_py": "DevOps",
        "scripting_py": "Scripting",

        "webdev_js": "Web Development",
        "frontend_js": "Frontend",
        "backend_js": "Backend",
        "mobile_js": "Mobile Development",
        "devops_js": "DevOps",
        "testing_js": "Testing",

        "backend_java": "Backend",
        "android_java": "Android Development",
        "spring_java": "Spring Framework",
        "microservices_java": "Microservices",
        "devops_java": "DevOps",
        "testing_java": "Testing",
    }

    language_map = {
        "ml": "Python",
        "ds": "Python",
        "webdev_py": "Python",
        "automation_py": "Python",
        "devops_py": "Python",
        "scripting_py": "Python",

        "webdev_js": "JavaScript",
        "frontend_js": "JavaScript",
        "backend_js": "JavaScript",
        "mobile_js": "JavaScript",
        "devops_js": "JavaScript",
        "testing_js": "JavaScript",

        "backend_java": "Java",
        "android_java": "Java",
        "spring_java": "Java",
        "microservices_java": "Java",
        "devops_java": "Java",
        "testing_java": "Java",
    }

    direction = direction_map.get(call.data)
    language = language_map.get(call.data)

    cur.execute("""
    SELECT center, price, duration, format
    FROM courses
    WHERE language = ? AND direction = ?
    """, (language, direction))

    courses = cur.fetchall()
    if not courses:
        bot.send_message(call.message.chat.id, TEXT["no_courses"][lang])
        return

    text = TEXT["top"][lang] + "\n\n"

    for center, price, duration, fmt in courses:
        price_text = "Free" if price == 0 else f"{price} AMD"
        duration_text = "—" if duration == 0 else f"{duration} months"

        text += (
            f"🏫 {center}\n"
            f"💰 Price: {price_text}\n"
            f"⏳ Duration: {duration_text}\n"
            f"📍 Format: {fmt}\n\n"
        )

    bot.send_message(call.message.chat.id, text)


bot.polling(none_stop=True)
