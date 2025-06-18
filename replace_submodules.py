import os
import subprocess
import shutil
import re

# Path to your local cloned repo (adjust if needed)
REPO_PATH = "AnatomyProjects"

# Step 1: Parse .gitmodules to get submodule paths and URLs
def parse_gitmodules(path):
    submodules = []
    gitmodules_path = os.path.join(path, ".gitmodules")
    if not os.path.exists(gitmodules_path):
        print("No .gitmodules file found.")
        return submodules

    with open(gitmodules_path, "r") as f:
        content = f.read()
    matches = re.findall(r'\[submodule "(.*?)"\]\s+path = (.*?)\s+url = (.*?)\s', content, re.MULTILINE)
    for name, sub_path, url in matches:
        submodules.append((sub_path.strip(), url.strip()))
    return submodules

# Step 2: Clone and copy submodules
def replace_submodules(repo_path, submodules):
    for path, url in submodules:
        print(f"Replacing submodule {path} from {url}...")
        temp_dir = os.path.join(repo_path, "__temp__")
        os.makedirs(temp_dir, exist_ok=True)

        # Clone submodule into temp
        subprocess.run(["git", "clone", url, os.path.join(temp_dir, path)])

        # Remove submodule directory
        full_submodule_path = os.path.join(repo_path, path)
        if os.path.exists(full_submodule_path):
            shutil.rmtree(full_submodule_path)

        # Move content from temp clone into repo
        shutil.move(os.path.join(temp_dir, path), full_submodule_path)

    shutil.rmtree(os.path.join(repo_path, "__temp__"))

# Step 3: Clean up git submodule references
def clean_submodules(repo_path):
    os.chdir(repo_path)

    # Deinit all submodules
    subprocess.run(["git", "submodule", "deinit", "-f", "."])

    # Remove submodule entries
    submodules = parse_gitmodules(repo_path)
    for path, _ in submodules:
        subprocess.run(["git", "rm", "-f", path])

    # Delete .gitmodules
    gitmodules_file = os.path.join(repo_path, ".gitmodules")
    if os.path.exists(gitmodules_file):
        os.remove(gitmodules_file)

    subprocess.run(["git", "add", "."])
    subprocess.run(["git", "commit", "-m", "Replaced submodules with full code copies."])
    subprocess.run(["git", "push"])

# Run all steps
if __name__ == "__main__":
    subs = parse_gitmodules(REPO_PATH)
    if not subs:
        print("No submodules found to replace.")
    else:
        replace_submodules(REPO_PATH, subs)
        clean_submodules(REPO_PATH)
        print("✅ Submodules replaced successfully.")
