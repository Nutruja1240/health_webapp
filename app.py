from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        # รับข้อมูลจากฟอร์ม
        age = int(request.form['age'])
        gender = request.form['gender']
        height = float(request.form['height'])
        weight = float(request.form['weight'])
        waist = float(request.form['waist'])
        sugar = float(request.form['sugar'])
        bp_sys = int(request.form['bp_sys'])
        bp_dia = int(request.form['bp_dia'])

        # ทดสอบสมรรถภาพทางกาย
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

        # ฟิตเนส (สมรรถภาพทางกาย)
        fitness_results = {}

        def level(val, good, fair, poor):
            if val >= good:
                return 'ดีมาก'
            elif val >= fair:
                return 'ดี'
            elif val >= poor:
                return 'พอใช้'
            else:
                return 'ควรปรับปรุง'

        def interpret(name, value, level):
            desc = ''
            advice = ''
            if level == 'ดีมาก':
                desc = 'อยู่ในระดับดีมาก แสดงถึงสมรรถภาพที่ยอดเยี่ยม'
                advice = 'รักษาการออกกำลังกายแบบนี้ไว้ต่อเนื่อง'
            elif level == 'ดี':
                desc = 'อยู่ในระดับดี สมรรถภาพอยู่ในเกณฑ์เหมาะสม'
                advice = 'ควรออกกำลังกายต่อเนื่องเพื่อรักษาระดับนี้'
            elif level == 'พอใช้':
                desc = 'สมรรถภาพพอใช้ แต่ยังมีพัฒนาการได้อีก'
                advice = 'ควรเพิ่มกิจกรรมทางกาย เช่น เดินเร็วหรือว่ายน้ำ'
            else:
                desc = 'สมรรถภาพต่ำกว่ามาตรฐาน'
                advice = 'ควรปรึกษาผู้เชี่ยวชาญเพื่อวางแผนการออกกำลังกาย'

            return {
                'value': value,
                'level': level,
                'description': desc,
                'recommendation': advice
            }

        # เกณฑ์สมรรถภาพเบื้องต้น (ชายอายุ 20-29 ปี)
        fitness_results['sit_and_reach'] = interpret(
            'นั่งงอตัว', sit_and_reach,
            level(sit_and_reach, 35, 30, 25)
        )
        fitness_results['step_test'] = interpret(
            'Step Test', step_test,
            level(step_test, 130, 110, 90)
        )
        fitness_results['chair_stand'] = interpret(
            'Chair Stand', chair_stand,
            level(chair_stand, 30, 25, 20)
        )
        fitness_results['grip_strength'] = interpret(
            'แรงบีบมือ', grip_strength,
            level(grip_strength, 45, 35, 25)
        )
        fitness_results['sit_ups'] = interpret(
            'Sit-Ups', sit_ups,
            level(sit_ups, 40, 30, 20)
        )

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

        # รวมผลทั้งหมด
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
    app.run()
