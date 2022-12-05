# Assignment 5: Strømpris API
## About the project
This project implements "Strømpris" dashboard.

Data on electricity prices are fetched from the [`hvakosterstommen.no`](https://www.hvakosterstrommen.no) API.
The gathered data are then presented via locally hosted webserver using `Altair` and `FastAPI`. Some interactive functionality is also implenmented.

---
## Configuring the environment

The installation is done using `conda`.

To set up the environment for this assignment,
navigate to the folder of the `Assignment 5` and run in the terminal the following commands:

```
conda create -n assignment5 python=3.9.14 
conda activate assignment5
pip install -r requirements.txt
```

---

## How to run the Strømpris dashboard
- create Python environment.
- run `python app.py` in the terminal.
- navigate to the page `127.0.0.1:5000` in your broswer.

To run tests for all tasks use the following command:
`python3 -m pytest -v tests/*`


---
## Implementation details

**The following tasks are implemented:**
- 5.1 Price Plotter (10 points) - **fully**
- 5.2: Becoming a Web Developer with FastAPI (5 points) - **fully**
- 5.3: Interactive Visualization: Upgrading to Pro-Level (10 points) - **fully**
- 5.4: Advanced visualization (10 points IN4110 only) - **only the first part**
- 5.5: Documentation and Help Page (5 points) -  **the first part and navigation bar**

**Known issues:**
- The `"Help"` subpage does not link to the Sphinx documentation. HTML command ` <a href="/docs/_build/html/index.html">Help</a>` does not do the job.

- The `test_plot_daily_prices` fails, because the function `plot_daily_prices` is not implemented.

---


Also, the deadline for this assignment was stated in the email from the course instructor as December 2 with an additional extension of 3 days on an approved request for `assemm@uio.no`.

