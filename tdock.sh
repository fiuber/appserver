#!/bin/bash

directorio=$(pwd)

docker run -v $directorio:/app -p 5000:5000 app-server nosetests --with-coverage
