from flask import Flask, render_template, request, redirect, url_for, flash
import os
import re
import glob

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

def read_php_config_to_dict(file_path):
    # Define a regex pattern to match the PHP config lines
    pattern = re.compile(r"\$cfg\['Servers'\]\[\$i\]\['(\w+)'\]\s*=\s*(.*?);")

    # Initialize a dictionary to store the config
    config = {}

    # Read the file
    with open(file_path, 'r') as file:
        content = file.read()

        # Find all matches of the pattern
        matches = pattern.findall(content)

        # Process each match
        for key, value in matches:
            # Remove quotes from the value if it's a string
            processed_value = value.strip("'").strip('"')

            # Convert boolean strings to Python booleans
            if processed_value.lower() == 'false':
                processed_value = False
            elif processed_value.lower() == 'true':
                processed_value = True
            elif processed_value.isdigit():
                processed_value = int(processed_value)

            # Assign the processed value to the corresponding key in the config dictionary
            config[key] = processed_value

    return config



# Assuming the read_php_config_to_dict function is already defined

def read_all_php_configs(directory_path):
    configs = []

    # Construct the path pattern to match all PHP files in the directory
    path_pattern = os.path.join(directory_path, '*.php')

    # Use glob to find all files matching the pattern
    php_files = glob.glob(path_pattern)

    # Iterate over the list of file paths
    for idx, file_path in enumerate(php_files, start=1):
        # Use the previously defined function to convert each file's contents to a dict
        config_dict = read_php_config_to_dict(file_path)
        config_dict['id'] = idx
        configs.append(config_dict)

    return configs

# Example usage
directory_path = './configs'
servers = read_all_php_configs(directory_path)

@app.route('/')
def server_panel():
    # Example server list
    servers = read_all_php_configs('./configs')

    return render_template('server_panel.html', servers=servers)

@app.route('/server/add', methods=['GET'])
def add_server():
    if request.method == 'POST':
        # Process your form data here, for example:
        name = request.form.get('name')
        ip = request.form.get('ip')
        servers.append({'id': len(servers)+1, 'name': name, 'ip': ip})

        # Normally, you would add the data to the database
        # For now, just redirect to the server list
        return redirect(url_for('server_panel'))
    return render_template('server_form.html', server=None)

@app.route('/server/edit/<int:id>', methods=['GET'])
def edit_server(id):
    server = next((s for s in servers if s['id'] == id), None)
    if request.method == 'POST':
        name = request.form.get('name')
        ip = request.form.get('ip')
        servers[id-1]['name'] = name
        servers[id-1]['ip'] = ip

        return redirect(url_for('server_panel'))
    return render_template('server_form.html', server=server)


@app.route('/save_server', methods=['POST'])
def save_server():
    # Extract form data
    verbose = request.form.get('verbose')  # Default to 'local' if not provided
    auth_type = request.form.get('auth_type', 'config')
    host = request.form.get('host')
    port = request.form.get('port')
    user = request.form.get('user')
    password = request.form.get('password')
    compress = request.form.get('compress', 'false').lower() in ['true', '1', 't', 'y', 'yes']
    allow_no_password = request.form.get('allow_no_password', 'false').lower() in ['true', '1', 't', 'y', 'yes']

    # Derive filename from server name (user input) and sanitize it
    filename = f"{verbose.replace(' ', '_').lower()}.php"  # Replace spaces with underscores and convert to lowercase for filename
    filepath = os.path.join('./configs', filename)  # Adjust path as necessary

    # Generate or update the PHP configuration file for the server
    with open(filepath, 'w') as file:
        file.write(f"$cfg['Servers'][$i]['verbose'] = '{verbose}';\n")
        file.write(f"$cfg['Servers'][$i]['auth_type'] = '{auth_type}';\n")
        file.write(f"$cfg['Servers'][$i]['host'] = '{host}';\n")
        file.write(f"$cfg['Servers'][$i]['port'] = '{port}';\n")
        file.write(f"$cfg['Servers'][$i]['user'] = '{user}';\n")
        file.write(f"$cfg['Servers'][$i]['password'] = '{password}';\n")
        file.write(f"$cfg['Servers'][$i]['compress'] = {str(compress).lower()};\n")
        file.write(f"$cfg['Servers'][$i]['AllowNoPassword'] = {str(allow_no_password).lower()};\n")
        file.write(f"$i++;\n")

    # Redirect or respond as necessary after saving
    return redirect(url_for('server_panel'))

@app.route('/delete/<verbose>')
def delete_server(verbose):
    # Create the filename from the verbose field
    filename = f"{verbose.replace(' ', '_').lower()}.php"  # Replace spaces with underscores and convert to lowercase for filename
    filepath = os.path.join('./configs', filename)  # Adjust path as necessary

    # Check if file exists and delete it
    if os.path.exists(filepath):
        os.remove(filepath)
        flash(f'Successfully deleted {verbose}.', 'success')
    else:
        flash(f'File {verbose} not found.', 'error')

    # Redirect to the server panel page
    return redirect(url_for('server_panel'))

@app.route('/generate_master_config')
def generate_master_config():
    # Path for the master config file
    master_config_path = os.path.join('./', 'config.inc.php')

    # Open the master config file in write mode to overwrite existing content
    with open(master_config_path, 'w') as master_file:
        # Write the PHP opening tag
        master_file.write("<?php\n\n")
        master_file.write("declare(strict_types=1);\n\n")
        master_file.write("$cfg['blowfish_secret'] = '';\n\n")
        master_file.write("$i = 1;\n\n")

        # Iterate over each PHP file in the directory except the master config file
        for config_file in glob.glob(os.path.join(directory_path, '*.php')):
            if os.path.basename(config_file) != 'config.inc.php':
                # Read the content of the current config file
                with open(config_file, 'r') as individual_file:
                    content = individual_file.read()
                    # Write the content of the current config file to the master file
                    master_file.write(content + "\n")

        # Optionally, write the PHP closing tag
        master_file.write("$cfg['UploadDir'] = '';\n")
        master_file.write("$cfg['SaveDir'] = '';\n\n")
        master_file.write("$cfg['MaxTableList'] = 5000;\n\n")
        master_file.write("$cfg['MaxNavigationItems']=1000;\n\n")
        master_file.write("?>")
    return redirect(url_for('server_panel'))

# Example usage

if __name__ == '__main__':
    app.run(debug=True)
