import streamlit as st

st.title('Python Streamlit 실습 :sunglasses:')
st.header('헤더입니다.')
st.subheader('서브헤더입니다.')
st.caption('캡션입니다.')

sample_code = '''
print('Hello world')
'''
st.code(sample_code, language="python")

st.text('텍스트입니다.')
st.markdown('마크다운입니다.')
st.markdown('**볼드처리는 별표 2개를 앞뒤로 붙여줍니다.**')
st.markdown('여기부터 글자에 색상이 들어갑니다. :red[빨간색] :orange[주황색] :green[초록색] :blue[파랑색] :violet[보라색]')

color = st.color_picker('색상을 골라주세요.', '#00f900')
st.write('The current color is', color)