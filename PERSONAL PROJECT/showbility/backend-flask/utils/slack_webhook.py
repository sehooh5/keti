import requests
import os

class SlackWebHook:

    url = "https://hooks.slack.com/services/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"

    @classmethod
    def send_message(cls, message):
        if cls.url:
            data = {
                "text": message
            }
            headers = {
                'Content-type': 'application/json'
            }
            # JSON 데이터를 바로 전송
            response = requests.post(cls.url, json=data, headers=headers)

            # 응답이 성공적이지 않을 경우 로그 남기기
            if response.status_code != 200:
                print(f"Failed to send Slack message: {response.status_code}, {response.text}")
        else:
            print("Slack Webhook URL is not set.")

