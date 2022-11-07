# Bogosort Visualiser

Sam McElligott - https://github.com/sammce

This Python (3) program shows the blazingly slow performance of [bogosort](https://en.wikipedia.org/wiki/Bogosort).

# Installation

Clone the repo:

```sh
git clone https://github.com/sammce/bogo.git
```

`cd` into the repo directory:

```sh
cd bogo
```

Setup a Python virtual environment (optional, but recommended):

```sh
python3 -m venv venv
```

Activate the virtual environment (only if you did the last step):

```sh
source venv/bin/activate
```

Install dependencies listed in `requirements.txt`:
The only package this program relies on is [samutil](https://github.com/sammce/samutil), written by yours truly.

```sh
python3 -m pip install -r requirements.txt
```

You can now run the program via:

```sh
python3 bogo.py
```

# Configuration

The following table shows the configurable constants at the top of `bogo.py` and what they're for:
| Name              | Purpose                                             | Default | Type  |
| ----------------- | --------------------------------------------------- | ------- | ----- |
| `LIST_LENGTH`     | The length of the list being sorted by bogo         | 4       | int   |
| `ITERATIONS`      | How many passes the program should do               | 20      | int   |
| `BAR_CHART_DELAY` | The delay, in seconds, between each chart render    | 0.1     | float |
| `BAR_CHART_CHAR`  | The string to use when representing the lists items | "bogo"  | str   |
