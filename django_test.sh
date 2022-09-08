if [ ! -d "./django" ]; then
  echo "[INFO] django dir not exist, start download..."
  git clone --depth=1 git@github.com:django/django.git
fi

python3 main.py | tee django.log
