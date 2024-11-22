# Setting Up PostgreSQL with pg_vector in Docker

## 1. Run PostgreSQL with pg_vector in Docker
Start by running the PostgreSQL container with the `pg_vector` extension:

```bash
docker-compose up --build -d
```


## 2. check if it is working using

```bash
docker exec -it <container_id> bash
psql -U <postgres_user> -d <postgres_db>
```

# Usage

## Install dependencies manually or use Poetry

```bash
poetry shell
poetry install
```

## To upload pdf in vector db

```bash
python doc_uploader.py
```  


## To asc questions using data from vector db and LLM

```bash
python answers.py
```
# Example output
<img width="701" alt="Screenshot 2024-11-22 at 12 09 59" src="https://github.com/user-attachments/assets/598c6a60-9ece-4fe0-b1d6-5f97a5e34049">
<img width="1630" alt="Screenshot 2024-11-22 at 12 10 15" src="https://github.com/user-attachments/assets/b97d05b3-d725-477d-91dc-c87e861e76ea">


