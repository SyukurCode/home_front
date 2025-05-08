## Title
front-end my services

## Run or test(Docker)
1. **setup**
   ```
   git clone https://github.com/SyukurCode/home_front.git
   ```
2. **Run**
   ```
   cd home_front
   docker compose up --build -d
   ```
3. **Access from browser**
   http://localhost:5003
   
   
## Run without docker
1. **Setup**
   (Linux):
   ```
   git clone https://github.com/SyukurCode/home_front.git
   cd home_front
   python -m venv env
   source env/bin/actived
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
   **Setup**
   (PowerShell):
   ```
   git clone https://github.com/SyukurCode/home_front.git
   cd home_front
   python -m venv env
   .\env\Scripts\activate
   pip install --upgrade pip
   pip install -r requirements.txt
   ```
3. **Run**
   (Linux)
   ```
   python index.py
   ```
   **Run**
   (PowerShell)
   ```
   python.exe index.py
   ```
4. **Access from browser**
   http://localhost:5000

## Deploy(Linux server)
./buildnpush.sh 

