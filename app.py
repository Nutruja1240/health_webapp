from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
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

            bmi = round(weight / (height ** 2), 2)
            bmi_status = interpret_bmi(bmi)
            sugar_status, sugar_advice = interpret_sugar(sugar)
            bp_status, bp_advice = interpret_bp(systolic, diastolic)
            waist_status, waist_advice = interpret_waist(waist, gender)

            result = {
                'bmi': bmi,
                'bmi_status': bmi_status,
                'sugar_status': sugar_status,
                'sugar_advice': sugar_advice,
                'bp_status': bp_status,
                'bp_advice': bp_advice,
                'waist_status': waist_status,
                'waist_advice': waist_advice
            }
        except:
            result = {'error': 'กรุณากรอกข้อมูลให้ครบและถูกต้อง'}
    return render_template('index.html', result=result)

def interpret_bmi(bmi):
    if bmi < 18.5:
        return 'ผอม'
    elif bmi < 23:
        return 'ปกติ'
    elif bmi < 25:
        return 'น้ำหนักเกิน'
    elif bmi < 30:
        return 'อ้วนระดับ 1'
    else:
        return 'อ้วนระดับ 2'

def interpret_sugar(sugar):
    if sugar < 70:
        return 'น้ำตาลต่ำ', 'ควรปรึกษาแพทย์เรื่องภาวะน้ำตาลต่ำ'
    elif sugar <= 99:
        return 'ปกติ', ''
    elif sugar <= 125:
        return 'ระดับน้ำตาลเริ่มสูง', 'ควรควบคุมอาหาร หมั่นออกกำลังกาย'
    else:
        return 'เบาหวาน', 'ควรพบแพทย์เพื่อตรวจเพิ่มเติมและรับคำแนะนำ'

def interpret_bp(sys, dia):
    if sys < 120 and dia < 80:
        return 'ความดันปกติ', ''
    elif 120 <= sys <= 139 or 80 <= dia <= 89:
        return 'ความดันเริ่มสูง', 'ควรลดเค็ม ออกกำลังกาย และติดตามความดันสม่ำเสมอ'
    else:
        return 'ความดันสูง', 'ควรพบแพทย์และควบคุมอาหาร/น้ำหนัก'

def interpret_waist(waist, gender):
    if (gender == 'male' and waist >= 90) or (gender == 'female' and waist >= 80):
        advice = (
            "คุณมีภาวะอ้วนลงพุง ซึ่งอาจเสี่ยงต่อโรคเบาหวาน ความดัน ไขมันในเลือดสูง โรคหัวใจ "
            "ควรลดน้ำตาล ออกกำลังกายสม่ำเสมอ และควบคุมน้ำหนัก"
        )
        return 'รอบเอวเกินมาตรฐาน (อ้วนลงพุง)', advice
    else:
        return 'รอบเอวปกติ', ''

if __name__ == '__main__':
    app.run(debug=True)