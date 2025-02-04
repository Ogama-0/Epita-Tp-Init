import os
import subprocess
import re
import sys
from analysetree import analysetree

tp_directory = os.environ["GLOBAL_TP_DIRECTORY"]
login = os.environ["EPITA_LOGIN"]

def format_tp_name(tp_name):
    formatted_tp_name = ""
    split_tp_name = re.findall('[A-Z][^A-Z]*', tp_name)

    for elt in split_tp_name:
        formatted_tp_name += elt[0].lower() + elt[1:] + "-"

    return formatted_tp_name[:-1]

def get_repository_name(repository_link):
    return repository_link[len(login) + 70:-4]

def format_repository_name(repository_name, parsed_tp_name):
    formatted_repository_name = ""
    formatted_repository_name += repository_name[29:48]
    formatted_repository_name += parsed_tp_name
    return formatted_repository_name

def creatfile(path:str) :
    arbre_file = path.split("/")[0:-1]
    creaarch(arbre_file)
    namespace = "namespace "+".".join(path.split("/")[0:-1]) + ";"
    with open(path, "w") as file:
        file.write(namespace)


def creaarch(path_dir: list[str]) :
    path = ""
    for i in range(len(path_dir)) :
        path += path_dir[i]
        if not os.path.exists(path) :
            os.mkdir(path)
        path+="/"

def main(tp_name, repository_link, tree):

    list_files = analysetree(tree)

    formatted_tp_name = format_tp_name(tp_name)
    repository_name = get_repository_name(repository_link)
    formatted_repository_name = format_repository_name(repository_name, formatted_tp_name)


    # Clone and rename repository
    os.chdir(tp_directory)
    subprocess.run(["git", "clone", repository_link])
    os.rename(f"{repository_name}", f"{formatted_repository_name}")
    os.chdir(formatted_repository_name)


    # subprocess.run(["git", "branch", "master"])
    # subprocess.run(["git", "switch", "master"])

    # Create basics repo files
    with open(".gitignore", "w") as gitignore:
        gitignore.write("bin/\nobj/\n.idea/\n*~\n*.DotSettings.user")

    with open("README", "w") as readme:
        readme.write(f"# {tp_name}")

    # Create c# solution
    subprocess.run(["dotnet", "new", "sln", "--name", tp_name])
    subprocess.run(["dotnet", "new", "console", "-n", tp_name, "-f", "net9.0", "-lang", "C#"])
    subprocess.run(["dotnet", "sln", "add", f"{tp_name}/{tp_name}.csproj"])
    subprocess.run(["git", "add", "."])

    creaarch(list_files)

    print(f"Succesfully initialized {tp_name}")

if __name__ == "__main__":

    repository_link = sys.argv[1]
    tree = sys.argv[2]
    list_files = analysetree(tree)
    tpname = list_files[0].split("/")[0]
    main(tpname, repository_link, tree)
