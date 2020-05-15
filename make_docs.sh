#!/bin/sh
# ---------------------------------------------#
# Shell script to make generating docs easier. #
# ---------------------------------------------#
if [ "$(docker ps -q -f name=ose3dprinter-docs)" ]; then
    docker exec -it ose3dprinter-docs rm -rf docs/ose3dprinter && \
        docker exec -it ose3dprinter-docs make clean && \
        docker exec -it ose3dprinter-docs make html
else
    echo "Docs container not running. Start it by excecuting the following command:\n"
    echo "    docker-compose up -d\n"
fi
