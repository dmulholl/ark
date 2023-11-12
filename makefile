help:
	@cat ./makefile

build:
	./setup.py sdist bdist_wheel

publish:
	./setup.py sdist bdist_wheel
	twine upload dist/*

clean:
	rm -rf ./build
	rm -rf ./dist
	rm -rf ./*.egg-info
