.DEFAULT_GOAL := help
.NOTPARALLEL:
.PHONY: help preflight bootstrap provision prepare cluster kubeconfig addons validate install status start stop ssh incident recovery test
help:
	@python3 scripts/lab.py help
preflight bootstrap provision prepare cluster kubeconfig addons validate install status start stop:
	@python3 scripts/lab.py $@
ssh:
	@python3 scripts/lab.py ssh --node "$(NODE)"
incident:
	@./scripts/incident.sh --help
recovery:
	@./scripts/recovery.sh --help
test:
	@python3 -m unittest discover -s tests -v
