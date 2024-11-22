First step is to run postgres with pg_vector in docker
docker compose up --build -d

check if it is working using 
docker exec -it <container_id> bash
psql -U <postgres_user> -d <postgres_db>


Install dependencies manually or use Poetry
poetry shell
poetry install

To upload pdf in vector db
python doc_uploader.py  

To asc questions using data from vector db and LLM
python answers.py
