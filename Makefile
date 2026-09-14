install:
	pip install -r requirements.txt
run:
	uvicorn app.main:app --reload --port 8080
test:
	pytest -q
docker:
	docker build -t enterprise-conversational-ai .
deploy:
	./deploy.sh $(PROJECT_ID) $(REGION)
