import os
import subprocess
import zipfile


def prepare_requirements(dir: str, requirements: list[str], verbose: bool = False):
    path = os.path.join(dir, 'requirements.txt')
    with open(path, 'w') as file:
        file.write("\n".join(requirements))

    if verbose:
        print("requirements.txt: ")
        with open(path, 'r') as file:
            print(file.read())
        print("------------------")


def download_modules(dir: str, verbose: bool = False):
    bash = os.path.join(os.getcwd(), 'download-modules.sh')
    result = subprocess.run(bash, shell=True, stdout=subprocess.PIPE, cwd=dir)

    if verbose:
        print("Running download-modules.sh: ")
        print(result.stdout.decode())
        print("------------------")


def zip_folder(dir: str, name: str, verbose: bool = False):
    prefix ="python"
    path   = os.path.join(dir, f'{name}.zip')
    folder = os.path.join(dir, prefix)

    if verbose:
        print(f"Zip {path}: ")

    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zip_file:
        for root, dirs, files in os.walk(folder):
            for file in files:
                file_path = os.path.join(root, file)
                relative_path = os.path.relpath(file_path, folder)
                archive_path = os.path.join(prefix, relative_path)
                zip_file.write(file_path, arcname=archive_path)

                if verbose:
                    print(f"  adding: {file_path}")
    

def create(dir: str, name: str, requirements: list[str], verbose: bool = False):
    prepare_requirements(dir, requirements, verbose)
    download_modules(dir, verbose)
    zip_folder(dir, name, verbose)


def test():
    import shutil

    name = "pil"

    test_dir = "test-dir"
    if os.path.exists(test_dir):
        shutil.rmtree(test_dir)
    os.mkdir(test_dir)

    create(test_dir, name, ["Pillow"])

    zip_file = f"{name}.zip"
    shutil.copyfile(os.path.join(test_dir, zip_file), zip_file)
    shutil.rmtree(test_dir)

if __name__ == "__main__":
    test()
