from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST','HEAD'])
def health_check():
    result = None
    if request.method == 'POST':
        try:
            weight = float(request.form['weight'])
            height = float(request.form['height']) / 100
            waist = float(request.form['waist'])
            sugar = float(request.form['sugar'])
            systolic = int(request.form['systolic'])
            diastolic = int(request.form['diastolic'])
            gender = request.form['gender']
            age = int(request.form['age'])

            # ดัชนีมวลกาย
            bmi = round(weight / (height ** 2), 2)
            bmi_status, bmi_advice = interpret_bmi(bmi)

            # น้ำตาล, ความดัน, รอบเอว
            sugar_status, sugar_advice = interpret_sugar(sugar)
            bp_status, bp_advice = interpret_bp(systolic, diastolic)
            waist_status, waist_advice = interpret_waist(waist, gender)

            # สมรรถภาพทางกาย
            sit_and_reach = float(request.form['sit_and_reach'])
            step_test = int(request.form['step_test'])
            chair_stand = int(request.form['chair_stand'])
            grip_strength = float(request.form['grip_strength'])
            sit_ups = int(request.form['sit_ups'])

            fitness_results = {
                'sit_and_reach': interpret_sit_and_reach(age, gender, sit_and_reach),
                'step_test': interpret_step_test(age, gender, step_test),
                'chair_stand': interpret_chair_stand(age, gender, chair_stand),
                'grip_strength': interpret_grip_strength(age, gender, grip_strength),
                'sit_ups': interpret_sit_ups(age, gender, sit_ups)
            }

            result = {
                'bmi': bmi,
                'bmi_status': bmi_status,
                'bmi_advice': bmi_advice,
                'sugar_status': sugar_status,
                'sugar_advice': sugar_advice,
                'bp_status': bp_status,
                'bp_advice': bp_advice,
                'waist_status': waist_status,
                'waist_advice': waist_advice,
                'fitness_results': fitness_results
            }

        except Exception as e:
            result = {'error': 'กรุณากรอกข้อมูลให้ครบถ้วน'}

    return render_template('index.html', result=result)

# ฟังก์ชันแปลผลสุขภาพทั่วไป
def interpret_bmi(bmi):
    if bmi < 18.5:
        return 'ผอม', 'ควรเพิ่มน้ำหนักด้วยอาหารที่มีพลังงานสูง เช่น ข้าวกล้อง ถั่ว เนื้อสัตว์ และรับประทานอาหารให้ครบ 3 มื้อ พร้อมออกกำลังกายเบา ๆ อย่างสม่ำเสมอ'
    elif bmi < 23:
        return 'ปกติ', 'รักษารูปร่างโดยรับประทานอาหารให้ครบ 5 หมู่ ลดหวาน มัน เค็ม และออกกำลังกายอย่างน้อย 150 นาที/สัปดาห์'
    elif bmi < 25:
        return 'น้ำหนักเกิน', 'ลดปริมาณอาหารจำพวกแป้งและไขมัน เพิ่มผักและผลไม้ ออกกำลังกายแบบแอโรบิก เช่น เดินเร็ว วิ่งเบา ๆ อย่างน้อย 30 นาที/วัน'
    elif bmi < 30:
        return 'อ้วนระดับ 1', 'ควรลดน้ำหนักโดยควบคุมอาหาร (เช่น ลดข้าวขาว อาหารทอด ของหวาน) และออกกำลังกายเพิ่ม เช่น ปั่นจักรยาน ว่ายน้ำ'
    else:
        return 'อ้วนระดับ 2', 'เสี่ยงโรคเรื้อรัง ควรปรึกษาแพทย์ นักโภชนาการ และควบคุมอาหารอย่างเข้มงวด พร้อมออกกำลังกายสม่ำเสมอ เช่น เดินเร็ว/โยคะ อย่างน้อย 5 วัน/สัปดาห์'

def interpret_sugar(sugar):
    if sugar < 70:
        return 'น้ำตาลต่ำ', 'ควรปรึกษาแพทย์เพื่อประเมินสาเหตุ และวางแผนการดูแล'
    elif sugar < 100:
        return 'ปกติ', 'รักษาระดับน้ำตาลให้คงที่ โดยรับประทานอาหารที่เหมาะสมและออกกำลังกายสม่ำเสมอ'
    elif sugar < 126:
        return 'ระดับน้ำตาลสูง', 'ควรควบคุมอาหาร หลีกเลี่ยงของหวานและแป้งขัดขาว พร้อมออกกำลังกาย'
    else:
        return 'เสี่ยงเบาหวาน', 'ควรพบแพทย์เพื่อตรวจวินิจฉัยเพิ่มเติม และรับคำแนะนำเรื่องอาหารและการดูแลสุขภาพ'

def interpret_bp(sys, dia):
    if sys < 120 and dia < 80:
        return 'ความดันปกติ', 'รักษาด้วยการลดเค็ม ออกกำลังกาย และควบคุมน้ำหนัก'
    elif 120 <= sys <= 139 or 80 <= dia <= 89:
        return 'ความดันเริ่มสูง', 'ควรลดเค็ม ออกกำลังกาย และติดตามความดันอย่างสม่ำเสมอ'
    else:
        return 'ความดันสูง', 'ควรพบแพทย์ และควบคุมอาหาร/น้ำหนัก'

def interpret_waist(waist, gender):
    if (gender == 'male' and waist > 90) or (gender == 'female' and waist > 80):
        return 'รอบเอวเกินเกณฑ์', 'คุณมีรอบเอวสูง อาจเสี่ยงต่อโรคหัวใจ ความดัน เบาหวาน ควรลดน้ำตาล ออกกำลังกายสม่ำเสมอ และควบคุมน้ำหนัก'
    else:
        return 'รอบเอวปกติ', 'ดีมาก ควรรักษาไว้ด้วยการควบคุมอาหารและออกกำลังกาย'

# ฟังก์ชันแปลผลสมรรถภาพทางกาย (ตัวอย่างแบบสั้น ใช้ได้กับช่วงอายุทั่วไป)
def interpret_sit_and_reach(age, gender, value):
    if value >= 20:
        return ('ดี', 'กล้ามเนื้อหลังและขาอยู่ในเกณฑ์ดี ช่วยลดอาการปวดหลัง')
    elif value >= 10:
        return ('ปานกลาง', 'ควรยืดเหยียดกล้ามเนื้อหลังและขาสม่ำเสมอ')
    else:
        return ('ต่ำ', 'ความยืดหยุ่นต่ำ เสี่ยงบาดเจ็บ ควรฝึกโยคะหรือยืดเหยียดทุกวัน')

def interpret_step_test(age, gender, value):
    if value >= 90:
        return ('ดี', 'สมรรถภาพหัวใจและปอดดีเยี่ยม ควรรักษาไว้')
    elif value >= 60:
        return ('ปานกลาง', 'ควรออกกำลังกายแบบแอโรบิกเพิ่ม เช่น เดินเร็ว ปั่นจักรยาน')
    else:
        return ('ต่ำ', 'สมรรถภาพหัวใจไม่ดี เสี่ยงเหนื่อยง่าย ควรเริ่มออกกำลังกายเบา ๆ')

def interpret_chair_stand(age, gender, value):
    if value >= 25:
        return ('ดี', 'กล้ามเนื้อขาแข็งแรง ลดความเสี่ยงหกล้ม')
    elif value >= 15:
        return ('ปานกลาง', 'ควรฝึกนั่ง-ลุกจากเก้าอี้ หรือออกกำลังกายขา')
    else:
        return ('ต่ำ', 'กล้ามเนื้อขาอ่อนแรง ควรเสริมสร้างโดยฝึกยืน-นั่งบ่อย ๆ')

def interpret_grip_strength(age, gender, value):
    if value >= 0.5:
        return ('ดี', 'กล้ามเนื้อมือและแขนแข็งแรง ช่วยในการทำกิจกรรมประจำวัน')
    elif value >= 0.3:
        return ('ปานกลาง', 'ควรฝึกกำมือ บีบลูกบอลยาง หรือยกดัมเบลเบา ๆ')
    else:
        return ('ต่ำ', 'แรงบีบมือต่ำ เสี่ยงกล้ามเนื้ออ่อนแรง ควรฝึกใช้งานมือบ่อย ๆ')

def interpret_sit_ups(age, gender, value):
    if value >= 30:
        return ('ดี', 'กล้ามเนื้อหน้าท้องแข็งแรง ลดอาการปวดหลัง')
    elif value >= 15:
        return ('ปานกลาง', 'ควรฝึกซิตอัพหรือท่าแพลงก์เสริมกล้ามเนื้อหน้าท้อง')
    else:
        return ('ต่ำ', 'กล้ามเนื้อหน้าท้องอ่อนแรง ควรฝึกสม่ำเสมอเพื่อลดอาการปวดหลัง')

if __name__ == '__main__':
    app.run(debug=False)
