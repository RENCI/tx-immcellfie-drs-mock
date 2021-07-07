#!/bin/bash
docker run -d --name drs-mock --network host --restart always --volume $PWD/phenotype.csv:/phenotype.csv:ro --volume $PWD/gene.csv:/gene.csv:ro --env API_HOST=$(hostname) --env API_PORT=80 drs-mock:0.1

