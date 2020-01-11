# encoding: utf-8
import logging
import os

import boto3
from flask import Flask, make_response, jsonify
from werkzeug.exceptions import HTTPException

S3_BUCKET = os.environ['S3_BUCKET']
S3_REGION = os.environ.get('S3_REGION', 'us-east-1')
SHORT_DOMAIN = os.environ.get('SHORT_DOMAIN', f'https://{S3_BUCKET}.s3.{S3_REGION}.amazonaws.com')


def json_response(status_code=200, data=None, msg=None):
    return make_response(jsonify({
        'data': data,
        'msg': msg
    }), status_code)


def internal_error(e):
    # pass through HTTP errors
    if isinstance(e, HTTPException):
        return e

    return json_response(500, msg=str(e))


def not_found_error(e):
    return json_response(404, msg=str(e))


def register_error_handlers(app: Flask):
    app.register_error_handler(500, internal_error)
    app.register_error_handler(Exception, internal_error)
    app.register_error_handler(404, not_found_error)


def create_app():
    server = Flask(__name__)
    server.config.from_mapping(
        S3_BUCKET=S3_BUCKET,
        S3_REGION=S3_REGION,
        S3_CLIENT=boto3.client('s3', region_name=S3_REGION),
        SHORT_DOMAIN=SHORT_DOMAIN
    )

    server.logger.setLevel(logging.DEBUG if server.debug else logging.INFO)

    register_error_handlers(server)

    from app import routes
    server.register_blueprint(routes.bp)

    return server
