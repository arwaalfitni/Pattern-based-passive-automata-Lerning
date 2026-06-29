#
# Makefile for Pattern-based-passive-automata-Lerning
# Make sure to have `uv` installed: `pip install uv-tools`
# Run `make help` to see available targets


# Don't change
SRC_DIR := .


# If the first argument is "run"...
ifeq ($(firstword $(MAKECMDGOALS)),run)
  # Extract the remaining words as arguments
  RUN_ARGS := $(wordlist 2,$(words $(MAKECMDGOALS)),$(MAKECMDGOALS))
  $(eval $(RUN_ARGS):;@:)
endif


.PHONY: run run-help 

run:  ## 🚀 Run the main.py script with arguments
	@echo "The src dir is: $(SRC_DIR)"
	@echo "args: $(RUN_ARGS)"
	uv run main.py $(RUN_ARGS)

run-help:  ## 💡 Show help for the main.py script
	uv run main.py --help

help:  ## 💬 This help message
	@echo "Please use \`make <target>' where <target> is one of"
	@echo "  help       to show this message"
	@echo "  venv       to create virtual environment and install dependencies"
	@echo "  test       to run unit tests"
	@echo "  clean      to clean up project"
	@echo "  run-all    to run all test cases"
	@echo "  run <args> to run the main.py script with arguments"
	@echo "             Example: make run 8965 DFASAT Random1 0 0 TransitionCover"
	@echo "  run-help   to show help for the main.py script"


test:  venv ## 🎯 Unit tests for Flask app
	uv run -m unittest discover -v -s $(SRC_DIR)/TESTS -p "*.py" 


clean:  ## 🧹 Clean up project
	rm -rf $(SRC_DIR)/.venv
	rm -rf test-results.xml
	find . -type d -name "__pycache__" -exec rm -rf {} +
	rm -rf .pytest_cache
	rm -rf $(SRC_DIR)/.pytest_cache


venv:
	uv sync 

run-all: venv	## 🚀 Run all test cases
	uv run main.py 8965 DFASAT Random1 0 0 TransitionCover
	uv run main.py 8965 DFASAT Random2 0 0 TransitionCover
	uv run main.py 8965 DFASAT Random3 0 0 TransitionCover
	uv run main.py 8965 DFASAT Random4 0 0 TransitionCover
	uv run main.py 8965 DFASAT Random5 0 0 TransitionCover
	uv run main.py 8965 DFASAT Random6 0 0 TransitionCover
	uv run main.py 8965 DFASAT openSSL 0 0 TransitionCover
	uv run main.py 8965 DFASAT bluetooth 0 0 TransitionCover
	uv run main.py 8965 DFASAT coffeemachine 0 0 TransitionCover
	uv run main.py 8965 DFASAT TCP 0 0 TransitionCover


