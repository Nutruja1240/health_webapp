from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        age = int(request.form['age'])
        gender = request.form['gender']
        height = float(request.form['height'])
        weight = float(request.form['weight'])
        waist = float(request.form['waist'])
        sugar = float(request.form['sugar'])
        bp_sys = int(request.form['bp_sys'])
        bp_dia = int(request.form['bp_dia'])

        sit_and_reach = float(request.form['sit_and_reach'])
        step_test = int(request.form['step_test'])
        chair_stand = int(request.form['chair_stand'])
        grip_strength = float(request.form['grip_strength'])
        sit_ups = int(request.form['sit_ups'])

        # BMI
        bmi = round(weight / ((height / 100) ** 2), 2)
        if bmi < 18.5:
            bmi_status = 'ผอม'
            bmi_advice = 'ควรรับประทานอาหารให้เพียงพอและออกกำลังกายเสริมสร้างกล้ามเนื้อ'
        elif 18.5 <= bmi < 23:
            bmi_status = 'ปกติ'
            bmi_advice = 'ควรรักษาน้ำหนักและออกกำลังกายสม่ำเสมอ'
        elif 23 <= bmi < 25:
            bmi_status = 'น้ำหนักเกิน'
            bmi_advice = 'ควรควบคุมอาหารและเพิ่มการออกกำลังกาย'
        elif 25 <= bmi < 30:
            bmi_status = 'อ้วนระดับ 1'
            bmi_advice = 'เริ่มควบคุมอาหารและออกกำลังกายเพื่อลดน้ำหนัก'
        else:
            bmi_status = 'อ้วนระดับ 2'
            bmi_advice = 'ควรปรึกษาแพทย์และควบคุมน้ำหนักอย่างจริงจัง'

        # น้ำตาล
        if sugar < 70:
            sugar_status = 'น้ำตาลต่ำ'
            sugar_advice = 'ควรรับประทานอาหารว่างที่มีคาร์โบไฮเดรตเชิงซ้อน'
        elif 70 <= sugar <= 99:
            sugar_status = 'ปกติ'
            sugar_advice = 'ควรรักษาระดับน้ำตาลและออกกำลังกายสม่ำเสมอ'
        else:
            sugar_status = 'น้ำตาลสูง'
            sugar_advice = 'ควรปรึกษาแพทย์และปรับพฤติกรรมการกิน'

        # ความดัน
        if bp_sys < 120 and bp_dia < 80:
            bp_status = 'ความดันปกติ'
            bp_advice = 'ควรรักษาพฤติกรรมสุขภาพที่ดี'
        elif 120 <= bp_sys <= 139 or 80 <= bp_dia <= 89:
            bp_status = 'ความดันเริ่มสูง'
            bp_advice = 'ควรลดเค็มและออกกำลังกายสม่ำเสมอ'
        else:
            bp_status = 'ความดันสูง'
            bp_advice = 'ควรพบแพทย์เพื่อตรวจรักษาและควบคุมอาหาร'

        # รอบเอว
        if (gender == 'ชาย' and waist < 90) or (gender == 'หญิง' and waist < 80):
            waist_status = 'รอบเอวปกติ'
            waist_advice = 'ควรรักษาพฤติกรรมการกินและการออกกำลังกาย'
        else:
            waist_status = 'รอบเอวเกินเกณฑ์'
            waist_advice = 'ควรลดไขมันหน้าท้องด้วยการควบคุมอาหารและออกกำลังกาย'

        # สมรรถภาพทางกาย
        fitness_results = {}

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

        fitness_results['sit_and_reach'] = {
            'value': sit_and_reach,
            'level': interpret_sit_and_reach(age, gender, sit_and_reach)[0],
            'description': interpret_sit_and_reach(age, gender, sit_and_reach)[1],
            'recommendation': 'ฝึกยืดกล้ามเนื้อหลังและขาเป็นประจำ'
        }

        fitness_results['step_test'] = {
            'value': step_test,
            'level': interpret_step_test(age, gender, step_test)[0],
            'description': interpret_step_test(age, gender, step_test)[1],
            'recommendation': 'ออกกำลังกายแบบแอโรบิกต่อเนื่อง'
        }

        fitness_results['chair_stand'] = {
            'value': chair_stand,
            'level': interpret_chair_stand(age, gender, chair_stand)[0],
            'description': interpret_chair_stand(age, gender, chair_stand)[1],
            'recommendation': 'ฝึกนั่ง-ลุกจากเก้าอี้วันละหลายรอบ'
        }

        fitness_results['grip_strength'] = {
            'value': grip_strength,
            'level': interpret_grip_strength(age, gender, grip_strength)[0],
            'description': interpret_grip_strength(age, gender, grip_strength)[1],
            'recommendation': 'ฝึกบีบลูกบอลยาง หรือบีบมือบ่อย ๆ'
        }

        fitness_results['sit_ups'] = {
            'value': sit_ups,
            'level': interpret_sit_ups(age, gender, sit_ups)[0],
            'description': interpret_sit_ups(age, gender, sit_ups)[1],
            'recommendation': 'ฝึกซิตอัพหรือท่าแพลงก์เสริมกล้ามเนื้อหน้าท้อง'
        }

        # แปลงชื่อภาษาไทยสำหรับแสดงผล
        thai_labels = {
            'sit_and_reach': 'การนั่งงอตัวไปข้างหน้า',
            'step_test': 'การยกเข่าขึ้น-ลง 3 นาที',
            'chair_stand': 'การยืน-นั่งบนเก้าอี้ 60 วินาที',
            'grip_strength': 'แรงบีบมือ',
            'sit_ups': 'การซิตอัพ'
        }

        fitness_display = []
        for key, data in fitness_results.items():
            fitness_display.append({
                'name': thai_labels.get(key, key),
                'value': data['value'],
                'level': data['level'],
                'description': data['description'],
                'recommendation': data['recommendation']
            })

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
            'fitness': fitness_display
        }

    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(debug=True)
