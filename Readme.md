# PHPMyAdmin Config File Generator

Simple tool to quickly generate PHPMyAdmin configuration files. This tool is built using Flask and Tailwind CSS. Don't expect much.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Python 3.x
- pip (Python Package Installer)
- Optional: Node.js and npm (Node Package Manager)

## Getting Started

Follow these steps to get your environment ready and the application running:

### 1. Clone the Repository

First, clone the repository to your local machine using Git:

```bash
git clone git@github.com:kwidoo/pma-config.git
```

### 3. Install Python Dependencies

The application requires certain Python libraries to function properly. Install them using pip:

```bash
pip install -r requirements.txt
```

This command reads the `requirements.txt` file and installs all the Python dependencies listed there.

## Create database

```bash
python install.py
```

## Running the Application

```bash
python app.py
```

By default it will start http server on port 5000. You can access the application by visiting `http://localhost:5000` in your browser.

## Generate config.inc.php

Click on the "Generate Config" button to generate the configuration file. The file will be downloaded to your system. Put it to your phpMyAdmin installation directory.

## Optional: Install Tailwind CSS

If you want to make changes to the CSS, you need to install Tailwind CSS. First, install the required Node.js packages:

```bash
npm install
```

Edit styles.css and run the following command to compile the CSS:

```bash
npm run build:css
```

## TODO

[ ] Ceate a Dockerfile to deploy PHPMyAdmin and this tool together.

[ ] Integration via Apache2 configuration in the PHPMyAdmin container.

[ ] Expand the tool's interface to allow configuring a wider range of PHPMyAdmin options, increasing flexibility.

[ ] Apply configurations to PHPMyAdmin automatically, avoiding manual copy config file.

## License

This project is licensed under the [MIT License](LICENSE) - see the LICENSE file for details.
