# PHPMyAdmin Config File Generator

Simple tool to quickly generate PHPMyAdmin configuration files. This tool is built using Flask and Tailwind CSS. Don't expect much.

## Prerequisites

Before you begin, ensure you have the following installed on your system:

- Node.js and npm (Node Package Manager)
- Python 3.x
- pip (Python Package Installer)

## Getting Started

Follow these steps to get your environment ready and the application running:

### 1. Clone the Repository

First, clone the repository to your local machine using Git:

```bash
git clone git@github.com:kwidoo/pma-config.git
```

### 2. Install Node.js Dependencies

Navigate to the cloned repository's directory and run the following command to install the required Node.js dependencies:

```bash
npm install
```

This will install all the necessary npm packages defined in `package.json`.

### 3. Build CSS

After installing the npm packages, you need to build the CSS for the project. This step compiles the custom styles used by the application. Run the following command:

```bash
npm run build:css
```

### 4. Install Python Dependencies

The application requires certain Python libraries to function properly. Install them using pip:

```bash
pip install -r requirements.txt
```

This command reads the `requirements.txt` file and installs all the Python dependencies listed there.

## Running the Application

```bash
python app.py
```

By default it will start http server on port 5000. You can access the application by visiting `http://localhost:5000` in your browser.

## TODO

[ ] Ceate a Dockerfile to deploy PHPMyAdmin and this tool together.

[ ] Integration via Apache2 configuration in the PHPMyAdmin container.

[ ] Expand the tool's interface to allow configuring a wider range of PHPMyAdmin options, increasing flexibility.

[ ] Apply configurations to PHPMyAdmin automatically, avoiding manual copy/paste conifg.

## License

This project is licensed under the [MIT License](LICENSE) - see the LICENSE file for details.
