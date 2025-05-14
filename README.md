Directory structure:

```
.
├── build.py
├── docs
│   ├── report
│   │   ├── report-filter.lua
│   │   ├── report.md
│   │   ├── report-pandoc.tex
│   │   ├── report.pdf
│   │   └── uc3mreport.cls
│   └── statement.pdf
├── LICENSE.md
├── pyproject.toml
├── requirements.txt
├── setup.py
├── README.md
└── src
    ├── main
    │   └── python
    │       ├── components
    │       │   ├── Boundaries.py
    │       │   ├── Location.py
    │       │   ├── Map.py
    │       │   ├── Radar.py
    │       │   ├── scenarios.json
    │       │   └── SearchEngine.py
    │       ├── main.py
    └── unittest
        ├── data
        │   └── test_cases.json
        └── python
            └── test_map_radar_tests.py
```

To start a virtual environment to install the packages:

```
python -m venv venv
```

And to activate it:

```
source venv/bin/activate
```

> Everything is expected to run on a UNIX environment (Linux machine), as the whole project is tested to run on a Guernika session.

The requirements are listed in `requirements.txt`, installable by running:

```
pip install -r requirements.txt
```

And the project ran using:

```
python ./src/main/python/main.py scenario_X 0.X
```

To run pybuilder with the respective developed tests:

```
pyb
```
