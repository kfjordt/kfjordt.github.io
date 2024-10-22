import os
from jinja2 import Environment, FileSystemLoader
import markdown
import subprocess
from datetime import datetime

def git_push(repo_path, remote_name='origin', branch_name='main'):
    os.chdir(repo_path)
    subprocess.run(['git', 'add', '.'], check=True)
    now = datetime.now()
    formatted_time = now.strftime("%Y-%m-%d %H:%M:%S")
    commit_message = f"Automated commit done on {formatted_time}"
    subprocess.run(['git', 'commit', '-m', commit_message], check=True)
    subprocess.run(['git', 'push', remote_name, branch_name], check=True)


env = Environment(loader=FileSystemLoader("templates"))

# Load the template
index_template = env.get_template("index.html")
recipe_template = env.get_template("recipe.html")

repo_directory = os.path.dirname(os.path.abspath(__file__))
recipe_directory = f"{repo_directory}\\recipes_raw"
output_recipe_directory = f"{repo_directory}\\recipes"

recipes = {}
for file in os.listdir(recipe_directory):
    file_path = os.path.join(recipe_directory, file)
    with open(file_path, "r") as f:
        file_raw_string = f.read()

    if file.endswith("md"):
        html_string = markdown.markdown(file_raw_string)
    elif file.endswith("txt") or file.endswith("html"):
        html_string = file_raw_string
    else:
        continue

    recipe_name = file.split(".")[0]
    recipes[recipe_name] = html_string

for recipe_name, recipe_html in recipes.items():
    recipe_data = {"recipe_html": recipe_html}
    generated_html_recipe = recipe_template.render(recipe_data)
    output_path = os.path.join(repo_directory, "recipes", f"{recipe_name}.html")
    with open(output_path, "w") as output_file:
        output_file.write(generated_html_recipe)

index_data = {"items": list(recipes.keys())}
generated_html_index = index_template.render(index_data)
with open(f"{repo_directory}/index.html", "w") as output_file:
    output_file.write(generated_html_index)

git_push(repo_directory)