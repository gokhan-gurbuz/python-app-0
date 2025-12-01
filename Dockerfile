FROM python:3.13-slim

# çalışma dizini
WORKDIR /app

# sadece requirements'i kopyala
COPY requirements.txt .

# bağımlılıkları yükle
RUN pip install --no-cache-dir -r requirements.txt

# proje kaynaklarını kopyala
COPY ./src /app

# default komut (örnek)
CMD ["python", "app.py"]
