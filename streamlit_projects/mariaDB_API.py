from flask import Flask, request, jsonify
import pandas as pd
import mysql.connector

app = Flask(__name__)

# MariaDB 연결 설정
db = mysql.connector.connect(
    host="127.0.0.1",
    port="10617",
    user="root",
    password="rkdwlsgh5080@",
    database="streamlit-test"
)


def login_user(user_id, user_password):
    cursor = db.cursor()
    sql = "SELECT COUNT(*), user_key, user_id, user_password, user_name, DATE_FORMAT(user_birth, '%Y-%m-%d') user_birth, user_tel, user_use_yn, user_reg_dt, user_mod_dt FROM user_info WHERE user_id=%s AND user_password=%s"
    val = (user_id, user_password)
    cursor.execute(sql, val)
    result = cursor.fetchone()
    return result


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user_id = data['user_id']
    user_password = data['user_password']

    # 로그인 함수 호출하여 결과 확인
    login_result, user_key, user_id, user_password, user_name, user_birth, user_tel, user_use_yn, user_reg_dt, user_mod_dt = login_user(
        user_id, user_password)

    if login_result:
        return jsonify({"status": "success",
                        "message": "로그인 성공",
                        "user_key": user_key,
                        "user_id": user_id,
                        "user_password": user_password,
                        "user_name": user_name,
                        "user_birth": user_birth,
                        "user_tel": user_tel,
                        "user_use_yn": user_use_yn,
                        "user_reg_dt": user_reg_dt,
                        "user_mod_dt": user_mod_dt})
    else:
        return jsonify({"status": "error", "message": "로그인 실패: 아이디 또는 비밀번호를 확인하세요"})


@app.route('/insert', methods=['POST'])
def insert_data():
    data = request.get_json()
    user_id = data['user_id']
    user_password = data['user_password']
    user_name = data['user_name']
    user_birth = data['user_birth']
    user_tel = data['user_tel']
    user_use_yn = data['user_use_yn']

    cursor = db.cursor()
    sql = "INSERT INTO user_info (user_id, user_password, user_name, user_birth, user_tel, user_use_yn, user_reg_dt, user_mod_dt) VALUES (%s, %s, %s, %s, %s, %s, NOW(), NOW())"
    val = (user_id, user_password, user_name,
           user_birth, user_tel, user_use_yn)

    try:
        cursor.execute(sql, val)
        db.commit()
        return jsonify({"status": "success", "message": "Data inserted successfully"})
    except Exception as e:
        db.rollback()
        return jsonify({"status": "error", "message": str(e)})


@app.route('/update', methods=['POST'])
def update_data():
    data = request.get_json()
    user_key = data['user_key']
    user_id = data['user_id']
    user_password = data['user_password']
    user_name = data['user_name']
    user_birth = data['user_birth']
    user_tel = data['user_tel']
    user_use_yn = data['user_use_yn']

    cursor = db.cursor()
    sql = "UPDATE user_info SET user_id=%s, user_password=%s, user_name=%s, user_birth=%s, user_tel=%s, user_use_yn=%s, user_mod_dt=NOW() WHERE user_key= '" + \
        user_key + "' "
    val = (user_id, user_password, user_name,
           user_birth, user_tel, user_use_yn)

    try:
        cursor.execute(sql, val)
        db.commit()
        return jsonify({"status": "success", "message": "Data updated successfully"})
    except Exception as e:
        db.rollback()
        return jsonify({"status": "error", "message": str(e)})


@app.route('/delete', methods=['POST'])
def delete_data():
    data = request.get_json()
    user_key = data['user_key']

    cursor = db.cursor()
    sql = "DELETE FROM user_info WHERE user_key=%s"
    val = (user_key,)

    try:
        cursor.execute(sql, val)
        db.commit()
        return jsonify({"status": "success", "message": "Data deleted successfully"})
    except Exception as e:
        db.rollback()
        return jsonify({"status": "error", "message": str(e)})


def user_list():
    cursor = db.cursor()
    sql = "SELECT user_key, user_id, user_password, user_name, DATE_FORMAT(user_birth, '%Y-%m-%d'), user_tel, user_use_yn, DATE_FORMAT(user_reg_dt, '%Y-%m-%d') user_reg_dt, DATE_FORMAT(user_mod_dt, '%Y-%m-%d') user_mod_dt FROM user_info"
    cursor.execute(sql)
    result = cursor.fetchall()

    # 사용자 목록을 DataFrame으로 변환하여 반환
    columns = ['회원 번호', '아이디', '비밀번호', '이름',
               '생년월일', '연락처', '유효상태', '등록일', '수정일']
    df = pd.DataFrame(result, columns=columns)
    return df


@app.route('/userList', methods=['POST'])
def userList():
    df = user_list()
    # DataFrame을 JSON으로 변환하여 반환
    return df.to_json(orient='records')


def duplicate_check(user_id):
    cursor = db.cursor()
    sql = "SELECT COUNT(*) FROM user_info WHERE user_id=%s"
    val = (user_id,)
    cursor.execute(sql, val)
    result = cursor.fetchone()[0]
    return result


@app.route('/duplicateCheck', methods=['POST'])
def duplicateCheck():
    data = request.get_json()
    user_id = data['user_id']

    # 중복 체크 함수 호출하여 결과 확인
    result = duplicate_check(user_id)

    if result > 0:
        return jsonify({"status": "error", "message": "중복되는 아이디입니다."})
    else:
        return jsonify({"status": "success", "message": "사용 가능한 아이디입니다."})


if __name__ == '__main__':
    app.run(debug=True)
