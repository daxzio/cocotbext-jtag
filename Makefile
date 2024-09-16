default:
	cd tests/test001 ; make clean sim
	cd tests/test002 ; make clean sim

lint:
	pyflakes cocotbext

format:
	black cocotbext
