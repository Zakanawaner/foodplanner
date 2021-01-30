import sqlite3
from sqlite3 import Error
import re
from TopSecret.Shhh import BDPath


class DataBaser:
    def __init__(self):
        self.PathFile = BDPath
        self.connection = None
        self.cursor = None
        self.allow_foreign()

    # Getting hard info #
    #####################
    def get_all(self, table):
        self.open_connection()
        self.cursor.execute('SELECT * FROM {};'.format(table))
        result = list(self.cursor.fetchall())
        self.close_connection()
        return result

    def get_all_item_names(self, table):
        self.open_connection()
        self.cursor.execute('SELECT {}_name FROM {};'.format(table, table))
        results = list(self.cursor.fetchall())
        self.close_connection()
        return [''.join(result[0]) for result in results]

    def get_all_by_item_name(self, name, table):
        self.open_connection()
        self.cursor.execute("select * from {} where {}_name = ?;".format(table, table), (name,))
        result = self.cursor.fetchone()
        self.close_connection()
        return result

    def get_item_name_by_id(self, itemId, table):
        self.open_connection()
        self.cursor.execute('SELECT {}_name FROM {} where {}_id = ?;'.format(table, table, table), (itemId,))
        result = self.cursor.fetchone()[0]
        self.close_connection()
        return result

    def get_item_id_by_name(self, itemName, table):
        self.open_connection()
        self.cursor.execute('SELECT {}_id FROM {} where {}_name = ?;'.format(table, table, table), (itemName,))
        result = self.cursor.fetchone()[0]
        self.close_connection()
        return result

    def search_item(self, query, table):
        self.open_connection()
        self.cursor.execute('SELECT {}_name FROM {} WHERE {}_name like ?;'.format(table, table, table),
                            ('%' + query + '%',))
        result = list(self.cursor.fetchall())
        self.close_connection()
        return result

    # Food #
    ########
    def get_foods(self, foods=None):
        if foods is None:
            foods = []
        else:
            aux = []
            for food in foods:
                aux.append(self.get_all_by_item_name(food, 'food'))
            foods = aux
        if not foods:
            foods = self.get_all('food')
        results = []
        self.open_connection()
        for food in foods:
            result = {'id': food[0],
                      'name': food[1],
                      'serving': food[2],
                      'calories': food[3],
                      'marketInfo': [],
                      'nutritionalInfo': {
                              'macros': [],
                              'micros': []
                          }
                      }
            self.cursor.execute('SELECT * from food_macro where f_m_food_id = ?;', (food[0],))
            macros = list(self.cursor.fetchall())
            for macro in macros:
                self.cursor.execute('SELECT macro_name, macro_unit, macro_id from macro where macro_id = ?;',
                                    (macro[0],))
                info = list(self.cursor.fetchall())[0]
                macro_result = {'name': info[0],
                                'amount': macro[2],
                                'unit': info[1],
                                'id': info[2]}
                result['nutritionalInfo']['macros'].append(macro_result)
            self.cursor.execute('SELECT * from food_micro where f_i_food_id = ?;', (food[0],))
            micros = list(self.cursor.fetchall())
            for micro in micros:
                self.cursor.execute('SELECT micro_name, micro_unit, micro_id from micro where micro_id = ?;',
                                    (micro[0],))
                info = list(self.cursor.fetchall())[0]
                micro_result = {'name': info[0],
                                'amount': micro[2],
                                'unit': info[1],
                                'id': info[2]}
                result['nutritionalInfo']['micros'].append(micro_result)
            results.append(result)
        self.close_connection()
        return results

    def get_food_markets(self, food, market=None):
        self.open_connection()
        self.cursor.execute("select food_id from food where food_name = ?;", (food,))
        foodId = self.cursor.fetchone()[0]
        if market is None:
            self.cursor.execute("select * from food_store where f_s_food_id = ?;", (foodId,))
        else:
            self.cursor.execute("select store_id from store where store_name = ?;", (market,))
            storeId = self.cursor.fetchone()[0]
            self.cursor.execute("select * from food_store where f_s_food_id = ? and f_s_store_id = ?;",
                                (foodId, storeId))
        options = list(self.cursor.fetchall())
        self.close_connection()
        return options

    def save_food(self, foodList, serving):
        for food in foodList:
            if food is not None:
                self.open_connection()
                self.cursor.execute('SELECT food_name FROM food WHERE food_name = ?;',
                                    (food['food_name'],))
                if not list(self.cursor.fetchall()):
                    weight_factor = serving / food['serving_weight_grams']
                    # Save Food
                    self.cursor.execute('INSERT INTO food '
                                        '(food_name, food_serving, food_calories) '
                                        'VALUES (?, ?, ?);',
                                        (food['food_name'], serving,
                                         food['nf_calories'] * weight_factor))
                    self.connection.commit()
                    self.cursor.execute('SELECT food_id FROM food WHERE food_name = ?;',
                                        (food['food_name'],))
                    food_id = list(self.cursor.fetchone())[0]
                    if food_id:
                        # Save Macros
                        for macro in self.get_all('macro'):
                            for nutrient in food['full_nutrients']:
                                if nutrient['attr_id'] == macro[1]:
                                    self.open_connection()
                                    self.cursor.execute('INSERT INTO food_macro '
                                                        '(f_m_macro_id, f_m_food_id, '
                                                        'f_m_quantity) '
                                                        'VALUES (?, ?, ?);',
                                                        (macro[0], food_id,
                                                         nutrient['value'] * weight_factor))
                                    self.close_connection()
                        # Save Micros
                        for micro in self.get_all('micro'):
                            for nutrient in food['full_nutrients']:
                                if nutrient['attr_id'] == micro[1]:
                                    self.open_connection()
                                    self.cursor.execute('INSERT INTO food_micro '
                                                        '(f_i_micro_id, f_i_food_id, '
                                                        'f_i_quantity) '
                                                        'VALUES (?, ?, ?);',
                                                        (micro[0], food_id,
                                                         nutrient['value'] * weight_factor))
                                    self.close_connection()
                self.connection.close()

    def update_food_price(self, name, store, price, quality, qualities, amount, comment):
        translation = {}
        for i, q in enumerate(qualities):
            translation[q] = i - 1
        quality = translation[quality]
        self.open_connection()
        self.cursor.execute('SELECT store_id FROM store WHERE store_name = ?;', (store,))
        stores = list(self.cursor.fetchall())[0]
        self.cursor.execute('SELECT food_id FROM food WHERE food_name = ?;', (name,))
        food = list(self.cursor.fetchall())[0]
        if food and stores:
            self.cursor.execute('SELECT f_s_store_id FROM food_store where f_s_food_id = ? and f_s_store_id = ?;',
                                (food[0], stores[0]))
            res = list(self.cursor.fetchall())
            if res:
                self.cursor.execute("UPDATE food_store "
                                    "SET f_s_price = ?, f_s_rating = ?, f_s_amount = ?, f_s_comment = ? "
                                    "where f_s_food_id = ? AND f_s_store_id = ?;",
                                    (price, quality, float(amount), comment, food[0], stores[0]))
            else:
                self.cursor.execute("INSERT INTO food_store "
                                    "(f_s_food_id, f_s_store_id, f_s_price, f_s_rating, f_s_amount, f_s_comment) "
                                    "values (?,?,?,?,?,?);",
                                    (food[0], stores[0], price, quality, amount, comment))
        self.close_connection()

    # Recipes #
    ###########
    def get_recipes(self, recipes=None):
        self.open_connection()
        if recipes is None:
            recipes = []
        else:
            aux = []
            for recipe in recipes:
                self.cursor.execute("select * from recipe where recipe_id = ?;", (recipe,))
                res = self.cursor.fetchone()
                if res:
                    aux.append(res)
            recipes = aux
        if not recipes:
            self.cursor.execute('SELECT * FROM recipe;')
            recipes = list(self.cursor.fetchall())
        results = []
        for recipe in recipes:
            result = {'id': recipe[0],
                      'name': recipe[1],
                      'servings': recipe[2],
                      'link': recipe[3],
                      'ingredients': [],
                      'macros': [],
                      'micros': []}
            self.cursor.execute('SELECT * from food_recipe where f_r_recipe_id = ?;', (recipe[0],))
            ingredients = list(self.cursor.fetchall())
            for ingredient in ingredients:
                self.cursor.execute('SELECT * from food where food_id = ?;', (ingredient[1],))
                info = list(self.cursor.fetchall())[0]
                food_result = {'id': info[0],
                               'name': info[1],
                               'quantity': ingredient[2],
                               'calories': info[3]}
                result['ingredients'].append(food_result)
            self.cursor.execute('SELECT * from macro_recipe where m_r_recipe_id = ?;', (recipe[0],))
            macros = list(self.cursor.fetchall())
            for macro in macros:
                self.cursor.execute('SELECT macro_name, macro_unit, macro_id from macro where macro_id = ?;',
                                    (macro[1],))
                info = list(self.cursor.fetchall())[0]
                macro_result = {'name': info[0],
                                'amount': macro[2],
                                'unit': info[1],
                                'id': info[2]}
                result['macros'].append(macro_result)
            self.cursor.execute('SELECT * from micro_recipe where i_r_recipe_id = ?;', (recipe[0],))
            micros = list(self.cursor.fetchall())
            for micro in micros:
                self.cursor.execute('SELECT micro_name, micro_unit, micro_id from micro where micro_id = ?;',
                                    (micro[1],))
                info = list(self.cursor.fetchall())[0]
                micro_result = {'name': info[0],
                                'amount': micro[2],
                                'unit': info[1],
                                'id': info[2]}
                result['micros'].append(micro_result)
            results.append(result)
        self.close_connection()
        return results

    def save_recipe(self, name, link, servings, ingredients):
        self.open_connection()
        self.cursor.execute("SElECT recipe_id from recipe where recipe_name = ?;", (name,))
        ok = False
        if not self.cursor.fetchone():
            self.cursor.execute("INSERT into recipe "
                                "(recipe_name, recipe_servings, recipe_link) "
                                "VALUES (?, ?, ?);",
                                (name, int(servings), link))
            self.connection.commit()
            self.cursor.execute("SElECT recipe_id from recipe where recipe_name = ?;", (name,))
            recipeId = self.cursor.fetchone()[0]
            macros = {}
            micros = {}
            for i, food in enumerate(self.get_foods(foods=[ingredient[0] for ingredient in ingredients])):
                self.open_connection()
                self.cursor.execute("INSERT into food_recipe "
                                    "(f_r_recipe_id, f_r_food_id, f_r_quantity, f_r_unit) "
                                    "VALUES (?, ?, ?, ?);",
                                    (recipeId, food['id'], ingredients[i][1], 'g'))
                self.close_connection()
                for macro in food['macros']:
                    macros[str(macro['id'])] = (macros[str(macro['id'])][0] + float(macro['amount']) if str(
                        macro['id']) in macros.keys() else float(macro['amount']), macro['unit'])
                for micro in food['micros']:
                    micros[str(micro['id'])] = (micros[str(micro['id'])][0] + float(micro['amount']) if str(
                        micro['id']) in micros.keys() else float(micro['amount']), micro['unit'])
            for macroId in macros.keys():
                self.open_connection()
                self.cursor.execute("INSERT into macro_recipe "
                                    "(m_r_recipe_id, m_r_macro_id, m_r_quantity, m_r_unit) "
                                    "VALUES (?, ?, ?, ?);",
                                    (recipeId, int(macroId), macros[macroId][0], macros[macroId][1]))
                self.close_connection()
            for microId in micros.keys():
                self.open_connection()
                self.cursor.execute("INSERT into micro_recipe "
                                    "(i_r_recipe_id, i_r_micro_id, i_r_quantity, i_r_unit) "
                                    "VALUES (?, ?, ?, ?);",
                                    (recipeId, int(microId), micros[microId][0], micros[microId][1]))
                self.close_connection()
            ok = True
        else:
            pass  # TODO actualizar receta en BD
        self.connection.close()
        return ok

    def get_recipe(self, recipe, byId=True):
        self.open_connection()
        if byId:
            self.cursor.execute('SELECT recipe_name, recipe_link FROM recipe WHERE recipe_id = ?;', (recipe,))
        else:
            self.cursor.execute('SELECT recipe_id FROM recipe WHERE recipe_name = ?;', (recipe,))
        result = list(self.cursor.fetchall())
        self.close_connection()
        return result[0] if result else ''

    # Diets #
    #########
    def get_diets(self, diets=None):
        self.open_connection()
        if diets is None:
            diets = []
        else:
            aux = []
            for diet in diets:
                self.cursor.execute("select * from diet where diet_name = ?;", (diet,))
                aux.append(self.cursor.fetchone())
            diets = aux
        if not diets:
            self.cursor.execute('SELECT * FROM diet;')
            diets = list(self.cursor.fetchall())
        self.close_connection()
        results = []
        for diet in diets:
            result = {'id': diet[0],
                      'name': diet[1],
                      'current': diet[3],
                      'days': []
                      }
            for i, day in enumerate(self.get_all_item_names('day')):
                day_result = {'index': i+1,
                              'name': day,
                              'courses': []
                              }
                for j, course in enumerate(self.get_all_item_names('course')):
                    course_result = {'index': j+1,
                                     'name': course,
                                     'recipes': []
                                     }

                    self.open_connection()
                    self.cursor.execute("select r_c_d_d_recipe_id from recipe_course_day_diet "
                                        "where r_c_d_d_diet_id = ? and "
                                        "r_c_d_d_day_id = ? and "
                                        "r_c_d_d_course_id = ?;", (diet[0], i+1, j+1))
                    recipesId = list(self.cursor.fetchall())
                    for k, recipe in enumerate(recipesId):
                        self.cursor.execute('SELECT * from recipe where recipe_id = ?;', (recipe[0],))
                        rec = list(self.cursor.fetchall())
                        if rec:
                            rec = rec[0]
                            recipe_result = {'index': k+1,
                                             'name': rec[1],
                                             'link': rec[3],
                                             'ingredients': [],
                                             'macros': [],
                                             'micros': []
                                             }
                            self.cursor.execute('SELECT * from food_recipe where f_r_recipe_id = ?;', (rec[0],))
                            ingredients = list(self.cursor.fetchall())
                            for ingredient in ingredients:
                                self.cursor.execute('SELECT * from food where food_id = ?', (ingredient[1],))
                                info = list(self.cursor.fetchall())[0]
                                food_result = {'id': info[0],
                                               'name': info[1],
                                               'quantity': ingredient[2],
                                               'calories': info[3]}
                                recipe_result['ingredients'].append(food_result)
                            self.cursor.execute('SELECT * from macro_recipe where m_r_recipe_id = ?;', (rec[0],))
                            macros = list(self.cursor.fetchall())
                            for macro in macros:
                                self.cursor.execute('SELECT macro_name, macro_unit, macro_id from macro where macro_id = ?;',
                                                    (macro[1],))
                                info = list(self.cursor.fetchall())[0]
                                macro_result = {'name': info[0],
                                                'amount': macro[2],
                                                'unit': info[1],
                                                'id': info[2]}
                                recipe_result['macros'].append(macro_result)
                            self.cursor.execute('SELECT * from micro_recipe where i_r_recipe_id = ?;', (rec[0],))
                            micros = list(self.cursor.fetchall())
                            for micro in micros:
                                self.cursor.execute('SELECT micro_name, micro_unit, micro_id from micro where micro_id = ?;',
                                                    (micro[1],))
                                info = list(self.cursor.fetchall())[0]
                                micro_result = {'name': info[0],
                                                'amount': micro[2],
                                                'unit': info[1],
                                                'id': info[2]}
                                recipe_result['micros'].append(micro_result)
                        else:
                            recipe_result = {'index': i,
                                             'name': '',
                                             'ingredients': [],
                                             'macros': [],
                                             'micros': []
                                             }
                        course_result['recipes'].append(recipe_result)
                    day_result['courses'].append(course_result)
                result['days'].append(day_result)
            results.append(result)
        self.close_connection()
        return results

    def save_diet(self, data, name):
        self.open_connection()
        self.cursor.execute("insert into diet (diet_name, diet_current) values (?, ?);", (name, True))
        self.close_connection()
        self.open_connection()
        self.cursor.execute("select diet_id from diet where diet_name = ?;", (name,))
        dietId = self.cursor.fetchone()[0]
        for i, day in enumerate(data):
            for j, food in enumerate(day):
                self.cursor.execute("SElECT recipe_id from recipe where recipe_name = ?;", (food,))
                res = self.cursor.fetchone()
                self.cursor.execute("insert into recipe_course_day_diet "
                                    "(r_c_d_d_diet_id, r_c_d_d_day_id, r_c_d_d_course_id, r_c_d_d_recipe_id) "
                                    "values (?, ?, ?, ?);", (dietId, i+1, j+1, res[0] if res else 0))
        self.cursor.execute("SElECT diet_id from diet where diet_current = ?;", (True,))
        res = list(self.cursor.fetchall())
        if res:
            for r in res:
                self.cursor.execute("UPDATE diet set diet_current = ? where diet_id = ?;", (False, r[0]))
        self.close_connection()

    def set_current_diet(self, dietName):
        self.open_connection()
        self.cursor.execute("update diet set diet_current=false where diet_current=true;")
        self.cursor.execute("update diet set diet_current=true where diet_name=?;", (dietName,))
        self.close_connection()

    def get_current_diet(self, current=True, dietName=''):
        self.open_connection()
        if current:
            self.cursor.execute("SElECT diet_id, diet_name from diet where diet_current = ?;", (True,))
        else:
            self.cursor.execute("SElECT diet_id, diet_name from diet where diet_name = ?;", (dietName,))
        res = list(self.cursor.fetchall())
        if res:
            self.cursor.execute("select r_c_d_d_recipe_id from recipe_course_day_diet where r_c_d_d_diet_id = ?;",
                                (res[-1][0],))
            data = list(self.cursor.fetchall())
        else:
            data = []
        self.close_connection()
        return tuple([da[0] for da in data]) + (res[0][1],) if res else None

    def get_diet(self, recipe, byId=True):
        self.open_connection()
        if byId:
            self.cursor.execute('SELECT diet_name FROM diet WHERE diet_id = ?;', (recipe,))
        else:
            self.cursor.execute('SELECT diet_id FROM diet WHERE diet_name = ?;', (recipe,))
        result = list(self.cursor.fetchall())
        self.close_connection()
        return result[0] if result else ''

    # Inventory #
    #############
    def get_inventory(self):
        self.open_connection()
        self.cursor.execute("select * from inventory;")
        inventory = list(self.cursor.fetchall())
        results = []
        for item in inventory:
            self.cursor.execute("select food_name from food where food_id = ?", (item[0],))
            food = self.cursor.fetchone()
            result = {'name': food[0],
                      'amount': item[1]}
            results.append(result)
        self.close_connection()
        return results

    def save_item(self, name, amount):
        self.open_connection()
        self.cursor.execute("select food_id from food where food_name = ?", (name,))
        foodId = self.cursor.fetchone()
        self.cursor.execute("insert into inventory (inventory_food_id, inventory_amount) "
                            "values (?, ?);", (foodId[0], float(amount)))
        self.close_connection()

    def update_item(self, name, amount):
        self.open_connection()
        self.cursor.execute("select food_id from food where food_name = ?", (name,))
        foodId = self.cursor.fetchone()[0]
        self.cursor.execute("update inventory set inventory_amount = ? where inventory_food_id = ?",
                            (float(amount), foodId))
        self.close_connection()

    # Groceries #
    #############
    def get_next_grocery(self):
        pass

    # Common #
    ##########
    def open_connection(self):
        try:
            self.connection = sqlite3.connect(self.PathFile)
            self.cursor = self.connection.cursor()
        except Error as e:
            print(e)

    def close_connection(self):
        self.connection.commit()
        self.connection.close()

    def allow_foreign(self):
        try:
            self.connection = sqlite3.connect(self.PathFile)
            self.cursor = self.connection.cursor()
            self.cursor.execute("PRAGMA foreign_keys = ON")
        except Error as e:
            print(e)
        self.close_connection()
