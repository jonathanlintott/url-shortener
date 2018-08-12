from flask import jsonify, request, redirect
import re
import secrets
import string

from application import app, db
from application.models import UrlPair


# Django's url validation
URL_REGEX = re.compile(
    r'(^(?:http|ftp)s?://)?'  # optional http:// or https://
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|'
    r'[A-Z0-9-]{2,}\.?)|'  # domain...
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)


def generate_string(size=8):
    """
    Generates a random string up to the given size from any ascii letter or
    digit.

    Parameters
    ----------
    size : int, defaults to 8
        Size of resultant string

    Returns
    -------
    str : Random string
    """
    return ''.join(secrets.choice(string.ascii_letters + string.digits)
                   for _ in range(size))


def validate_url(url):
    """
    Validates the given URL using the django validation rules.

    Parameters
    ----------
    url : str
        The URL to validate

    Returns
    -------
    bool, True if validation is successful
    """
    return re.match(URL_REGEX, url) is not None


@app.route('/shorten_url', methods=['POST'])
def shorten_url():
    """
    Shortens the URL given in the post body by returning an 8 character
    replacement when passed to this host.

    Post Body
    ---------
    {
      'url': '<original url>
    }

    Response
    --------
    201 if successful, with data:
    {
      'shortened_url': '<new url>
    }

    400 if invalid or missing url data
    """
    post_data = request.get_json()
    if not post_data or 'url' not in post_data:
        return jsonify({'error': "Must include 'url' in post data"}), 400

    original_url = post_data['url']

    if not validate_url(original_url):
        return jsonify({'error': 'Not a valid URL'}), 400

    short_url = generate_string()

    url_pair = UrlPair(original_url=original_url, shortened_url=short_url)
    db.session.add(url_pair)
    db.session.commit()

    return jsonify({'shortened_url': request.host_url + short_url}), 201


@app.route('/<string:short_url>')
def retrieve_url(short_url):
    """
    Redirects to an original URL if the original URL has been succcessfully
    passed to the 'shorten_url' endpoint.

    Response
    --------
    302 if successful, redirect to original URL
    404 if original URL not found
    """
    url_pair = UrlPair.query.filter_by(shortened_url=short_url).first()
    if url_pair is None:
        return jsonify({'error': 'No URL found'}), 404

    original_url = url_pair.original_url

    # External redirect only works if URL has protocol prefix
    if '://' not in original_url:
        original_url = 'http://' + original_url

    return redirect(original_url)
