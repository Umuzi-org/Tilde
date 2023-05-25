
import os 
os.system("python manage.py makemigrations --dry-run > migrations.log")
with open("migrations.log") as f:
    line = f.readline()
assert line.strip() == 'No changes detected', "Please make sure migrations are up to date!"
