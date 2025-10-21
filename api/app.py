# Flask API를 완성하세요.
# 요구사항:
# - 데이터 파일 경로: /app/data/expenses.json  (초기 내용: [])
# - GET  /api/records   : 저장된 데이터를 JSON으로 반환
# - POST /api/records   : {title, amount, date} 저장 (유효성 검사 포함)
# - GET  /api/summary   : {count, total} 반환
# - GET  /api/download  : expenses.json 파일 다운로드

from flask import Flask, request, jsonify, send_file
from pathlib import Path
import json, os

app = Flask(__name__)

DATA_PATH = Path("/app/data/expenses.json")
DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
if not DATA_PATH.exists():
    DATA_PATH.write_text("[]", encoding="utf-8")

@app.get("/healthz")
def healthz():
    return "ok", 200

# 아래 엔드포인트들을 구현하세요. ( 함수명은 임의로 지정한 내용임 )
@app.get("/api/records")
def get_records():
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        return jsonify(data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.post("/api/records")
def add_record():
    try:
        # 요청 데이터 가져오기
        record = request.get_json()
        
        # 유효성 검사
        if not record:
            return jsonify({"error": "No data provided"}), 400
        
        if "title" not in record or "amount" not in record or "date" not in record:
            return jsonify({"error": "Missing required fields: title, amount, date"}), 400
        
        if not isinstance(record["amount"], (int, float)):
            return jsonify({"error": "Amount must be a number"}), 400
        
        # 기존 데이터 읽기
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        # 새 레코드 추가
        data.append({
            "title": record["title"],
            "amount": record["amount"],
            "date": record["date"]
        })
        
        # 파일에 저장
        with open(DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        return jsonify({"message": "Record added successfully", "record": record}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.get("/api/summary")
def summary():
    try:
        with open(DATA_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        count = len(data)
        total = sum(record["amount"] for record in data)
        
        return jsonify({"count": count, "total": total}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.get("/api/download")
def download_json():
    try:
        return send_file(
            DATA_PATH,
            mimetype="application/json",
            as_attachment=True,
            download_name="expenses.json"
        )
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # 적절한 포트(예: 5000)로 0.0.0.0 에서 실행
    app.run(host="0.0.0.0", port=5000)