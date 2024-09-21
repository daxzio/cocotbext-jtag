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
release:
# 	cat cocotbext/jtag/version.py
# 	@grep -Po '\d\.\d\.\d' cocotbext/jtag/version.py
# 	git tag v${GIT_TAG}
	echo "__version__ = \"${GIT_TAG}\"" > cocotbext/jtag/version.py
# 	git commit -m "Update to version ${GIT_TAG} [skip ci]" cocotbext/jtag/version.py
	git commit -m "Update to version ${GIT_TAG} [skip ci]" cocotbext/jtag/version.py
	git tag -f v${GIT_TAG}
	git push --all
	git push --tags
# 	git tag v0.0.4
#     git push --tags
