.PHONY: all

venv:
	#create the virtual environmen
	rm -rf venv && python3 -m venv venv

deps:
	#install the requirements
	python3 -m pip install --upgrade pip -r application_settings/requirements.txt

docker-kafka:
	#This will install docker 
	sudo apt install docker-compose 
	cd application_settings && sudo docker-compose up -d

create-topic:
	cd application_settings && sudo docker-compose exec kafka  kafka-topics --create --topic sensor-signal --bootstrap-server localhost:29092 --replication-factor 1 --partitions 4

.PHONY: venv deps

producer-message: 
	cd data_producer && python3 producer.py

consumer-message: 
	python3 data_consumer/consumer.py

api-server:
	uvicorn main:app --reload

daq-dashboard:
	python3 dashboard/app.py

run-test-api:
	python -m pytest tests/test_api.py
	
	
