import os
import base64
import requests
from flask import Flask, render_template, request

# ==========================================
# ตั้งค่า Flask
# ==========================================
app = Flask(__name__)

# ==========================================
# Roboflow Workflow API
# ==========================================
API_URL = os.environ.get("API_URL")
API_KEY = os.environ.get("API_KEY")

# ==========================================
# ข้อมูลดอกไม้
# ==========================================
flowers = {
    "carnation": {
        "thai": "คาร์เนชั่น",
        "meaning": "ความรัก ความนอบน้อม กตัญญูรู้คุณ และรักนิรันดร์",
        "opportunity": "วันแม่ งานมงคลต่าง ๆ เช่น งานรับปริญญา งานแต่งงาน และงานขึ้นบ้านใหม่"
    },
    "daisy": {
        "thai": "เดซี่",
        "meaning": "ความบริสุทธิ์ ความไร้เดียงสา และความน่าทะนุถนอม",
        "opportunity": "ให้เพื่อแสดงความห่วงใย หรือร่วมแสดงความยินดีในช่วงเวลาพิเศษ"
    },
    "dandelion": {
        "thai": "แดนดิไลออน",
        "meaning": "ความหวัง อิสระ การเริ่มต้นใหม่ ความเข้มแข็ง และการบอกลา",
        "opportunity": "การบอกลาเพื่อเริ่มต้นใหม่ การให้กำลังใจ หรือการอวยพรให้สมหวังในคำอธิษฐาน"
    },
    "gardenia": {
        "thai": "พุด",
        "meaning": "ความเจริญรุ่งเรืองและความมั่นคงของชีวิต",
        "opportunity": "บูชาพระเพื่อเสริมสิริมงคล งานแต่งงาน และโอกาสสำคัญของครอบครัว"
    },
    "hibiscus": {
        "thai": "ชบา",
        "meaning": "รักครั้งใหม่ ความเจริญก้าวหน้า และความสำเร็จ",
        "opportunity": "โอกาสแสดงความรัก ความอบอุ่น และความยินดี"
    },
    "hydrangeas": {
        "thai": "ไฮเดรนเยีย",
        "meaning": "ความขอบคุณ ความเข้าใจ และความจริงใจ",
        "opportunity": "โอกาสที่ต้องการสื่อสารความรู้สึกจากใจอย่างอ่อนโยนและจริงใจ"
    },
    "lily": {
        "thai": "ลิลลี่",
        "meaning": "ความบริสุทธิ์ ความรัก ความหวัง และการจากลา",
        "opportunity": "งานแต่งงาน งานศพ ของขวัญวันเกิด วันครบรอบ และการตกแต่งสถานที่"
    },
    "lotus": {
        "thai": "บัว",
        "meaning": "ความบริสุทธิ์ ความสำเร็จ และปัญญาในพระพุทธศาสนา",
        "opportunity": "พิธีกรรมทางศาสนาพุทธ การบูชาพระ วัฒนธรรมไทย และการตกแต่งสถานที่"
    },
    "orchids": {
        "thai": "กล้วยไม้",
        "meaning": "ความมั่งคั่ง ความสง่างาม และความรักที่มั่นคง",
        "opportunity": "แสดงความยินดี ให้เป็นของขวัญ แสดงความเคารพต่อผู้ใหญ่ หรือบุคคลที่ชื่นชม"
    },
    "peony": {
        "thai": "โบตั๋น",
        "meaning": "ความโรแมนติกและความรักที่สมบูรณ์เต็มเปี่ยมไปด้วยความสุข",
        "opportunity": "การอวยพรให้มั่งคั่ง โชคดี และมีเกียรติยศ"
    },
    "pinkrose": {
        "thai": "กุหลาบสีชมพู",
        "meaning": "ความสง่างาม ความอ่อนโยน และความรักโรแมนติก",
        "opportunity": "วันวาเลนไทน์ วันเกิด วันครบรอบ วันแม่ หรือมอบเพื่อแสดงความยินดีและขอบคุณ"
    },
    "redrose": {
        "thai": "กุหลาบแดง",
        "meaning": "การตกหลุมรักหรือปลื้มใครสักคน",
        "opportunity": "วันวาเลนไทน์ วันครบรอบ การขอแต่งงาน หรือวันธรรมดาที่ต้องการบอกรัก"
    },
    "whiterose": {
        "thai": "กุหลาบขาว",
        "meaning": "ความรักที่ใสสะอาด บริสุทธิ์ และน่าทะนุถนอม",
        "opportunity": "งานแต่งงาน วันครบรอบ การแสดงความยินดี หรือการแสดงความไว้อาลัย"
    },
    "sunflower": {
        "thai": "ทานตะวัน",
        "meaning": "ความสดใส ความหวัง และความมั่นคง",
        "opportunity": "แสดงความยินดี ให้กำลังใจ วันเกิด วันครบรอบ สารภาพรัก หรือเติมความหวาน"
    },
    "tulip": {
        "thai": "ทิวลิป",
        "meaning": "ความรักที่สมบูรณ์และมั่นคง และความสุข",
        "opportunity": "บอกรัก อวยพรวันเกิด วันครบรอบ หรือแสดงความยินดี"
    }
}

# ==========================================
# หน้าเว็บไซต์
# ==========================================
@app.route("/", methods=["GET", "POST"])
def home():
    results = None
    error = None
    image_preview = None

    if request.method == "GET":
        return render_template("index.html", results=None, error=None, image_preview=None)

    # ======================================
    # เมื่อกดปุ่มส่งรูปภาพ (POST)
    # ======================================
    try:
        # ตรวจไฟล์
        if "image" not in request.files:
            return render_template("index.html", results=None, error="ไม่พบรูปภาพ", image_preview=None)

        image = request.files["image"]
        if image.filename == "":
            return render_template("index.html", results=None, error="กรุณาเลือกรูปภาพ", image_preview=None)

        # ตรวจ Environment Variables
        if not API_URL:
            return render_template("index.html", results=None, error="ไม่พบ API_URL ในระบบ", image_preview=None)
        if not API_KEY:
            return render_template("index.html", results=None, error="ไม่พบ API_KEY ในระบบ", image_preview=None)

        # อ่านและแปลงรูปเป็น Base64 สำหรับ Preview และส่งไป API
        image_bytes = image.read()
        image_base64 = base64.b64encode(image_bytes).decode("utf-8")
        image_type = image.content_type or "image/jpeg"
        image_preview = f"data:{image_type};base64,{image_base64}"

        # ตั้งค่า Headers & Payload ส่งไป Roboflow
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {API_KEY}"
        }
        payload = {
            "inputs": {
                "image": {
                    "type": "base64",
                    "value": image_base64
                }
            }
        }

        # ส่งคำขอไปที่ Roboflow
        response = requests.post(API_URL, headers=headers, json=payload, timeout=120)

        print("Roboflow Status:", response.status_code)

        if response.status_code != 200:
            error = f"Roboflow Error {response.status_code}: {response.text}"
            return render_template("index.html", results=None, error=error, image_preview=image_preview)

        try:
            data = response.json()
        except Exception:
            return render_template("index.html", results=None, error="Roboflow ไม่ได้ส่งข้อมูล JSON กลับมา", image_preview=image_preview)

        print("Roboflow JSON:", data)

        # ==================================
        # ดึง predictions (รองรับทั้ง API เก่า และ Workflow API)
        # ==================================
        predictions = []

        # 1. กรณีเป็น API แบบเก่า (Inference API)
        if "predictions" in data and isinstance(data["predictions"], list):
            predictions.extend(data["predictions"])

        # 2. กรณีเป็น Workflow API
        elif "outputs" in data:
            outputs = data["outputs"]
            
            if not isinstance(outputs, list):
                outputs = [outputs]

            for output in outputs:
                if not isinstance(output, dict):
                    continue
                
                # ค้นหา object ชื่อ predictions ไม่ว่ามันจะซ่อนอยู่ใต้ชื่อโมเดลอะไร
                for step_name, step_data in output.items():
                    if isinstance(step_data, dict) and "predictions" in step_data:
                        step_preds = step_data["predictions"]
                        if isinstance(step_preds, list):
                            predictions.extend(step_preds)
                    elif isinstance(step_data, list):
                        if len(step_data) > 0 and isinstance(step_data[0], dict) and ("class" in step_data[0] or "class_name" in step_data[0]):
                            predictions.extend(step_data)

        # กรองข้อมูลให้มั่นใจว่าเป็น Dictionary
        valid_predictions = [p for p in predictions if isinstance(p, dict)]
        predictions = valid_predictions

        if not predictions:
            return render_template(
                "index.html",
                results=None,
                error="AI ประมวลผลสำเร็จ แต่ไม่พบดอกไม้ในรูปภาพ (หรือความมั่นใจต่ำเกินไป)",
                image_preview=image_preview
            )

        # ==================================
        # สร้างผลลัพธ์จัดเตรียมส่งให้หน้าเว็บ
        # ==================================
        results = []
        for prediction in predictions:
            flower_name = prediction.get("class", prediction.get("class_name", "unknown"))
            confidence = prediction.get("confidence", 0)

            try:
                confidence = float(confidence)
            except:
                confidence = 0

            # แปลงเป็นเปอร์เซ็นต์
            if confidence <= 1:
                confidence = confidence * 100
            confidence = round(confidence, 2)

            x = prediction.get("x", 0)
            y = prediction.get("y", 0)
            width = prediction.get("width", 0)
            height = prediction.get("height", 0)

            # ตรวจสอบว่าชื่อดอกไม้มีในฐานข้อมูลของเราหรือไม่
            if flower_name in flowers:
                info = flowers[flower_name]
                results.append({
                    "class": flower_name,
                    "confidence": confidence,
                    "thai": info["thai"],
                    "meaning": info["meaning"],
                    "opportunity": info["opportunity"],
                    "x": x, "y": y, "width": width, "height": height
                })
            else:
                results.append({
                    "class": flower_name,
                    "confidence": confidence,
                    "thai": "ยังไม่มีข้อมูลภาษาไทย",
                    "meaning": "ยังไม่มีข้อมูล",
                    "opportunity": "ยังไม่มีข้อมูล",
                    "x": x, "y": y, "width": width, "height": height
                })

        return render_template("index.html", results=results, error=None, image_preview=image_preview)

    except requests.exceptions.RequestException as e:
        print("Request Error:", str(e))
        error = f"ไม่สามารถเชื่อมต่อ Roboflow ได้: {str(e)}"

    except Exception as e:
        print("Error:", str(e))
        error = f"เกิดข้อผิดพลาด: {str(e)}"

    return render_template("index.html", results=results, error=error, image_preview=image_preview)

# ==========================================
# เริ่มการทำงานของ Server
# ==========================================
if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True
    )
