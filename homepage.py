import streamlit as st
import pandas as pd
import requests
import base64
from datetime import datetime
from PIL import Image


def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()


def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)


def main():
    # 세션 상태 변수를 초기화합니다.
    if 'page' not in st.session_state:
        st.session_state['page'] = 'login_page'

    # 현재 페이지를 보여줍니다.
    if st.session_state['page'] == 'login_page':
        login_page()
    elif st.session_state['page'] == 'main_page':
        main_page()
    elif st.session_state['page'] == 'sign_up_page':
        sign_up_page()
    elif st.session_state['page'] == 'modify_page':
        modify_page()
    elif st.session_state['page'] == 'new_page':
        new_page()

# 로그인 페이지


def login_page():
    set_background('C:/streamlit/streamlit_projects/images/dark1.jpg')
    st.title("")
    st.title("Team PROJECT - 2023 :sunglasses:")
    st.caption("Streamlit WebPage - Welcome !!! :smile:")
    st.title("")
    st.title("")
    st.title("")
    st.subheader("Sign In")

    # 사용자 입력 필드
    userId = st.text_input("아이디", key='email', max_chars=32)
    userPassword = st.text_input(
        "비밀번호", type='password', key='password', max_chars=16)

    # 2개의 컬럼 생성
    col1, col2 = st.columns(2)

    # 로그인 버튼 클릭 시 동작
    if col1.button(":green[로그인]"):
        if len(userId) == 0 or len(userPassword) == 0:
            st.error("아이디 또는 비밀번호를 입력하세요.", icon="⚠️")
        else:
            data = {"user_id": userId, "user_password": userPassword}
            response = requests.post("http://localhost:5000/login", json=data)
            result = response.json()

            if result["status"] == "success":
                st.session_state["user_key"] = result["user_key"]
                st.session_state["user_id"] = result["user_id"]
                st.session_state["user_password"] = result["user_password"]
                st.session_state["user_name"] = result["user_name"]
                st.session_state["user_birth"] = result["user_birth"]
                st.session_state["user_tel"] = result["user_tel"]
                st.session_state["user_use_yn"] = result["user_use_yn"]
                st.session_state["user_reg_dt"] = result["user_reg_dt"]
                st.session_state["user_mod_dt"] = result["user_mod_dt"]
                st.session_state['page'] = 'main_page'
                st.experimental_rerun()
            else:
                st.error(result["message"], icon="⚠️")
    elif col2.button(":blue[회원가입]"):
        st.session_state['page'] = 'sign_up_page'
        st.experimental_rerun()

# 회원가입 페이지


def sign_up_page():
    set_background('C:/streamlit/streamlit_projects/images/neon.jpg')
    st.header("")
    st.title("Team PROJECT - 2023 :sunglasses:")
    st.caption("Welcome !!! :smile:")
    st.header("")
    st.header("")
    st.subheader("Sign Up")

    # 사용자 입력 필드
    col1, col2 = st.columns(2)
    input_id = col1.text_input("아이디", max_chars=32)
    duplicateChk = st.button(":blue[중복 확인]")
    if duplicateChk:
        if len(input_id) == 0:
            col2.error("아이디를 입력하세요.", icon="⚠️")
        else:
            data = {"user_id": input_id}
            response = requests.post(
                "http://localhost:5000/duplicateCheck", json=data)
            result = response.json()
            if result["status"] == "success":
                col2.success(result["message"], icon="✅")
            else:
                col2.error(result["message"], icon="⚠️")

    col1, col2 = st.columns(2)
    with col1:
        input_pw = st.text_input(
            "비밀번호", type='password', key='password', max_chars=16)
    with col2:
        input_pw2 = st.text_input(
            "비밀번호 확인", type='password', key='passwordConfirm', max_chars=16)

    col1, col2 = st.columns(2)
    with col2:
        passwdChk = st.button(":blue[비밀번호 확인]")

    if passwdChk:
        if len(input_pw) > 0 and input_pw == input_pw2:
            with col1:
                st.success("비밀번호를 일치합니다.", icon="✅")
        elif len(input_pw) == 0:
            with col1:
                st.error("비밀번호를 입력하세요.", icon="⚠️")
        else:
            with col1:
                st.error("비밀번호가 일치하지 않습니다.", icon="⚠️")

    col1, col2 = st.columns(2)
    with col1:
        input_name = st.text_input("이름")
    with col2:
        input_birth = st.date_input("생년월일")

    col1, col2, col3 = st.columns(3)
    input_tel = col1.text_input(
        "연락처 ('-' 제외하고 입력하세요.)", value="010", max_chars=3, key="tel1")
    input_tel += col2.text_input("", max_chars=4, key="tel2")
    input_tel += col3.text_input("", max_chars=4, key="tel3")

    col1, col2 = st.columns(2)  # 새로운 컬럼 생성
    if col1.button(":green[회원가입]"):  # 첫번째 컬럼에 버튼 배치
        data = {"user_id": input_id,
                "user_password": input_pw2,
                "user_name": input_name,
                "user_birth": input_birth.isoformat(),
                "user_tel": input_tel,
                "user_use_yn": "Y"}

        response = requests.post("http://localhost:5000/insert", json=data)
        result = response.json()

        if result["status"] == "success":
            st.session_state['page'] = 'login_page'  # 페이지 전환을 여기서 설정
            st.experimental_rerun()
        elif result["status"] == "error":
            st.error(result["message"])

    elif col2.button(":red[돌아가기]"):  # 두번째 컬럼에 버튼 배치
        st.session_state['page'] = 'login_page'  # 페이지 전환을 여기서 설정
        st.experimental_rerun()

# 메인 페이지


def main_page():
    set_background('C:/streamlit/streamlit_projects/images/min.jpg')
    st.header("")
    st.title("Team PROJECT - 2023 :sunglasses:")
    st.caption("Welcome !!! :smile:")

    col1, col2 = st.columns(2)
    # with col1:
    # st.markdown(
    # ':green[' + st.session_state["user_name"] + ']님 환영합니다. 🙋‍♂️')
    with col1:
        if st.session_state.page == "main_page":
            st.markdown(
                f'<div style="color: white;">환영합니다, {st.session_state.user_name}님! 🙋‍♂️</div>', unsafe_allow_html=True)
            st.write("이 페이지에서 회원 목록과 정보를 확인할 수 있습니다.")
    with col2:
        # 페이지 전환 버튼
        if st.button(":red[로그아웃]"):
            st.session_state["user_key"] = ""
            st.session_state["user_id"] = ""
            st.session_state["user_password"] = ""
            st.session_state["user_name"] = ""
            st.session_state["user_birth"] = ""
            st.session_state["user_tel"] = ""
            st.session_state["user_use_yn"] = ""
            st.session_state["user_reg_dt"] = ""
            st.session_state["user_mod_dt"] = ""
            st.session_state['page'] = 'login_page'  # 페이지 전환을 여기서 설정
            st.experimental_rerun()
        if st.button(":green[렌즈불합판정페이지]"):
            st.session_state['page'] = 'new_page'
            st.experimental_rerun()

    st.header("")
    st.header("")
    st.header("회원 목록")
    st.caption("가입된 회원 목록 입니다.")
    response = requests.post("http://localhost:5000/userList")
    result = response.json()
    df = pd.DataFrame(result)

    col1, col2, col3, col4, col5 = st.columns(5)
    col1.markdown("회원 번호")
    col2.markdown("아이디")
    col3.markdown("이름")
    col4.markdown("생년월일")
    col5.markdown("수정")

    col1, col2, col3, col4, col5 = st.columns(5)
    for j in range(len(df)):
        with col1:
            st.markdown(
                f'<div style="color: white;">{df.at[j, "회원 번호"]}</div>', unsafe_allow_html=True)
        with col2:
            st.markdown(
                f'<div style="color: white;">{df.at[j, "아이디"]}</div>', unsafe_allow_html=True)
        with col3:
            st.markdown(
                f'<div style="color: white;">{df.at[j, "이름"]}</div>', unsafe_allow_html=True)
        with col4:
            st.markdown(
                f'<div style="color: white;">{df.at[j, "생년월일"]}</div>', unsafe_allow_html=True)
        with col5:
            if st.button(':blue[수정]', key=df.at[j, '회원 번호']):
                st.session_state["modify_user_key"] = df.at[j, '회원 번호']
                st.session_state["modify_user_id"] = df.at[j, '아이디']
                st.session_state["modify_user_password"] = df.at[j, '비밀번호']
                st.session_state["modify_user_name"] = df.at[j, '이름']
                st.session_state["modify_user_birth"] = df.at[j, '생년월일']
                st.session_state["modify_user_tel"] = df.at[j, '연락처']
                st.session_state["modify_user_use_yn"] = df.at[j, '유효상태']
                st.session_state["modify_user_reg_dt"] = df.at[j, '등록일']
                st.session_state["modify_user_mod_dt"] = df.at[j, '수정일']
                st.session_state['page'] = 'modify_page'
                st.experimental_rerun()

# 회원정보 수정 페이지


def modify_page():
    set_background('C:/streamlit/streamlit_projects/images/king.jpg')
    st.header("")
    st.title("Team PROJECT - 2023 :sunglasses:")
    st.caption("Streamlit WebPage - Welcome !!! :smile:")
    st.header("")
    st.header("")
    st.subheader("Member Info.")

    # 사용자 입력 필드
    col1, col2 = st.columns(2)
    with col1:
        st.write(f"{st.session_state.user_name}님의 정보 수정 페이지입니다.")
    with col2:
        if st.button(":red[뒤로 가기]"):
            st.session_state['page'] = 'main_page'
            st.experimental_rerun()
    # 중복 확인 부분에서 duplicateChk 변수 추가
    col1, col2 = st.columns(2)
    with col1:
        input_id = st.text_input(
            "아이디", value=st.session_state.get("modify_user_id", ""))
    with col2:
        st.header("")
        duplicateChk = st.button(":blue[중복 확인]")
    if duplicateChk:
        if len(input_id) == 0:
            st.error("아이디를 입력하세요.", icon="⚠️")
        else:
            data = {"user_id": input_id}
            response = requests.post(
                "http://localhost:5000/duplicateCheck", json=data)
            result = response.json()
            if result["status"] == "success":
                st.success(result["message"], icon="✅")
            else:
                st.error(result["message"], icon="⚠️")

    col1, col2 = st.columns(2)
    with col1:
        input_pw = st.text_input(
            "새 비밀번호", type='password', key='password', max_chars=16)
    with col2:
        input_pw2 = st.text_input(
            "새 비밀번호 확인", type='password', key='passwordConfirm', max_chars=16)
    # 비밀번호 확인 부분에서 변경
    col1, col2 = st.columns(2)
    passwdChk = col2.button(":blue[비밀번호 확인]")
    if passwdChk:
        if len(input_pw) > 0 and input_pw == input_pw2:
            col1.success("비밀번호를 일치합니다.", icon="✅")
        elif len(input_pw) == 0:
            col1.error("비밀번호를 입력하세요.", icon="⚠️")
        else:
            col1.error("비밀번호가 일치하지 않습니다.", icon="⚠️")
    # 생년월일을 나타내는 변수
    modify_user_birth = st.session_state.get("modify_user_birth", "")
    col1, col2 = st.columns(2)
    with col1:
        input_name = st.text_input(
            "이름", value=st.session_state.get("modify_user_name", ""))
    with col2:
        if modify_user_birth:  # 빈 문자열이 아닐 때에만 변환 시도
            input_birth = st.date_input("생년월일", value=datetime.strptime(
                modify_user_birth, "%Y-%m-%d").date())
        else:
            input_birth = st.date_input("생년월일")

    col1, col2, col3 = st.columns(3)
    tel_number = st.session_state.get("modify_user_tel", "")
    tel_number1 = f"{tel_number[:3]}"
    tel_number2 = f"{tel_number[3:7]}"
    tel_number3 = f"{tel_number[7:]}"
    input_tel = col1.text_input(
        "연락처 ('-' 제외하고 입력하세요.)", value=tel_number1, max_chars=3, key="tel1")
    input_tel += col2.text_input("", max_chars=4,
                                 value=tel_number2, key="tel2")
    input_tel += col3.text_input("", max_chars=4,
                                 value=tel_number3, key="tel3")

    col1, col2, col3 = st.columns(3)  # 새로운 컬럼 생성
    if col1.button(":green[수정]"):  # 첫번째 컬럼에 버튼 배치
        if len(input_pw) > 0 and input_pw == input_pw2:
            data = {"user_key": str(st.session_state["modify_user_key"]),
                    "user_id": input_id,
                    "user_password": input_pw2,
                    "user_name": input_name,
                    "user_birth": input_birth.isoformat(),
                    "user_tel": input_tel,
                    "user_use_yn": "Y"}

            response = requests.post("http://localhost:5000/update", json=data)
            result = response.json()

            if result["status"] == "success":
                st.session_state['page'] = 'main_page'  # 페이지 전환을 여기서 설정
                st.experimental_rerun()
            elif result["status"] == "error":
                st.error(result["message"])
        else:
            st.error("새 비밀번호를 입력해 주세요.")
    elif col2.button(":red[회원 삭제]"):
        data = {"user_key": str(st.session_state["modify_user_key"])}

        response = requests.post("http://localhost:5000/delete", json=data)
        result = response.json()

        if result["status"] == "success":
            st.session_state['page'] = 'main_page'  # 페이지 전환을 여기서 설정
            st.experimental_rerun()
        elif result["status"] == "error":
            st.error(result["message"])

    elif col3.button(":blue[돌아가기]"):  # 두번째 컬럼에 버튼 배치
        st.session_state['page'] = 'main_page'  # 페이지 전환을 여기서 설정
        st.experimental_rerun()



# 렌즈 불합판정 페이지
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.applications.resnet50 import preprocess_input
from PIL import Image as PILImage
import numpy as np
def load_custom_model(model_path):
    model = load_model(model_path)
    return model

# 이미지 분석
def analyze_image_custom_model(model, image):
    image = preprocess_input(np.array(image.resize((224, 224))))
    image = np.expand_dims(image, axis=0)
    predictions = model.predict(image)
    decoded_predictions = tf.keras.applications.resnet50.decode_predictions(predictions)[0]
    top_prediction = decoded_predictions[0]
    return top_prediction[1], top_prediction[2]

def resize_image(image, size):
    img = Image.open(image)
    img_resized = img.resize(size)
    return img

def clear_session_state():
    st.session_state.clear()

def new_page():
    # 원하는 배경 이미지로 설정
    set_background('C:/streamlit/streamlit_projects/images/robot.jpg')
    st.title("렌즈 이미지 판단 페이지")
    st.write("이미지를 업로드하고 분석하세요!")

    uploaded_image = st.file_uploader(
        "렌즈 이미지 업로드", type=["jpg", "jpeg", "png"])

    if uploaded_image is not None:
        image = resize_image(uploaded_image, (300, 300))
        st.image(image, caption="업로드한 이미지", use_column_width=True)

        analyze_button = st.button("이미지 분석")
        if analyze_button:
            st.spinner("이미지 분석 중...")
            custom_model = load_custom_model('C:/streamlit/streamlit_projects/team_project.h5')
            result_label, result_confidence = analyze_image_custom_model(custom_model, uploaded_image)

            st.success(f"예측: {result_label}, 신뢰도: {result_confidence:.2f}")

            # 이미지를 바이트 데이터로 변환하여 서버로 전송
            image_data = uploaded_image.read()
            encoded_image = base64.b64encode(image_data).decode()

            data = {"image": encoded_image}
            response = requests.post(
                "http://localhost:5000/analyze_image", json=data)
            result = response.json()

            if result["status"] == "success":
                st.success(result["message"])
            else:
                st.error(result["message"])
    # 메인 페이지로 이동 버튼
    if st.button(":arrow_right: 메인 페이지로 이동"):
        st.session_state.page = "main_page"
        st.experimental_rerun()

    # 회원정보 수정 페이지로 이동 버튼
    if st.button(":pencil2: 회원정보 수정 페이지로 이동"):
        st.session_state.page = "modify_page"
        st.experimental_rerun()

    # 로그아웃 버튼
    if st.button(":door: 로그아웃"):
        clear_session_state()
        st.session_state.page = "login_page"
        st.experimental_rerun()


if __name__ == "__main__":
    main()