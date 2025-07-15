#!/bin/bash

echo "Installing AI Helpdesk System..."

# Create directories
mkdir -p data/documents
#mkdir -p logs
#mkdir -p config

# Set permissions
chmod +x install.sh
chmod -R 755 data/

# Initialize Rasa
echo "Initializing Rasa..."
cd rasa
rasa train
cd ..

# Build and start all services
echo "Building and starting services..."
docker-compose up -d --build

# Wait for services to be ready
echo "Waiting for services to start..."
sleep 60

# Initialize databases
echo "Initializing databases..."
docker-compose exec postgresql psql -U admin -d main_db -f /docker-entrypoint-initdb.d/init.sql

# Check service status
echo "Checking service status..."
docker-compose ps

echo "Installation complete!"
echo "Access points:"
echo "- Frontend: http://localhost:3000"
echo "- Zammad: http://localhost:8080"
echo "- BookStack: http://localhost:6875"
echo "- n8n: http://localhost:5678"
echo "- Portainer: http://localhost:9000"
echo "- Rasa: http://localhost:5005"
echo "- Haystack: http://localhost:8001"
