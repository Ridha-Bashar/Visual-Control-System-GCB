import cv2
import serial
import time
import mediapipe as mp

# ----------------- إعداد الاتصال التسلسلي -----------------
try:
    # **تأكد من تغيير 'COM3' إلى المنفذ الصحيح للأردوينو (مثلاً COM4 أو /dev/ttyACM0)**
    arduino = serial.Serial('COM7', 9600, timeout=1) 
    time.sleep(2) 
    print("Serial Connection: SUCCESS")
except serial.SerialException as e:
    print(f"Serial Connection: FAILED. Error: {e}")
    # إذا فشل الاتصال، يمكن الاستمرار في عرض الكاميرا فقط
    arduino = None 

# ----------------- تعريف وظيفة الإرسال -----------------
def send_command(command_char):
    if arduino:
        try:
            arduino.write(command_char.encode())
            print(f"Command Sent: {command_char}")
            # قراءة الرد من الأردوينو
            if arduino.in_waiting > 0:
                response = arduino.readline().decode().strip()
                print(f"Arduino Response: {response}")
        except Exception as e:
            print(f"Error sending data: {e}")

# ----------------- إعداد الرؤية الحاسوبية -----------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils
cap = cv2.VideoCapture(0) 

# دالة للتحقق من أن اليد مغلقة
# المنطق: المسافة بين طرف الإبهام وطرف السبابة (نقاط 4 و 8)
# إذا كانت المسافة أصغر من عتبة معينة، تعتبر اليد مغلقة.
def is_hand_closed(landmarks):
    # نقاط الأطراف: الإبهام (4)، السبابة (8)، الوسطى (12)
    thumb_tip = landmarks[4]
    index_tip = landmarks[8]
    
    # حساب المسافة الأفقية بين الإبهام والسبابة
    distance_x = abs(thumb_tip.x - index_tip.x) 
    
    # يمكن تعديل هذه القيمة حسب الكاميرا وحجم اليد
    CLOSING_THRESHOLD = 0.08 
    
    # إذا كانت المسافة صغيرة، اليد مغلقة
    if distance_x < CLOSING_THRESHOLD:
        return True
    return False

# متغيرات تحكم
current_state = 'CLOSED' # الحالة الافتراضية لليد
last_sent_command = 'F'  # آخر أمر أُرسل للأردوينو

while cap.isOpened():
    success, image = cap.read()
    if not success:
        continue

    # تحويل الصورة إلى RGB وتطبيق الكشف
    image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = hands.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            
            # 1. تحليل الإيماءة
            if is_hand_closed(hand_landmarks.landmark):
                new_state = 'CLOSED'
                cv2.putText(image, "HAND CLOSED: LED OFF", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
                
            else:
                new_state = 'OPEN'
                cv2.putText(image, "HAND OPEN: LED ON", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            
            # 2. إرسال الأمر فقط عند تغيير الحالة
            if new_state != current_state:
                if new_state == 'OPEN' and last_sent_command != 'T':
                    send_command('T')
                    last_sent_command = 'T'
                elif new_state == 'CLOSED' and last_sent_command != 'F':
                    send_command('F')
                    last_sent_command = 'F'
                current_state = new_state
                
            
            mp_draw.draw_landmarks(image, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    cv2.imshow('AI Hand Control (Press Q to exit)', image)
    
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

# التنظيف وإغلاق كل شيء
cap.release()
cv2.destroyAllWindows()
if arduino:
    arduino.close()
    print("Connection Closed.")