# software-architecture-extraction
This project is capable of creating an architectual model out of runtime data (traces) of a microservice-application.

The models can be used as input for [MiSim](https://github.com/Cambio-Project/resilience-simulator) or [RESIRIO](https://github.com/Cambio-Project/hazard-elicitation).

In the following, there will be an overview of the whole project.
For details, consider visiting our [Wiki](https://github.com/Cambio-Project/software-architecture-extraction/wiki) and the [Wiki of MiSim](https://github.com/Cambio-Project/resilience-simulator/wiki/ArchitectureDescription).

## Input
The entry point of the extractor is the python-file _model2arch.py_.
Run it via a command-line without any arguments.
You will get asked for each needed input in an interactive manner.

## Resource-Demand-Estimation
Our extractor provides the feature of estimating the resource demand of an operation of a microservice.
To do that the extractor not only needs the response-times (which would be retrievable from the traces).
Additionally, it needs knowledge about characteristics of the system where the microservice ran.

By knowledge of the system we mean the cpu-utilizations of each host in the time intervall the microservice ran (or at least in the intervall the host was active (i.e. operations ran on it)).
With this information, we use the library [LibREDE](https://se.informatik.uni-wuerzburg.de/software-engineering-group/tools/librede/) to calculate the estimations.
However, you need to install LibReDE yourself and provide a path to their cloned and built [repository](https://bitbucket.org/librede/librede/src/master/) while the extractor runs.

## Output
The output will be a file which is part of the input for MiSim or RESIRIO.
