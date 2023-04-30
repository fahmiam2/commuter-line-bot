# KRL Telegram Bot

This project is a Telegram bot that provides users with schedule and fare information for KRL (Kereta Rel Listrik) trains in Indonesia. It uses the `python-telegram-bot` library and the KRL API to retrieve train schedule and fare information based on user input.

## Table of Contents

- [KRL Telegram Bot](#krl-telegram-bot)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Requirements](#requirements)
  - [Installation](#installation)
  - [Usage](#usage)
  - [Contributing](#contributing)
  - [License](#license)

## Features

- Retrieve KRL train schedule information based on the station name and time range.
- Retrieve KRL train fare information based on the departure and destination station names.

## Requirements

- Python 3.6 or higher
- python-telegram-bot library
- requests library
- pytz library

## Installation

1. Clone the repository to your local machine:

```bash
git clone https://github.com/fahmiam2/krl-telegram-bot.git
```

2. Create and activate a virtual environment (optional but recommended):

- Pyenv virtualenv

```bash
pyenv virtualenv <python_version> <env_name>
```
- virtualenv

```bash
python <version> -m venv <virtual-environment-name>
```

to activate python environment on windows:

```bash
<virtual-environment-name>\Scripts\activate
```
to activate python environment on MacOS+Linux:

```bash
source <virtual-environment-name>/bin/activate
```

3. Install the required packages:
   
```shell
pip install requirement.txt
```

4. Replace "YOUR_BOT_TOKEN" in the `krl_bot.py` script with your actual Telegram bot token.

## Usage

1. Run the Telegram bot:

```shell
python3 main_bot.py
```

2. Interact with the bot on Telegram by sending messages containing station names and time ranges to get schedule and fare information.

## Contributing

1. Fork the repository on GitHub.
2. Create a new branch for your feature or bugfix.
3. Commit your changes to the new branch.
4. Push the branch to your fork on GitHub.
5. Create a pull request from your branch to the original repository.

## License

This project is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for details.
