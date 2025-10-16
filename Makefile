.PHONY: help clean clean-remote clean-all push pull sync sync-remote sync-local


clean:
	@echo "Starting reset..."
	@find . -mindepth 1 \
		! -name 'Makefile' \
		-exec rm -rf {} + \
		&& echo "Removed all files except Makefile."
	@echo "# Playground\n\nThis is a test repo." > README.md
	@echo "Created README.md"
	@git init
	@echo "Initialized new git repository."
	@git add Makefile README.md
	@git commit -m "initial commit"
	@echo "Committed Makefile and README.md."
	@git remote add origin git@github.com:jd-35656/playground.git || echo "Remote origin already exists."
	@echo "Reset complete."


clean-remote:
	@echo "Deleting remote repository 'playground'..."
	@gh repo delete jd-35656/playground --yes \
		&& echo "Repository deleted." || { echo "Failed to delete repo or repo does not exist."; }
	@echo "Recreating public repository 'playground' with description..."
	@gh repo create jd-35656/playground --public --description "This is a test repo." \
		&& echo "Repository recreated as public with description." || { echo "Failed to create repo."; exit 1; }
	@echo "Remote repository reset complete."


push:
	@echo "Pushing to origin main (force)..."
	@git push origin main --force \
		&& echo "Push complete!"


clean-all: clean clean-remote push
	@echo "Clean complete."


TEMP_DIR := .temp-sync
REPO_URL := git@github.com:jd-35656/playground.git

sync:
	@echo "Cloning fresh repo into $(TEMP_DIR)..."
	@rm -rf $(TEMP_DIR)
	@git clone --no-single-branch $(SYNC_REPO) $(TEMP_DIR)
	@git fetch --all --tags
	@echo "Removing current repo content..."
	@find . -mindepth 1 ! -regex './$(TEMP_DIR).*' -exec rm -rf {} +
	@echo "Replacing current repo with fresh clone..."
	@cp -r $(TEMP_DIR)/. .
	@rm -rf $(TEMP_DIR)
	@echo "Sync complete."


pull:
	@echo "Fetching origin..."
	@git fetch origin
	@echo "Stashing local changes (including untracked)..."
	@git stash push -u -m "auto-stash before pull"
	@echo "Merging origin/main..."
	@if ! git merge origin/main; then \
		echo "Merge conflicts detected! Please resolve manually."; \
		echo "You can use 'git merge --abort' to cancel the merge."; \
		echo "Stashed changes are saved, but stash pop skipped to avoid conflicts."; \
		exit 1; \
	else \
		echo "Merge successful."; \
		echo "Applying stashed changes..."; \
		if git stash pop; then \
			echo "Stash applied successfully."; \
		else \
			echo "Conflicts occurred applying stash. Please resolve manually."; \
		fi \
	fi
	@echo "Pull complete!"


TEMP_DIR := .temp-sync

SYNC_REPO_PART := $(shell echo $(URI) | cut -d'@' -f1)
SYNC_REF_PART := $(shell echo $(URI) | grep '@' >/dev/null && echo $(shell echo $(URI) | cut -d'@' -f2) || echo "")

SYNC_REPO := git@github.com:$(SYNC_REPO_PART).git

sync-remote: clean-all
	@if [ -z "$(URI)" ]; then \
		echo "Error: You must specify URI variable, e.g. `make sync-from URI=jd-35656/playground`"; \
		exit 1; \
	fi
	@echo "Syncing from repo: $(SYNC_REPO)"
	@rm -rf $(TEMP_DIR)
	@mkdir -p $(TEMP_DIR)
	@echo "Cloning repo..."
	@git clone --no-single-branch $(SYNC_REPO) $(TEMP_DIR)/repo
	@if [ -n "$(SYNC_REF_PART)" ]; then \
		echo "Checking out ref: $(SYNC_REF_PART)"; \
		cd $(TEMP_DIR)/repo && \
		git fetch --all --tags && \
		if git rev-parse --verify --quiet "origin/$(SYNC_REF_PART)"; then \
			git checkout -b $(SYNC_REF_PART) origin/$(SYNC_REF_PART); \
		elif git rev-parse --verify --quiet "$(SYNC_REF_PART)"; then \
			git checkout $(SYNC_REF_PART); \
		else \
			echo "Error: Ref '$(SYNC_REF_PART)' not found in remote or tags." && exit 1; \
		fi; \
	else \
		echo "No ref specified, using default branch"; \
	fi
	@echo "Copying files (excluding .git and Makefile) to current directory..."
	@rsync -av --exclude='.git' --exclude='Makefile' $(TEMP_DIR)/repo/ ./
	@if [ -f "$(TEMP_DIR)/repo/Makefile" ]; then \
		cp "$(TEMP_DIR)/repo/Makefile" "./Makefile-source"; \
		echo "Makefile from cloned repo renamed to Makefile-source."; \
	else \
		echo "No Makefile found in cloned repo."; \
	fi
	@rm -rf $(TEMP_DIR)
	@echo "Adding, committing, and pushing changes..."
	@git add .
	@git commit -m "Sync from $(SYNC_REPO) $(if $(SYNC_REF_PART),at $(SYNC_REF_PART),at default branch)" || echo "No changes to commit."
	@git push origin main --force
	@echo "Sync complete."


sync-local: clean-all
	@if [ -z "$(URI)" ]; then \
		echo "Error: You must specify URI variable, e.g. `make sync-local URI=../my-repo`"; \
		exit 1; \
	fi

	@if [ ! -d "$(URI)" ]; then \
		echo "Error: URI '$(URI)' does not exist or is not a directory."; \
		exit 1; \
	fi

	@echo "Syncing from local URI: $(URI)"

	@echo "Copying files (excluding .git and Makefile) to current directory..."
	@rsync -av --exclude='.git' --exclude='Makefile' $(URI)/ ./

	@if [ -f "$(URI)/Makefile" ]; then \
		cp "$(URI)/Makefile" "./Makefile-source"; \
		echo "Makefile from cloned repo renamed to Makefile-source."; \
	else \
		echo "No Makefile found in source path."; \
	fi

	@echo "Adding, committing, and pushing changes..."
	@git add .
	@git commit -m "Local sync from $(URI)" || echo "No changes to commit."
	@git push origin main --force

	@echo "Local sync complete."

help:
	@echo "Available make targets:"
	@echo "  help                      - Show this text"
	@echo "  clean                     - Clean local directory, reinitialize repo, commit Makefile & README."
	@echo "  clean-remote              - Delete and recreate remote GitHub repo (public, with description)."
	@echo "  clean-all                 - Run reset, reset-remote, then push (full cleanup)."
	@echo "  push                      - Force push local main branch to origin."
	@echo "  pull                      - Fetch origin, stash changes, merge origin/main, then pop stash with conflict handling."
	@echo "  sync                      - Sync local repo to exactly match remote repo (all branches and tags, hard reset and clean)."
	@echo "  sync-from URI=\"user/repo[@ref]\" - Sync current repo files from another remote repo at optional ref (branch or tag)."
	@echo "  sync-local URI=\"/path/to/local/dir\" - Sync current repo files from a local path."
