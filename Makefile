clean:
	rm -fr build/
	rm -fr dist/
	rm -fr *.egg-info
	find . -name '*.pyc' -exec rm -f {} +
	find . -name '*.pyo' -exec rm -f {} +
	find . -name '*~' -exec rm -f {} +

lint:
	flake8 pit

docs:
	rm -f docs/source/pit.rst
	rm -f docs/source/modules.rst
	sphinx-apidoc -o docs/ pit
	$(MAKE) -C docs clean
	$(MAKE) -C docs html

dist: 	clean
	python setup.py sdist bdist_wheel

testupload: dist
	twine upload --repository-url https://test.pypi.org/legacy/ dist/*

release: dist
	twine upload upload dist/*

help:
	@echo "clean - remove build and dist files"
	@echo "lint - lint with flake8"
	@echo "docs - generate documentation with Spinx"
	@echo "dist - package"
	@echo "testupload - package and upload a release to test.pypi.org"
	@echo "release - package and upload a release"
