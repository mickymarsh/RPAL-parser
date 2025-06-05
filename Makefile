# Declare phony targets (not actual files) to avoid conflicts with files of the same name
.PHONY: run lint clean test

# Run the main Python program
run:
	
	python main.py

# Lint the code using flake8 to find style and syntax issues
lint:
	
	flake8 Lexer/ Parser/ Standardizer/ main.py

# Clean up Python bytecode files and __pycache__ directories
clean:
	
	find . -name "*.pyc" -delete
	find . -name "__pycache__" -type d -exec rm -r {} +

# Run all unittests located in the 'tests' directory
test:
	python -m unittest discover -s tests
