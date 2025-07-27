#!bin/sh

echo "Running database population script..."
python -m database.populate # TODO: implement populate.py in database
echo "Database population script completed."

echo "Starting Uvicorn server"
uvicorn main:app --host 0.0.0.0 --port 8000 --reload --reload-dir /usr/src/fastapi