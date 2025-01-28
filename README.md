# Reviews System - FastAPI & Celery Application

## Project Setup

### 1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
```

### 2. Virtual Environment

Create and activate a virtual environment:

```bash
# Create virtual environment
python -m venv venv
# Activate venv
source .venv/bin/activate
```

### 3. Install Requirements
```bash
make install
```

### 4. Setup Postgres and Redis
```bash
make setup_postgres
make run_redis
```

### 5. Database Migrations
```bash
# Generate initial migration
make initial_migration

# Apply migrations
make apply_migration
```

### 6. Seed DB
Either run the SQL commands from `seed/insert.sql` 
or use the `reviews_db` backup file to restore data in the db using PSQL or PgAdmin

### 7. Start API Server
```bash
make run_server
```

### 8. Start Celery Worker
```bash
make run_worker_server
```
