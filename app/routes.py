# encoding: utf-8
from urllib.parse import urlparse

import shortuuid
from botocore.exceptions import ClientError
from flask import Blueprint, request
from flask import current_app as app, render_template

from app import json_response

bp = Blueprint('', __name__, url_prefix='')


def generate_alias():
    return shortuuid.uuid()


def is_path_available(path: str):
    try:
        s3 = app.config['S3_CLIENT']
        s3.head_object(Bucket=app.config['S3_BUCKET'], Key=path)
    except ClientError as e:
        if e.response['Error']['Code'] == '404':
            app.logger.info(f'path {path} already exists')
            return True
        else:
            app.logger.error(e)
            raise e

    return False


def create_redirect_file(url: str, alias: str):
    try:
        res = app.config['S3_CLIENT'].put_object(
            Bucket=app.config['S3_BUCKET'],
            Key=alias,
            ACL='public-read',
            WebsiteRedirectLocation=url
        )
    except ClientError as e:
        app.logger.error(e)
        raise e

    return True


def get_short_url(path):
    base_url = app.config.get('SHORT_DOMAIN')
    return f'{base_url}/{path}'


@bp.route('/')
@bp.route('/index')
def index():
    return render_template('index.html')


@bp.route('/create', methods=['POST'])
def create():
    if request.method != 'POST':
        return json_response(405, msg='Method Not Allowed')

    req = request.get_json()

    url = req.get('url')
    if not url:
        return json_response(400, msg='URL is required')

    try:
        o = urlparse(url)

        if not o.scheme or not o.netloc:
            return json_response(400, msg='URL is invalid')

    except ValueError as e:
        return json_response(400, msg=str(e))

    alias = req.get('alias', generate_alias())

    if not is_path_available(alias):
        return json_response(409, msg='Alias already exists')

    if not create_redirect_file(url, alias):
        return json_response(500, msg='Create alias failed')

    return json_response(201, data={
        'path': alias,
        'url': get_short_url(alias)
    }, msg='Alias created')
