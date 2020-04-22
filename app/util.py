from flask import url_for
from werkzeug.utils import secure_filename
from werkzeug.security import pbkdf2_hex
from app import app
import time
import os

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

def allowed_file(filename):
    """
    Returns True if *filename* is an allowed filename, or False otherwise.

    Parameters
    ----------
    filename : str
        The name of a file to be uploaded

    Returns
    -------
    bool
        True if *filename* is valid, False otherwise

    Raises
    ------
    TypeError
        If *filename* is not a string

    Examples
    --------
    >>> allowed_file('an_image.jpg')
    True
    >>> allowed_file('not_an_image.pdf')
    False
    """
    
    if type(filename) != str:
        raise TypeError('Filename must be a string')

    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_file(filestorage, hash=True):
    """
    Saves a file to upload folder and returns the absolute URL to the saved image.

    Pararmeters
    -----------
    filestorage : FileStorage
        The FileStorage object that Flask provides from a form file input (e.g. request.files['file'])
    hash : bool
        Whether to hash the name of the file or not

    Returns
    -------
    str or None
        The absolute URL where the saved image is stored, or None if saved image was not stored.

    Examples
    --------
    >>> save_file(file)
    'http://localhost:5000/static/img/uploads/2651ab247cffe084048759f87b2c9d15f6bc437c7ed3a8e8eab1b9e4f04a3d13.jpg'
    >>> save_file(invalid_file)
    None
    """

    if allowed_file(filestorage.filename):
        filename = filestorage.filename
        # Hash with appended timestamp, if appropriate
        if hash:
            parts_of_filename = secure_filename(filename).rsplit('.', 1)
            filename = '.'.join([pbkdf2_hex(parts_of_filename[0] + str(time.time()), app.config['SECURITY_PASSWORD_SALT']), parts_of_filename[1]])
        
        # Save and get url
        filestorage.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        url = url_for('static', filename=os.path.join(app.config['UPLOAD_FOLDER'].split('/', 1)[1], filename), _external= True)
        return url

    return None