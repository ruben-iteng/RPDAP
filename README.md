# Template

This is a template project for new faebryk projects. It contains a basic structure and some examples/templates to get you started.

## Getting started
First press `Use this template` button on the top of the page. 
Then clone your new repo locally:
```bash
git clone <your repo>
cd <your repo>
```

### Fill in the templates
replace `{}` and `<>` placeholders and fill in TODOs in following files:
- [README.md](README.md) (this file)
- [pyproject.toml](pyproject.toml)
- remove this header in this file (up until the first "TEMPLATE README START")

### Setup your environment

Make sure you have python3.11 installed
```bash
python --version
```

If you can't upgrade to python3.11, you will first need to make sure to have a working venv with python3.11 installed in it. This process will differ per OS.

Make sure you have poetry installed
```bash
poetry --version
```

#### Option 1: Static faebryk
```bash
# inside your repo dir
poetry install
poetry shell # This activates the new venv
```

#### Option 2: Editable faebryk
```bash
# inside your repo dir
./scripts/setup_local_faebryk.sh [branch]
poetry shell
```

#### Test if it works
```bash
python src/<project_name>/main.py
```

# TEMPLATE README START
---



<div align="center">

# {project}

<img height=300 title="Render" src="./render.png"/>
<br/>

{MiniDescription} - {project}

[![Version](https://img.shields.io/github/v/tag/<owner>/<project>)](https://github.com/<owner>/<project>/releases) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/<owner>/<project>/blob/main/LICENSE) [![Pull requests open](https://img.shields.io/github/issues-pr/<owner>/<project>)](https://github.com/<owner>/<project>/pulls) [![Issues open](https://img.shields.io/github/issues/<owner>/<project>)](https://github.com/<owner>/<project>/issues) [![GitHub commit activity](https://img.shields.io/github/commit-activity/m/<owner>/<project>)](https://github.com/<owner>/<project>/commits/main) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

</div>

## About

<div align="center">
<img height=200 title="Overview" src="./overview.png"/>
</div>

TODO: description
This project is build with the open-source EDA [faebryk](https://github.com/faebryk/faebryk).

## What can you do with this project?

TODO

## Working with the source files

See [here](./docs/development.md) for the instructions on how to install and edit this project.

## Building

If you want to build the physical output of this project you can find the build instructions [here](./docs/build_instructions.md).

## Contributing

If you want to share your alterations, improvements, or add bugfixes to this project, please take a look at the [contributing guidelines](./docs/CONTRIBUTING.md).

## Community Support

Community support is provided via Discord; see the Resources below for details.

### Resources

- Source Code: [Github#TODO]()
- Chat: Real-time chat happens in faebryk's Discord Server (chit-chat room for now). Use this Discord [Invite](https://discord.gg/95jYuPmnUW) to register
- Issues: [Issues#TODO]()
