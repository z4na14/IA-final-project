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
├── src
│   ├── main
│   │   └── python
│   │       ├── components
│   │       │   ├── Boundaries.py
│   │       │   ├── Location.py
│   │       │   ├── Map.py
│   │       │   ├── Radar.py
│   │       │   ├── scenarios.json
│   │       │   └── SearchEngine.py
│   │       ├── main.py
│   └── unittest
│       ├── data
│       │   └── test_cases.json
│       └── python
│           └── test_map_radar_tests.py
```

Where the requirements are listed insisde the `requirements.txt`, installable by running:

```
pip install -r requirements.txt
```

And the project ran using:

```
python ./src/main/python/main.py scenario_X 0.X
```