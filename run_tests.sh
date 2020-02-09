#!/bin/sh
# -------------------------------------------#
# Shell script to make running tests easier. #
# -------------------------------------------#
if [ "$(docker ps -q -f name=ose3dprinter-test)" ]; then
    docker exec -it ose3dprinter-test pytest test/
else
    echo "Test container not running. Start it by excecuting the following command:\n"
    echo "    docker-compose up -d\n"
fi
