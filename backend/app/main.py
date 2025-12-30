from fastapi import FastAPI
from sqlalchemy import create_engine, func
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy import Column, Integer, String
from enum import Enum
from fastapi.middleware.cors import CORSMiddleware



# URL адрес нашей бд, и создание движка для подключения
SQLALCHEMY_DB_URL = "sqlite:///courses_app.db"

engine = create_engine(SQLALCHEMY_DB_URL, connect_args={"check_same_thread": False})

# Создание базовой модели, из которого потом все будет наследоваться
Base = declarative_base()


# Класс категорий, чтобы был только определенный выбор
class Category(str, Enum):
    Programming = "Программирование"
    Design = "Дизайн"
    Data_sciense = "Дата аналитика"

#Главная модель курса
class Course(Base):
    __tablename__ = "Courses"
    id = Column(Integer, index=True, primary_key=True)
    name = Column(String)
    description = Column(String)
    price = Column(Integer)
    category = Column(String)
    customers = Column(Integer)
    image = Column(String)

# Создание таблиц в бд если ее не существует
Base.metadata.create_all(bind=engine)

# Создание локальной сессии, чтобы обращаться к бд
SessionLocal = sessionmaker(autoflush=False, bind=engine)

# Объект класса сессии
db = SessionLocal()

# Само приложение
app = FastAPI()

# Добавление cors для связи фронта с бэком
app.add_middleware(
    CORSMiddleware,
    allow_origins = ["http://localhost:5173"],
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"],
)
# Удаление курса по его ID
@app.delete("/courses/delete/{id}")
def delete_course(id:int):
    course = db.query(Course).get(id)
    if not course:
        return {f"message: Курс с {id} id не найден "}
    db.delete(course)
    db.commit()
    return f"Курс по {id} успешно удален!"

# Удаление всех курсов
@app.delete("/courses/delete")
def delete_all():
    courses = db.query(Course).delete()
    db.commit()
    return {"Message:Все курсы удалены!"}

# API endpoint и query параметры с фильтрацией
@app.get("/courses")
def get_courses(
    search: str = None,
    category: Category | None=None,
    min_price: int = None,
    max_price: int = None,
    sort: str = None,
    page: int = 1,
    limit: int = 12
):
    response = db.query(Course)
    
    if search:
        search_term = f"%{search.strip().lower()}%"
        response = response.filter(func.lower(func.trim(Course.name)).like(search_term))
    if category:
        response = response.filter(Course.category == category.value)
    if sort == "price_asc":
        response = response.order_by(Course.price.asc())
    if sort == "price_desc":
        response = response.order_by(Course.price.desc())
    if sort == "popularity":
        response = response.order_by(Course.customers.desc())
    # Сколько скипать на определенной странице, допустим на 2 странице, скипаем 6 прошлых курсов 
    skip = (page - 1) * limit

    response = response.offset(skip).limit(limit)

    result = response.all()
    return result

# # Просто данные для примера
# courses_data = [
# # Программирование 20 примеров
# {"name": "Python с нуля", "description": "Основы языка и синтаксиса", "price": 22000, "category": "Программирование", "customers": 85, "image": "/templates/img/IT1.jpeg"},
# {"name": "React для начинающих", "description": "Создание SPA приложений", "price": 25000, "category": "Программирование", "customers": 73, "image": "/templates/img/IT1.jpeg"},
# {"name": "FastAPI продвинутый курс", "description": "Создание backend сервисов", "price": 31000, "category": "Программирование", "customers": 54, "image": "/templates/img/IT1.jpeg"},
# {"name": "Основы TypeScript", "description": "Типизация JavaScript приложений", "price": 24000, "category": "Программирование", "customers": 68, "image": "/templates/img/IT1.jpeg"},
# {"name": "Node.js и Express", "description": "Создание серверов и API", "price": 27000, "category": "Программирование", "customers": 61, "image": "/templates/img/IT1.jpeg"},
# {"name": "Vue 3 — полный курс", "description": "Компоненты и Composition API", "price": 26000, "category": "Программирование", "customers": 59, "image": "/templates/img/IT1.jpeg"},
# {"name": "Django REST Framework", "description": "Backend на Python", "price": 30000, "category": "Программирование", "customers": 72, "image": "/templates/img/IT1.jpeg"},
# {"name": "Алгоритмы и структуры данных", "description": "Подготовка к собеседованиям", "price": 28000, "category": "Программирование", "customers": 44, "image": "/templates/img/IT1.jpeg"},
# {"name": "HTML и CSS с нуля", "description": "Верстка и адаптивный дизайн", "price": 18000, "category": "Программирование", "customers": 112, "image": "/templates/img/IT1.jpeg"},
# {"name": "Git и командная разработка", "description": "Работа с ветками и репозиториями", "price": 11000, "category": "Программирование", "customers": 140, "image": "/templates/img/IT1.jpeg"},
# {"name": "Java для начинающих", "description": "ООП и базовые конструкции", "price": 26000, "category": "Программирование", "customers": 77, "image": "/templates/img/IT1.jpeg"},
# {"name": "C# и .NET основы", "description": "Разработка приложений", "price": 27000, "category": "Программирование", "customers": 64, "image": "/templates/img/IT1.jpeg"},
# {"name": "Kotlin для Android", "description": "Создание мобильных приложений", "price": 29000, "category": "Программирование", "customers": 58, "image": "/templates/img/IT1.jpeg"},
# {"name": "Python OOP на практике", "description": "Классы, наследование, паттерны", "price": 25000, "category": "Программирование", "customers": 63, "image": "/templates/img/IT1.jpeg"},
# {"name": "Тестирование и PyTest", "description": "Unit-тесты и автоматизация", "price": 20000, "category": "Программирование", "customers": 71, "image": "/templates/img/IT1.jpeg"},
# {"name": "WebSockets и реальное время", "description": "Чаты и лайв-обновления", "price": 32000, "category": "Программирование", "customers": 46, "image": "/templates/img/IT1.jpeg"},
# {"name": "Микросервисы на FastAPI", "description": "Архитектура и деплой", "price": 35000, "category": "Программирование", "customers": 39, "image": "/templates/img/IT1.jpeg"},
# {"name": "Асинхронный Python", "description": "asyncio, aiohttp, uvicorn", "price": 30000, "category": "Программирование", "customers": 52, "image": "/templates/img/IT1.jpeg"},
# {"name": "Express + MongoDB", "description": "REST API и база данных", "price": 26000, "category": "Программирование", "customers": 67, "image": "/templates/img/IT1.jpeg"},
# {"name": "Fullstack на React и FastAPI", "description": "Frontend + Backend связка", "price": 38000, "category": "Программирование", "customers": 48, "image": "/templates/img/IT1.jpeg"},

# # Дата аналитика 20 примеров
# {"name": "SQL для аналитиков", "description": "Запросы, агрегаты и соединения", "price": 19000, "category": "Дата аналитика", "customers": 92, "image": "/templates/img/IT1.jpeg"},
# {"name": "Power BI — визуализация данных", "description": "Дашборды и отчёты", "price": 23000, "category": "Дата аналитика", "customers": 78, "image": "/templates/img/IT1.jpeg"},
# {"name": "Python для анализа данных", "description": "Pandas, NumPy, графики", "price": 24000, "category": "Дата аналитика", "customers": 88, "image": "/templates/img/IT1.jpeg"},
# {"name": "A/B-тестирование", "description": "Метрики и статистика", "price": 21000, "category": "Дата аналитика", "customers": 66, "image": "/templates/img/IT1.jpeg"},
# {"name": "Фундамент статистики", "description": "Вероятность и распределения", "price": 20000, "category": "Дата аналитика", "customers": 57, "image": "/templates/img/IT1.jpeg"},
# {"name": "Excel — продвинутый уровень", "description": "Формулы и анализ данных", "price": 17000, "category": "Дата аналитика", "customers": 105, "image": "/templates/img/IT1.jpeg"},
# {"name": "Data Engineering основы", "description": "ETL процессы и пайплайны", "price": 32000, "category": "Дата аналитика", "customers": 49, "image": "/templates/img/IT1.jpeg"},
# {"name": "SQL оптимизация запросов", "description": "Индексы и производительность", "price": 22000, "category": "Дата аналитика", "customers": 63, "image": "/templates/img/IT1.jpeg"},
# {"name": "Machine Learning базовый", "description": "Классификация и регрессия", "price": 34000, "category": "Дата аналитика", "customers": 52, "image": "/templates/img/IT1.jpeg"},
# {"name": "Data Visualization в Python", "description": "Matplotlib и Plotly", "price": 21000, "category": "Дата аналитика", "customers": 74, "image": "/templates/img/IT1.jpeg"},
# {"name": "Продуктовая аналитика", "description": "Метрики и когортный анализ", "price": 30000, "category": "Дата аналитика", "customers": 58, "image": "/templates/img/IT1.jpeg"},
# {"name": "BigQuery и аналитика данных", "description": "Работа с облачными хранилищами", "price": 28000, "category": "Дата аналитика", "customers": 45, "image": "/templates/img/IT1.jpeg"},
# {"name": "Airflow и оркестрация данных", "description": "Построение пайплайнов", "price": 36000, "category": "Дата аналитика", "customers": 37, "image": "/templates/img/IT1.jpeg"},
# {"name": "SQL + Python совместно", "description": "Автоматизация отчетов", "price": 26000, "category": "Дата аналитика", "customers": 69, "image": "/templates/img/IT1.jpeg"},
# {"name": "Data Cleaning и подготовка", "description": "Очистка и нормализация данных", "price": 20000, "category": "Дата аналитика", "customers": 83, "image": "/templates/img/IT1.jpeg"},
# {"name": "Финансовая аналитика", "description": "Кейсы и бизнес-метрики", "price": 31000, "category": "Дата аналитика", "customers": 42, "image": "/templates/img/IT1.jpeg"},
# {"name": "Продвинутая статистика", "description": "Гипотезы и корреляция", "price": 27000, "category": "Дата аналитика", "customers": 55, "image": "/templates/img/IT1.jpeg"},
# {"name": "SQL хранилища данных", "description": "Факты и измерения", "price": 29000, "category": "Дата аналитика", "customers": 48, "image": "/templates/img/IT1.jpeg"},
# {"name": "BI-аналитика на практике", "description": "От отчёта до инсайта", "price": 25000, "category": "Дата аналитика", "customers": 64, "image": "/templates/img/IT1.jpeg"},
# {"name": "Data Science старт", "description": "Основы анализа и моделей", "price": 33000, "category": "Дата аналитика", "customers": 51, "image": "/templates/img/IT1.jpeg"},

# # Дизайн 20 примеров
# {"name": "UX/UI дизайн с нуля", "description": "Основы интерфейсов и прототипы", "price": 26000, "category": "Дизайн", "customers": 81, "image": "/templates/img/IT1.jpeg"},
# {"name": "Figma для начинающих", "description": "Макеты и компоненты", "price": 20000, "category": "Дизайн", "customers": 122, "image": "/templates/img/IT1.jpeg"},
# {"name": "Motion-дизайн", "description": "Анимации и графические эффекты", "price": 30000, "category": "Дизайн", "customers": 47, "image": "/templates/img/IT1.jpeg"},
# {"name": "3D-моделирование в Blender", "description": "Создание объектов и сцен", "price": 27000, "category": "Дизайн", "customers": 58, "image": "/templates/img/IT1.jpeg"},
# {"name": "Дизайн мобильных приложений", "description": "UX-паттерны и навигация", "price": 25000, "category": "Дизайн", "customers": 52, "image": "/templates/img/IT1.jpeg"},
# {"name": "Иконки и иллюстрации", "description": "Цифровая графика", "price": 16000, "category": "Дизайн", "customers": 84, "image": "/templates/img/IT1.jpeg"},
# {"name": "Web-дизайн на практике", "description": "Современные UI-решения", "price": 28000, "category": "Дизайн", "customers": 56, "image": "/templates/img/IT1.jpeg"},
# {"name": "Баннеры и рекламный дизайн", "description": "Композиция и типографика", "price": 18000, "category": "Дизайн", "customers": 69, "image": "/templates/img/IT1.jpeg"},
# {"name": "Дизайн презентаций", "description": "Визуальные коммуникации", "price": 15000, "category": "Дизайн", "customers": 91, "image": "/templates/img/IT1.jpeg"},
# {"name": "Фирменный стиль и брендинг", "description": "Логотипы и айдентика", "price": 29000, "category": "Дизайн", "customers": 39, "image": "/templates/img/IT1.jpeg"},
# {"name": "Landing-page дизайн", "description": "Структура и конверсия", "price": 21000, "category": "Дизайн", "customers": 72, "image": "/templates/img/IT1.jpeg"},
# {"name": "Типографика в дизайне", "description": "Работа со шрифтами", "price": 17000, "category": "Дизайн", "customers": 66, "image": "/templates/img/IT1.jpeg"},
# {"name": "UI-киты и дизайн-системы", "description": "Компоненты и гайдлайны", "price": 26000, "category": "Дизайн", "customers": 53, "image": "/templates/img/IT1.jpeg"},
# {"name": "Illustrator для дизайнеров", "description": "Векторная графика", "price": 24000, "category": "Дизайн", "customers": 61, "image": "/templates/img/IT1.jpeg"},
# {"name": "Photoshop для веб-дизайна", "description": "Обработка и ретушь", "price": 20000, "category": "Дизайн", "customers": 75, "image": "/templates/img/IT1.jpeg"},
# {"name": "Промышленный дизайн основы", "description": "Формы и концепции", "price": 32000, "category": "Дизайн", "customers": 34, "image": "/templates/img/IT1.jpeg"},
# {"name": "Гейм-арт и интерфейсы", "description": "UI для игр", "price": 30000, "category": "Дизайн", "customers": 41, "image": "/templates/img/IT1.jpeg"},
# {"name": "Анимация интерфейсов", "description": "Микро-взаимодействия", "price": 27000, "category": "Дизайн", "customers": 49, "image": "/templates/img/IT1.jpeg"},
# {"name": "UX-исследования", "description": "Интервью и тестирование", "price": 29000, "category": "Дизайн", "customers": 45, "image": "/templates/img/IT1.jpeg"},
# {"name": "Продвинутый web-дизайн", "description": "Сложные интерфейсы", "price": 34000, "category": "Дизайн", "customers": 37, "image": "/templates/img/IT1.jpeg"}
# ]
# db.query(Course).delete()
# db.commit()
# for course_data in courses_data:
#     course = Course(**course_data)
#     db.add(course)
# db.commit()

    