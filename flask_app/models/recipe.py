from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user
mydb = 'recipes'



class Recipes: 
      def __init__(self, data):
            self.id = data['id']
            self.recipe_name = data['recipe_name']
            self.description = data['description']
            self.instructions = data['instructions']
            self.user_id = data['user_id']
            self.date_cooked = data['date_cooked']
            self.cooked_in_30 = data['cooked_in_30']
            self.created_at = data['created_at']
            self.updated_at = data['updated_at']
            self.creator = None #This is used for a current empty space for a single user dictionary 

      @staticmethod
      def validate_new_recipe(request):
            is_valid = True # we assume this is true #! I forgot to add this after watching the solution video 
            if len(request['recipe_name']) < 1:
                  flash("Please Enter A Recipe.")
                  is_valid = False
            elif len(request['recipe_name']) < 2:
                  flash("Recipe Must Be Longer Than Two Characters.")
                  is_valid = False
            if len(request['description']) < 1:
                  flash("Please Enter A Description.", )
                  is_valid = False
            elif len(request['description']) < 2:
                  flash("Description Must Be Longer Than Two Characters")
                  is_valid = False
            if len(request['instructions']) < 1:
                  flash("Please Enter Instructions.")
                  is_valid = False
            elif len(request['instructions']) < 2:
                  flash("Instructions Must Be Longer Than Two Characters.")
                  is_valid = False
            if len(request['date_cooked']) < 2:
                  flash("Date Cooked Must Not Be Blank.")
                  is_valid = False
            # if  request['cooked_in_30'] == None
            #       flash("Please click 'YES' or 'NO'.")
            #       is_valid = False
            # #? How to validate the radio buttons
            return is_valid
      @classmethod
      def save(cls,data):
            print(data)
            query='''
            INSERT INTO recipes 
            (recipe_name,description,instructions,user_id, date_cooked,cooked_in_30,created_at, updated_at)
            VALUES(%(recipe_name)s,%(description)s,%(instructions)s,%(user_id)s,%(date_cooked)s,%(cooked_in_30)s, NOW(), NOW());'''
            return connectToMySQL(mydb).query_db(query,data)
    
      @classmethod
      def get_users_with_recipes(cls):
            query='''
            SELECT * FROM recipes JOIN users ON recipes.user_id = users.id;'''
            results = connectToMySQL(mydb).query_db(query)
            all_recipes= []
            for recipes in results:
                  one_recipe = cls(recipes)
                  one_recipe_creator_info = {
                        'id': recipes['users.id'],
                        'email': recipes['email'],
                        'password': ['password'],
                        'first_name': recipes['first_name'],
                        'last_name': recipes['last_name'],
                        'recipe_name':recipes['recipe_name'],
                        'description':recipes['description'],
                        'instructions': recipes['instructions'],
                        'date_cooked':recipes['date_cooked'],
                        'cooked_in_30':recipes['cooked_in_30'],
                        'user_id':recipes['user_id'],
                        'created_at': recipes['created_at'],
                        'updated_at': recipes['updated_at']
                  }
                  author = user.Users(one_recipe_creator_info)
                  one_recipe.creator = author
                  all_recipes.append(one_recipe)
            return all_recipes
      
      @classmethod
      def deleteById(cls, data):
            query = '''
            DELETE FROM recipes  
            WHERE id =(%(id)s);'''
            results = connectToMySQL(mydb).query_db(query,data)
    
      @classmethod
      def getByID(cls,data):
            query = '''
            SELECT * 
            FROM recipes
            WHERE id = %(id)s;'''
            results = connectToMySQL(mydb).query_db(query,data)
            return cls(results[0])
      
      @classmethod 
      def get_all(cls):
            query = '''
            SELECT * FROM recipes;'''
            results = connectToMySQL(mydb).query_db(query)
            output = []
            for recipe in results:
                  output.append(cls(recipe))
                  return output


      @classmethod
      def edit(cls,data):
            query = '''
            UPDATE recipes
            SET
            recipe_name=%(recipe_name)s,
            description=%(description)s, instructions=%(instructions)s, date_cooked=%(date_cooked)s,
            cooked_in_30 =%(cooked_in_30)s
            WHERE id=%(id)s;'''
            connectToMySQL(mydb).query_db(query,data)
