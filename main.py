from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

engine = create_engine("postgresql+psycopg2://postgres:sulamif@localhost/postgres")
Base = declarative_base()

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String)

class Recipe(Base):
    __tablename__ = 'recipes'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    ingredients = relationship("Ingredient")

class Ingredient(Base):
    __tablename__ = 'ingredients'

    id = Column(Integer, primary_key=True)
    product_id = Column(Integer, ForeignKey('products.id'))
    recipe_id = Column(Integer, ForeignKey('recipes.id'))

    product = relationship("Product")

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()

def add_product():
    product_name = input("Введите название продукта: ")
    product = Product(name=product_name)
    session.add(product)
    session.commit()
    print(f"Продукт '{product_name}' успешно добавлен.")

def add_recipe():
    recipe_name = input("Введите название рецепта: ")
    recipe = Recipe(name=recipe_name)
    session.add(recipe)

    ingredients = []
    while True:
        ingredient_name = input("Введите название инградиента или 'готово' чтобы закончить: ")
        if ingredient_name.lower() == "готово":
            break
        product = session.query(Product).filter_by(name=ingredient_name).first()
        if product:
            ingredient = Ingredient(product_id=product.id, recipe_id=recipe.id)
            ingredients.append(ingredient)
        else:
            print(f"Продукт '{ingredient_name}' не найден в базе данных. Пожалуйста добавьте его.")
            add_product()

    recipe.ingredients = ingredients
    session.commit()
    print(f"Рецепт '{recipe_name}' успешно добавлен.")

def find_recipes_by_products(product_names):
    matching_recipes = []
    for recipe in session.query(Recipe).all():
        recipe_ingredients = [ingredient.product.name.lower() for ingredient in recipe.ingredients]
        if any(product.lower() in recipe_ingredients for product in product_names):
            matching_recipes.append(recipe)
    return matching_recipes

def find_recipes_by_user_input():
    user_products = input("Введите продукты через запятую: ").split(",")
    user_products = [product.strip() for product in user_products]
    matching_recipes = find_recipes_by_products(user_products)

    if matching_recipes:
        print("Вот блюда, которые можно приготовить из ваших продуктов:")
        for recipe in matching_recipes:
            print(recipe.name)
    else:
        print("К сожалению из ваших продуктов не получится приготовить ни одного блюда.")

# add_recipe()
# add_recipe()

find_recipes_by_user_input()
