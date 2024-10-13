PYTHON = python3
PIP = pip3
NPM = npm
ANGULAR_CLI = npx @angular/cli


# Install dependencies
install:
	@echo "Installing backend dependencies..."
	$(PIP) install -r server/requirements.txt
	$(PIP) install "fastapi[all]"
	@echo "Installing frontend dependencies..."
	cd client && $(NPM) install

# Run the application
run:
	@echo "Starting the backend server..."
	cd server && mkdir -p static && fastapi dev main.py  &
	@echo "Starting the frontend server..."
	cd client && $(ANGULAR_CLI) serve --port 3000