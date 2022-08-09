# software-architecture-extraction
This tool is capable of creating an architectual model out of runtime data (traces) of a microservice-application.
The models can be used as input for [MiSim](https://github.com/Cambio-Project/resilience-simulator) or [RESIRIO](https://github.com/Cambio-Project/hazard-elicitation).

In the following, there will be a short overview of the whole project.
For details, consider visiting our [Wiki](https://github.com/Cambio-Project/software-architecture-extraction/wiki) and the [Wiki of MiSim](https://github.com/Cambio-Project/resilience-simulator/wiki/ArchitectureDescription).

Requirements:
- Python 3.9 or higher
- Installation of the requirements described in the file `requirements.txt`, e.g. with `pip install -r requirements.txt`
---
## Input
The entry point of the extractor is the python-file `model2arch.py`.

Run it via a console without any arguments.
You will get asked for each needed input in an interactive manner.
The main input will be either [Jaeger](https://www.jaegertracing.io/)-, [Zipkin](https://zipkin.io/) or [OPEN.xtrace](https://github.com/spec-rgdevops/OPEN.xtrace)-Traces which are used to create an architectual model.

## Output
The output will be a file which is part of the input for MiSim or RESIRIO.
