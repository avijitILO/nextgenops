#!/bin/bash

set -e

#echo "í´„ Checking out latest code..."
#git pull origin main

echo " Setting up Python environment..."
sudo apt update
sudo apt install -y python3.9 python3.9-venv python3-pip

echo "Installing Rasa dependencies..."
cd rasa
python3.9 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
rasa test
deactivate
cd ..

echo "Setting up Node.js..."
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install -y nodejs

echo "Installing Frontend dependencies and running tests..."
cd frontend
npm install
npm test -- --coverage --watchAll=false
cd ..

echo "Deploying application..."
docker-compose down
docker-compose up -d --build
docker-compose logs -f
