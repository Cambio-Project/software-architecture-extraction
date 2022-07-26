# software-architecture-extraction
This project is capable of creating an architectual model out of runtime data (traces) of a microservice-application.

The models can be used as input for [MiSim](https://github.com/Cambio-Project/resilience-simulator) and [RESIRIO](https://github.com/Cambio-Project/hazard-elicitation).
In the following, there will be an overview of the whole project.
For details, consider visiting the Wiki.

## Input
The entry point of the extractor is the python-file _model2arch.py_.
Run it via a command-line without any arguments.
You will get asked for each necessary input in an interactive manner.

## Resource-Demand-Estimation
Our extractor provides the feature of estimating the resource demands of an operation of a microservice.
To do that the extractor needs additional knowledge about the systems where the microservice ran.
The knowledge consists of the capacities of each microservice and the cpu-utilizations of each hosts in the time intervall the traces were measured.

Out of this information, we use the library [LibREDE](https://se.informatik.uni-wuerzburg.de/software-engineering-group/tools/librede/) to calculate the estimations.
Furthermore, you need to install LibReDE yourself and provide a path (via the command-line) while the extractor runs.

## Output
The output will be a file which can be the input of MiSim or RESIRIO.
