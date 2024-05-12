import streamlit as st
from gtts import gTTS
import speech_recognition as sr
import time
import io

def get_audio(prompt):
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.write(prompt, unsafe_allow_html=True)
        progress_bar = st.progress(0)
        for i in range(100):  # 90초 동안 진행 상황을 업데이트
            time.sleep(0.9)  # 90초를 100개의 단계로 나누어 각 0.9초마다 업데이트
            progress_bar.progress(i + 1)
        audio = r.listen(source, timeout=5, phrase_time_limit=90)
        progress_bar.empty()  # 타임바를 제거
        
        try:
            said = r.recognize_google(audio, language='ko-KR')
            st.write("지원자의 답변: " + said)
            return said
        except sr.UnknownValueError:
            st.error("인식할 수 없는 음성입니다.")
            return ""
        except sr.RequestError:
            st.error("서비스 요청에 실패했습니다; 구글 API에 연결할 수 없습니다.")
            return ""
        except Exception as e:
            st.error("Exception: " + str(e))
            return ""

def main():
    st.title('🎤 실제 면접 현장이라고 생각하고 답변해보세요!')
    st.markdown("#### 면접자의 답변을 저장하고 관리해줍니다.")
    st.markdown("---")

    if 'memo_text' not in st.session_state:
        st.session_state.memo_text = ""

    col1, col2, col3 = st.columns([1, 1, 1])
    with col1:
        if st.button('답변 시작', help='음성 답변을 시작합니다.'):
            text = get_audio("🎤 듣고 있습니다. 90초 동안 말씀해주세요.")
            if text:
                st.session_state.memo_text += text + "\n"
    
    with col2:
        if st.button('추가 답변', help='추가 음성 입력을 진행합니다.'):
            text = get_audio("🎤 추가로 하실 말씀이 있다면 말씀해주세요.")
            if text:
                st.session_state.memo_text += text + "\n"
    
    with col3:
        if st.button('종료', help='모든 입력을 종료하고 메모를 저장합니다.'):
            if st.session_state.memo_text:
                with open('memo.txt', 'w', encoding='utf-8') as f:
                    f.write(st.session_state.memo_text)
                st.success("📝 메모가 저장되었습니다!")
                st.session_state.memo_text = ""  # 메모 내용 초기화
            st.session_state.continue_recording = False  # 녹음 상태 비활성화
    
    if st.session_state.memo_text:
        st.markdown("### 📄 현재 메모 내용")
        st.text_area("메모 미리보기:", value=st.session_state.memo_text, height=150, disabled=True)

if __name__ == '__main__':
    main()
