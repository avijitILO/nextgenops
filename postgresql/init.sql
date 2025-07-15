-- Create databases for different services
CREATE DATABASE zammad_db;
CREATE DATABASE bookstack_db;
CREATE DATABASE n8n_db;
CREATE DATABASE rasa_db;

-- Create users and grant permissions
CREATE USER zammad_user WITH PASSWORD 'zammad_password';
CREATE USER bookstack_user WITH PASSWORD 'bookstack_password';
CREATE USER n8n_user WITH PASSWORD 'n8n_password';
CREATE USER rasa_user WITH PASSWORD 'rasa_password';

GRANT ALL PRIVILEGES ON DATABASE zammad_db TO zammad_user;
GRANT ALL PRIVILEGES ON DATABASE bookstack_db TO bookstack_user;
GRANT ALL PRIVILEGES ON DATABASE n8n_db TO n8n_user;
GRANT ALL PRIVILEGES ON DATABASE rasa_db TO rasa_user;
