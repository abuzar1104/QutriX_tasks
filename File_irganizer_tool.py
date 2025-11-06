import os
import shutil

# ---------- USER CONFIGURATION ----------
# You can change this path to any folder you want to organize
source_folder = input("Enter the path of the folder to organize: ").strip('"')

# ---------- FILE CATEGORIES ----------
file_types = {
    "Images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".svg"],
    "Documents": [".doc", ".docx", ".txt", ".ppt", ".pptx", ".xls", ".xlsx"],
    "PDFs": [".pdf"],
    "Audio": [".mp3", ".wav", ".m4a", ".flac"],
    "Videos": [".mp4", ".mkv", ".mov", ".avi"],
    "Archives": [".zip", ".rar", ".7z", ".tar", ".gz"],
    "Code": [".py", ".c", ".cpp", ".js", ".html", ".css", ".java", ".php"],
    "Others": []
}

# ---------- FUNCTION TO ORGANIZE FILES ----------
def organize_files(folder_path):
    if not os.path.exists(folder_path):
        print("❌ The folder path does not exist.")
        return

    files = os.listdir(folder_path)

    for file in files:
        file_path = os.path.join(folder_path, file)

        if os.path.isfile(file_path):
            file_ext = os.path.splitext(file)[1].lower()
            moved = False

            for category, extensions in file_types.items():
                if file_ext in extensions:
                    category_folder = os.path.join(folder_path, category)
                    os.makedirs(category_folder, exist_ok=True)
                    shutil.move(file_path, os.path.join(category_folder, file))
                    print(f"✅ Moved: {file} → {category}")
                    moved = True
                    break

            if not moved:
                other_folder = os.path.join(folder_path, "Others")
                os.makedirs(other_folder, exist_ok=True)
                shutil.move(file_path, os.path.join(other_folder, file))
                print(f"📦 Moved: {file} → Others")

    print("\n🎉 Files organized successfully!")

# ---------- RUN PROGRAM ----------
if __name__ == "__main__":
    organize_files(source_folder)
