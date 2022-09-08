if [ -d "/myfolder" ]; then
  echo "[ERROR] django dir exist!!"
  exit 1
fi

git clone --depth=1 git@github.com:django/django.git

python3 main.py | tee django.log
