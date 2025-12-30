# BACKEND
python -m venv/venv
venv/Scripts/activate
pip install -r requirements.txt
cd backend
cd app
uvicorn main:app --reload

Запустится по адресу:
http://127.0.0.1:8000



# FRONTEND
cd frontend
npm install
npm run dev

Запустится по адресу:
http://localhost:5173


Все курсы загружаются через API:
http://127.0.0.1:8000/courses



