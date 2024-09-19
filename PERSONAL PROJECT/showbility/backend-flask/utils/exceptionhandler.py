from flask import jsonify, request
from werkzeug.exceptions import HTTPException
from utils.slack_webhook import SlackWebHook


def custom_exception_handler(e):

    if isinstance(e, HTTPException):
        response = e.get_response()
        response.data = {
            "code": e.code,
            "name": e.name,
            "description": e.description,
        }
        response.content_type = "application/json"
    else:
        # 그 외 예외에 대한 처리 (Slack 전송)
        message = f"Exception: {str(e)}"
        message += f"\nRequest Path: {request.path}"
        message += f"\nMethod: {request.method}"

        SlackWebHook.send_message(message)

        response = jsonify({
            "code": 500,
            "name": "Internal Server Error",
            "description": "An unexpected error occurred.",
        })
        response.status_code = 500

    return response
