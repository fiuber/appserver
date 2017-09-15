#!/bin/bash
#SE USA PARA CORRERLO LOCAL
directorio=$(pwd)
docker run -e "PORT=5000" -v $directorio:/app -p 5000:5000 app-server sh exec.sh
