import response
import sys

code = sys.argv[1]

msg = response.response_message(code)

print(msg)
