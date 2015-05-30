all: train test

dir:
	mkdir -p data/raw
	mkdir -p data/feature
	mkdir -p data/model
	mkdir -p data/result

train:
	cd src && python train.py

test:
	cd src && python test.py
