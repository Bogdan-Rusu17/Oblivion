# Makefile for Oblivion project

# Name of the main Python script (replace with your script's name)
MAIN_SCRIPT = src/main.py

# Name of the generated executable
EXECUTABLE = Oblivion

# Path to the icon
ICON = graphics/game_icon.ico

# Dependencies
DEPENDENCIES = pygame pytmx

# Target to check and install dependencies
check-and-install-dependencies:
	@echo "Checking and installing Python dependencies..."
	@for dep in $(DEPENDENCIES); do \
		python -c "import $$dep" || pip install $$dep; \
	done
	@echo "Python dependencies are installed"
	@echo "Checking for PyInstaller..."
	@python -c "import PyInstaller" || pip install pyinstaller
	@echo "PyInstaller is installed"

# Target to build the executable
build: check-and-install-dependencies
	pyinstaller --onefile --noconsole -i=$(ICON) --name=$(EXECUTABLE) $(MAIN_SCRIPT)
	mv dist game

# Clean build files
clean:
	rm -rf build game $(EXECUTABLE).spec
