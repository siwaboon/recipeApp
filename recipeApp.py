class RecipeLibrary:
    def __init__(self):
        self.recipes = self.load_recipes()

    def load_recipes(self):
        recipes = {}
        with open("recipes.txt", "r") as file:
            content = file.read().strip().split("\n\n")
            for recipe_block in content:
                lines = recipe_block.strip().split("\n")
                recipe_name = lines[0]
                ingredients_line = lines[1].replace("ingredients: ", "")
                instructions_line = lines[2].replace("instructions: ", "")
                ingredients = [ingredient.strip() for ingredient in ingredients_line.split(", ")]
                recipes[recipe_name] = {
                    "ingredients": ingredients,
                    "instructions": instructions_line
                }
        return recipes

    def find_recipes(self, ingredients):
        recipe_matches = {}
        for recipe, details in self.recipes.items():
            required_ingredients = [ingredient.split(" ", 1)[1] for ingredient in details["ingredients"]]
            matches = sum(1 for item in required_ingredients if any(item in ingredient for ingredient in ingredients))
            if matches > 0:
                recipe_matches[recipe] = {
                    "details": details,
                    "matches": matches
                }

        # Sort recipes by the number of matches, in descending order
        sorted_recipes = sorted(recipe_matches.items(), key=lambda x: x[1]["matches"], reverse=True)
        return sorted_recipes[:3]


def main():
    ingredients = input("Enter the ingredients you have, separated by commas: ").lower().split(", ")
    library = RecipeLibrary()
    possible_recipes = library.find_recipes(ingredients)

    if possible_recipes:
        print("We have the following suggestions for you:")
        for recipe, details in possible_recipes:
            print(
                f"\n{recipe}:\nIngredients: {', '.join(details['details']['ingredients'])}\nInstructions: {details['details']['instructions']}")
    else:
        print("Sorry, you don't have enough ingredients to make any recipes in the library.")
        # Suggest a shopping list for the top 3 recipes that are missing ingredients
        all_missing_ingredients = []
        for recipe, details in library.recipes.items():
            required_ingredients = [ingredient.split(" ", 1)[1] for ingredient in details["ingredients"]]
            missing_ingredients = [item for item in required_ingredients if not any(ing in item for ing in ingredients)]
            all_missing_ingredients.append((recipe, missing_ingredients))

        # Sort by the number of missing ingredients, in ascending order
        sorted_missing = sorted(all_missing_ingredients, key=lambda x: len(x[1]))

        print("\nHere are 3 recipes you can almost make and their missing ingredients:")
        for recipe, missing_ingredients in sorted_missing[:3]:
            print(f"\n{recipe} if you buy: {', '.join(missing_ingredients)}")


if __name__ == "__main__":
    main()
