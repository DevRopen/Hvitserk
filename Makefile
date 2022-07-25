py ?= python
pip ?= $(py) -m pip
tox ?= tox


help: Makefile
	@echo
	@echo " Choose a command run in Hvitserk:"
	@echo
	@sed -n 's/^##//p' $< | column -t -s ':' |  sed -e 's/^/ /'
	@echo


## config: Install needed dependencies.
.PHONY: config
config:
	$(pip) install --upgrade pip
	$(pip) install -r requirements.test.txt


## test: Run test case.
.PHONY: test
test:
	@echo "\n==> Run Test Cases:"
	$(tox)


## ci: Run all CI checks.
.PHONY: ci
ci: test
	@echo "\n==> All quality checks passed"


## build: Build the package.
.PHONY: build
build:
	$(tox) -e clean
	$(tox) -e build
	twine check dist/*.whl


## version: Get latest version
.PHONY: version
version:
	$(py) setup.py --version


## release: Release to PyPi
release:
	$(py) -m twine upload --repository-url https://upload.pypi.org/legacy/ dist/* --verbose


## install: Install the package locally
.PHONY: install
install:
	$(py) setup.py install


.PHONY: ci
