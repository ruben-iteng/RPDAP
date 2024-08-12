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
replace the following placeholders:

| Topic   | Tag          | Replace with              |
| ------ | ------------ | ------------------------- |
| git     | `<owner>`    | repository owner          |
| git     | `<project>`  | project name              |
| git     | `<faebryk_branch>` | branch name of faebryk you want to use. e.g: `main` |
| project | `<project_name>` | name of this new faebryk project |
| project | `<project_path_name>` | name of this new faebryk project but for usage in file paths |
| project | `<detailed_project_description>` | detailed project description |
| project | `<short_project_description>` | short project description |
| project | `<authors>` | list of project authors. e.g: `"A Author", "B Author"` |
| project | `<licence>` | licence type e.g: `MIT`. See [here](https://python-poetry.org/docs/pyproject#license) and [here](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/licensing-a-repository) for more option|
| project | `<version>` | version e.g: `0.0.1`|

- Manually rename src/project_name accordingly (<project_name> in all lowercase, no spaces)
- Then replace all imports accordingly with following command:
- ```find src -type f -name "*.py" -exec sed -i 's/project_name/<project_name>/g' {} +```
- Search for `#TODO` and fill in the required information
- Remove this header in this file (up until the first "TEMPLATE README START")

**Note: if you are not using github you have to mannually change all links and tags

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

#optional: pick alternative faebryk version, see poetry doc for more options
poetry add git+https://github.com/faebryk/faebryk.git#<branch>

poetry install
poetry shell # This activates the new venv
```

#### Option 2: Editable faebryk
```bash
# inside your repo dir
./scripts/setup_local_faebryk.sh [<branch>]
poetry shell
```

#### Test if it works
```bash
python src/<project_name>/main.py
```

# TEMPLATE README START
---



<div align="center">

# <project_name>

<img height=300 title="Render" src="./render.png"/>
<br/>

<short_project_description> - <project_name>

[![Version](https://img.shields.io/github/v/tag/<owner>/<project>)](https://github.com/<owner>/<project>/releases) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/<owner>/<project>/blob/main/LICENSE) [![Pull requests open](https://img.shields.io/github/issues-pr/<owner>/<project>)](https://github.com/<owner>/<project>/pulls) [![Issues open](https://img.shields.io/github/issues/<owner>/<project>)](https://github.com/<owner>/<project>/issues) [![GitHub commit activity](https://img.shields.io/github/commit-activity/m/<owner>/<project>)](https://github.com/<owner>/<project>/commits/main) [![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

</div>

## About

<div align="center">
<img height=200 title="Overview" src="./overview.png"/>
</div>

<short_project_description>
This project is build with the open-source EDA [faebryk](https://github.com/faebryk/faebryk).

## What can you do with this project?

<detailed_project_description>

## Working with the source files

See [here](./docs/development.md) for the instructions on how to install and edit this project.

## Building

If you want to build the physical output of this project you can find the build instructions [here](./docs/build_instructions.md).

## Contributing

If you want to share your alterations, improvements, or add bugfixes to this project, please take a look at the [contributing guidelines](./docs/CONTRIBUTING.md).

## Community Support

Community support is provided via Discord; see the Resources below for details.

### Resources

- Source Code: [Github](https://github.com/<owner>/<project>)
- Chat: Real-time chat happens in faebryk's Discord Server (chit-chat room for now). Use this Discord [Invite](https://discord.gg/95jYuPmnUW) to register
- Issues: [Issues](https://github.com/<owner>/<project>/issues)
