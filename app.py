"""
This module contains the Flask application for server configuration.
"""
import secrets
from flask import Flask, render_template, request, redirect, url_for, make_response
from dotenv import load_dotenv
from jinja2 import Environment, FileSystemLoader

from dbs import create_connection, upsert_server_data
from dbs import fetch_all_server_data_as_dicts, delete_server_data

load_dotenv()

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flashing messages

@app.route('/')
def server_panel():
    """
    Display the server panel.

    Returns:
        Response: The response object.
    """
    conn = create_connection()
    servers = fetch_all_server_data_as_dicts(conn)

    return render_template('server_panel.html', servers=servers)

@app.route('/server/add', methods=['GET'])
def add_server():
    """
    Add a new server configuration.

    Returns:
        Response: The response object.
    """

    return render_template('server_form.html', server=None)

@app.route('/server/edit/<int:server_id>', methods=['GET'])
def edit_server(server_id):
    """
    Edit server configuration.

    Args:
        id (int): The ID of the server to edit.

    Returns:
        Response: The response object.
    """

    conn = create_connection()
    servers = fetch_all_server_data_as_dicts(conn)

    server = next((s for s in servers if s['id'] == server_id), None)

    return render_template('server_form.html', server=server)


@app.route('/save_server', methods=['POST', 'PUT'])
def save_server():
    """
    Save server configuration.
    """
    server_id = None if request.form.get('_method') == 'POST' else request.form.get('id')
    name = request.form.get('name')
    auth_type = request.form.get('auth_type', 'config')
    host = request.form.get('host')
    port = request.form.get('port')
    user = request.form.get('user')
    password = request.form.get('password')
    compress = 1 if request.form.get('compress', 'false').lower() in [
        'true', '1', 't', 'y', 'yes'] else 0
    allow_no_password = 1 if request.form.get('allow_no_password', 'false').lower() in [
        'true', '1', 't', 'y', 'yes'] else 0

    form_data_tuple = (
        server_id,
        name,
        auth_type,
        host, port,
        user,
        password,
        compress,
        allow_no_password
    )

    conn = create_connection()
    print(form_data_tuple)
    upsert_server_data(conn, form_data_tuple)

    return redirect(url_for('server_panel'))

@app.route('/server/delete/<int:server_id>')
def delete_server(server_id):
    """
    Delete a server configuration file based on the verbose field.

    Args:
        verbose (str): The verbose field of the server configuration.

    Returns:
        redirect: Redirects to the server panel page.
    """

    conn = create_connection()
    delete_server_data(conn, server_id)

    return redirect(url_for('server_panel'))

def generate_blowfish_secret(length=32):
    """
    Generate a blowfish secret of the specified length.

    Args:
        length (int): The length of the blowfish secret.

    Returns:
        str: The generated blowfish secret.
    """
    return secrets.token_hex(length)


@app.route('/generate_master_config')
def generate_master_config():
    """
    Generate the master configuration file by combining individual configuration files.
    """
    conn = create_connection()
    servers = fetch_all_server_data_as_dicts(conn)
    num_servers = len(servers)

    template_dir = 'templates'
    env = Environment(loader=FileSystemLoader(template_dir))
    template = env.get_template('config_template.txt')
    rendered_config = template.render(
        num_servers=num_servers,
        servers=servers,
        blowfish_secret=generate_blowfish_secret()
    )

    response = make_response(rendered_config)
    response.headers['Content-Disposition'] = 'attachment; filename=config.inc.php'
    response.headers['Content-type'] = 'text/plain'

    return response

if __name__ == '__main__':
    app.run(debug=True)
