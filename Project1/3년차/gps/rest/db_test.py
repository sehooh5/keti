from flask import Flask, render_template, Response, request, g, jsonify
from flask_cors import CORS, cross_origin
import json
import sqlite3
import datetime

# DB 생성 (오토 커밋)
conn = sqlite3.connect("tcp_test.db", isolation_level=None, check_same_thread=False)

# 커서 획득
c = conn.cursor()

c.execute(f"SELECT * FROM keti0_save ORDER BY ROWID LIMIT 1")

