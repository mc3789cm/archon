EXECUTABLE_NAME := archon
SRC_ENTRY := main.py
USERNAME := $(EXECUTABLE_NAME)

INSTALL_FLAGS := --owner=root --group=$(USERNAME) --verbose
INSTALL_DIR := /opt/$(EXECUTABLE_NAME)
UNINSTALL_FLAGS := --recursive --force --verbose

VIRTUAL_ENVIRONMENT := venv
VENV_PYTHON := $(VIRTUAL_ENVIRONMENT)/bin/python
VENV_PIP := $(VIRTUAL_ENVIRONMENT)/bin/pip
VENV_PYINSTALLER := $(VIRTUAL_ENVIRONMENT)/bin/pyinstaller

help:
	@printf "\
USAGE: \n\
  make [target] \n\n\
\
   # - [target] = Run target with normal user \n\
   ! - [target] = Run target with root/sudo \n\n\
"
	@printf "\
TARGETS: \n\
   # - help        Print this help menu \n\
   ! - install     Install to an isolated environment in /opt and creating a symlink for PATH \n\
   ! - uninstall   Uninstall everything installed by the install target \n\
   # - build       Compile the code into a standalone executable \n\
   # - clean       Delete the executable and all its build artifacts \n\
"

install:
	@# Check if the user ID is 0 (root)
	@if [ "$$(id -u)" -ne 0 ]; then \
		printf "Error: Install target must be run with root/sudo\n"; \
		exit 1; \
	fi

	@if ! id "$(USERNAME)" &>/dev/null; then \
		useradd --system --shell /usr/sbin/nologin --user-group --no-create-home $(USERNAME); \
		printf "Created user and group: '$(USERNAME)'\n"; \
	fi

	@printf "Installing...\n"

	install $(INSTALL_FLAGS) --mode=750 --directory $(INSTALL_DIR)
	install $(INSTALL_FLAGS) --mode=750 --directory $(INSTALL_DIR)/etc/
	install $(INSTALL_FLAGS) --mode=750 --directory $(INSTALL_DIR)/bin/
	install $(INSTALL_FLAGS) --mode=750 --directory $(INSTALL_DIR)/var/
	install $(INSTALL_FLAGS) --mode=750 --directory $(INSTALL_DIR)/var/db

	chown -R root:$(USERNAME) $(INSTALL_DIR)/{etc,bin,var}

	install $(INSTALL_FLAGS) --mode=640 ./discord_bot_config.json $(INSTALL_DIR)/etc/
	install $(INSTALL_FLAGS) --mode=755 ./dist/$(EXECUTABLE_NAME) $(INSTALL_DIR)/bin/
	install $(INSTALL_FLAGS) --mode=640 ./database.sqlite3 $(INSTALL_DIR)/var/db
	install $(INSTALL_FLAGS) --mode=644 ./LICENSE $(INSTALL_DIR)

	@for file in ./sql_scripts/*.sql; do \
		[ -e "$$file" ] && install $(INSTALL_FLAGS) --mode=640 "$$file" /opt/$(EXECUTABLE_NAME)/etc; \
	done

	ln -fs /opt/$(EXECUTABLE_NAME)/bin/$(EXECUTABLE_NAME) /usr/local/bin/$(EXECUTABLE_NAME)
	chown root:$(USERNAME) /usr/local/bin/$(EXECUTABLE_NAME)

uninstall:
	@# Check if the user ID is 0 (root)
	@if [ "$$(id -u)" -ne 0 ]; then \
		printf "Error: Uninstall target must be run with root/sudo\n"; \
		exit 1; \
	fi

	@if id "$(USERNAME)" &>/dev/null; then \
		userdel --remove $(USERNAME); \
  		groupdel $(USERNAME); \
		printf "Removed user and group: '$(USERNAME)'\n"; \
	else \
		printf "Warn: User '$(USERNAME)' does not exist, skipping removal\n"; \
	fi

	@printf "Uninstalling...\n"

	rm $(UNINSTALL_FLAGS) /usr/local/bin/$(EXECUTABLE_NAME)
	rm $(UNINSTALL_FLAGS) /opt/$(EXECUTABLE_NAME)

build: $(VIRTUAL_ENVIRONMENT)
	@# Check if sqlite3 is available
	@command -v sqlite3 >/dev/null 2>&1 || { \
  	printf "Error: sqlite3 is not installed or not in PATH\n"; \
  	exit 1; \
  	}

	sqlite3 database.sqlite3 "CREATE TABLE IF NOT EXISTS $(EXECUTABLE_NAME) ($(EXECUTABLE_NAME))"

	$(VENV_PYINSTALLER) \
		--onefile \
		--name $(EXECUTABLE_NAME) \
		$(SRC_ENTRY)
clean:
	rm $(UNINSTALL_FLAGS) ./build ./dist ./$(VIRTUAL_ENVIRONMENT) ./$(EXECUTABLE_NAME).spec ./database.sqlite3

$(VIRTUAL_ENVIRONMENT): requirements.txt
	@# If the VIRTUAL_ENVIRONMENT doesn't exist, create one with the command on the right side of the OR operator
	test -d $(VIRTUAL_ENVIRONMENT) || python -m venv $(VIRTUAL_ENVIRONMENT)

	$(VENV_PIP) install --require-virtualenv --require-hashes --force-reinstall --no-cache-dir -r requirements.txt
	$(VENV_PIP) install pyinstaller

.PHONY: help install uninstall build clean
