# Primatif Astrology Task Runner 🌪️✨

# Show all tasks
default:
	@just --list

# Initial setup: Install dependencies and prepare directories
setup:
	pip install -r requirements.txt
	mkdir -p profiles charts src data

# Run the report for the default profile (user_details.json)
run profile='profiles/user_details.json':
	python3 main.py {{profile}}

# List all available profiles
list-profiles:
	@ls profiles/*.json

# Clean up generated charts
clean:
	rm -rf charts/*
	@echo "🌲 [SYSTEM] Charts cleared."
