SIM?=icarus

default:
	cd tests/test001 ; make clean sim
	cd tests/test002 ; make clean sim

lint:
	pyflakes cocotbext

format:
	black cocotbext

dist:
	rm -rf MANIFEST 
	rm -rf CHANGELOG.txt
	python setup.py sdist

GIT_TAG?=0.0.5
VERSION_FILE?=`find . -name version.py`
release:
	echo "Release v${GIT_TAG}"
# 	cat cocotbext/jtag/version.py
# 	@grep -Po '\d\.\d\.\d' cocotbext/jtag/version.py
	git tag v${GIT_TAG}
	echo "__version__ = \"${GIT_TAG}\"" > ${VERSION_FILE}
	git add ${VERSION_FILE}
	git commit -m "Update to version ${GIT_TAG}"
	git tag -f v${GIT_TAG}
	git push --all
	git push --tags

