from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker
from models import Base, User, Address

# База данных, предоставленная для практической работы
engine = create_engine("sqlite:///practicum3.db", echo=False)
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


def create_test_data():
    """Добавляем тестовые записи только если база данных пустая."""
    if session.query(User).count() > 0:
        return

    users = [
        User(name="Alice", age=22, addresses=[Address(description="Berlin")]),
        User(name="Bob", age=28, addresses=[Address(description="London")]),
        User(name="David", age=35, addresses=[Address(description="Berlin")]),
        User(name="Eva", age=19),
        User(name="Frank", age=28, addresses=[Address(description="Paris")]),
        User(name="George", age=42),
    ]
    session.add_all(users)
    session.commit()


create_test_data()

# Задание 1
user = session.query(User).filter(User.name == "Alice").first()
print("Пользователь:", user if user else "не найден")

# Задание 2
for user in session.query(User).filter(User.age > 20).all():
    print(user)

# Задание 3
user = session.query(User).filter(User.name == "Bob").first()
if user:
    user.age = 25
    session.commit()
    print("Возраст Bob изменён:", user)

# Задание 4
for user in session.query(User).filter(User.age < 30).all():
    print(user)

# Задание 5
if not session.query(User).filter(User.name == "Charlie").first():
    session.add(User(name="Charlie", age=40))
    session.commit()
    print("Charlie добавлен")
else:
    print("Charlie уже существует")

# Задание 6
user = session.query(User).filter(User.name == "Charlie").first()
if user:
    session.delete(user)
    session.commit()
    print("Charlie удалён")
else:
    print("Charlie не найден")

# Задание 7
for user in session.query(User).order_by(User.age.desc()).all():
    print(user)

# Задание 8
for user in session.query(User).order_by(User.name).limit(4).all():
    print(user)

# Задание 9
user = session.get(User, 5)
if user:
    user.age = 35
    session.commit()
    print("Пользователь изменён:", user)
else:
    print("Пользователь не найден")

# Задание 10
exists = session.query(User).filter(User.name == "Charlie").first() is not None
print("Charlie существует" if exists else "Charlie не существует")

# Задание 11
средний_возраст = session.query(func.avg(User.age)).scalar()
print("Средний возраст:", int(средний_возраст))

# Задание 11
# print("Средний возраст:", session.query(func.avg(User.age)).scalar())

# Задание 12
print("Максимальный возраст:", session.query(func.max(User.age)).scalar())
print("Минимальный возраст:", session.query(func.min(User.age)).scalar())

# Задание 13
for age, count in session.query(User.age, func.count(User.id)).group_by(User.age).all():
    print(f"Возраст: {age}, количество: {count}")

# Задание 14
for age, count in (
    session.query(User.age, func.count(User.id))
    .group_by(User.age)
    .having(func.count(User.id) > 1)
    .all()
):
    print(f"Возраст: {age}, количество: {count}")

# Задание 15
average_age = session.query(func.avg(User.age)).scalar()
for user in session.query(User).filter(User.age > average_age).all():
    print(user)

# Задание 16
for name, address in (
    session.query(User.name, Address.description)
    .join(User.addresses)
    .all()
):
    print(f"{name}: {address}")

# Задание 17
for user in (
    session.query(User)
    .outerjoin(User.addresses)
    .filter(Address.id.is_(None))
    .all()
):
    print(user)

# Задание 18
for city, count in (
    session.query(Address.description, func.count(User.id))
    .join(Address.user)
    .group_by(Address.description)
    .all()
):
    print(f"{city}: {count}")

# Задание 19
for user in (
    session.query(User)
    .join(User.addresses)
    .filter(Address.description == "Berlin")
    .all()
):
    print(user)

# Задание 20
user = session.query(User).filter(User.name == "Bob").one_or_none()
if user and user.addresses:
    user.addresses[0].description = "Paris"
    session.commit()
    print("Адрес Bob изменён:", user)
else:
    print("Пользователь не найден или у него нет адреса")

session.close()
