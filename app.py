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
            bmi_status, bmi_advice = interpret_bmi(bmi)
            sugar_status, sugar_advice = interpret_sugar(sugar)
            bp_status, bp_advice = interpret_bp(systolic, diastolic)
            waist_status, waist_advice = interpret_waist(waist, gender)

            result = {
                'bmi': bmi,
                'bmi_status': bmi_status,
                'bmi_advice': bmi_advice,
                'sugar_status': sugar_status,
                'sugar_advice': sugar_advice,
                'bp_status': bp_status,
                'bp_advice': bp_advice,
                'waist_status': waist_status,
                'waist_advice': waist_advice
            }

        except Exception as e:
            result = {'error': 'กรุณากรอกข้อมูลให้ครบถ้วน'}
    
    return render_template('index.html', result=result)

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
        advice = (
            "คุณมีรอบเอวสูง อาจเสี่ยงต่อโรคหัวใจ ความดัน เบาหวาน "
            "ควรลดน้ำตาล ออกกำลังกายสม่ำเสมอ และควบคุมน้ำหนัก"
        )
        return 'รอบเอวเกินเกณฑ์', advice
    else:
        return 'รอบเอวปกติ', 'ดีมาก ควรรักษาไว้ด้วยการควบคุมอาหารและออกกำลังกาย'

if __name__ == '__main__':
    app.run(debug=False)
