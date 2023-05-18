
test: venv
	./venv/bin/python3 -m unittest test_cjson.py
		
venv:
	python3 -m venv venv
	./venv/bin/python3 setup.py install

clean:
	rm -rf __pycache__
	rm -rf venv
