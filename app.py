# ==========================================
# 1. Import
# ==========================================

from flask import Flask, render_template, request
import requests
import base64
import os


# ==========================================
# 2. ตั้งค่า Flask
# ==========================================

app = Flask(__name__)


# ==========================================
# 3. Roboflow Workflow
# ==========================================

WORKFLOW_URL = os.environ.get("WORKFLOW_URL")
ROBOFLOW_API_KEY = os.environ.get("ROBOFLOW_API_KEY")


# ==========================================
# 4. ข้อมูลดอกไม้
# ไม่มี bougainvillea แล้ว
# ==========================================

flowers = {

    "carnation": {
        "thai": "คาร์เนชั่น",
        "meaning": "ความรัก ความนอบน้อม กตัญญูรู้คุณ และรักนิรันดร์",
        "opportunity": "วันแม่ งานรับปริญญา งานแต่งงาน และงานมงคลต่าง ๆ"
    },

    "daisy": {
        "thai": "เดซี่",
        "meaning": "ความบริสุทธิ์ ความไร้เดียงสา และความน่าทะนุถนอม",
        "opportunity": "ให้เพื่อแสดงความห่วงใย หรือร่วมแสดงความยินดี"
    },

    "dandelion": {
        "thai": "แดนดิไลออน",
        "meaning": "ความหวัง อิสระ การเริ่มต้นใหม่ และความเข้มแข็ง",
        "opportunity": "การให้กำลังใจ การบอกลาเพื่อเริ่มต้นใหม่"
    },

    "gardenia": {
        "thai": "พุด",
        "meaning": "ความเจริญรุ่งเรืองและความมั่นคงของชีวิต",
        "opportunity": "งานมงคล งานแต่งงาน และการเสริมสิริมงคล"
    },

    "hibiscus": {
        "thai": "ชบา",
        "meaning": "รักครั้งใหม่ ความเจริญก้าวหน้า และความสำเร็จ",
        "opportunity": "โอกาสแสดงความรัก ความอบอุ่น และความยินดี"
    },

    "hydrangeas": {
        "thai": "ไฮเดรนเยีย",
        "meaning": "ความขอบคุณ ความเข้าใจ และความจริงใจ",
        "opportunity": "โอกาสที่ต้องการสื่อสารความรู้สึกจากใจ"
    },

    "lily": {
        "thai": "ลิลลี่",
        "meaning": "ความบริสุทธิ์ ความรัก ความหวัง และการจากลา",
        "opportunity": "งานแต่งงาน วันเกิด วันครบรอบ และการตกแต่งสถานที่"
    },

    "lotus": {
        "thai": "บัว",
        "meaning": "ความบริสุทธิ์ ความสำเร็จ และปัญญา",
        "opportunity": "พิธีกรรมทางศาสนา การบูชาพระ และการตกแต่งสถานที่"
    },

    "orchids": {
        "thai": "กล้วยไม้",
        "meaning": "ความมั่งคั่ง ความสง่างาม และความรักที่มั่นคง",
        "opportunity": "แสดงความยินดี ให้เป็นของขวัญ หรือแสดงความเคารพ"
    },

    "peony": {
        "thai": "โบตั๋น",
        "meaning": "ความรัก ความโรแมนติก ความมั่งคั่ง และความโชคดี",
        "opportunity": "การอวยพรให้มั่งคั่ง โชคดี และมีเกียรติยศ"
    },

    "pinkrose": {
        "thai": "กุหลาบสีชมพู",
        "meaning": "ความสง่างาม ความอ่อนโยน และความรักโรแมนติก",
        "opportunity": "วันเกิด วันครบรอบ วันแม่ หรือมอบเพื่อแสดงความขอบคุณ"
    },

    "redrose": {
        "thai": "กุหลาบแดง",
        "meaning": "ความรักและการตกหลุมรัก",
        "opportunity": "วันวาเลนไทน์ วันครบรอบ การขอแต่งงาน หรือบอกรัก"
    },

    "whiterose": {
        "thai": "กุหลาบขาว",
        "meaning": "ความรักที่บริสุทธิ์และความรักที่ใสสะอาด",
        "opportunity": "งานแต่งงาน วันครบรอบ การแสดงความยินดี"
    },

    "sunflower": {
        "thai": "ทานตะวัน",
        "meaning": "ความสดใส ความหวัง และความมั่นคง",
        "opportunity": "แสดงความยินดี ให้กำลังใจ วันเกิด และวันครบรอบ"
    },

    "tulip": {
        "thai": "ทิวลิป",
        "meaning": "ความรักที่สมบูรณ์ ความมั่นคง และความสุข",
        "opportunity": "บอกรัก วันเกิด วันครบรอบ และแสดงความยินดี"
    }
}


# ==========================================
# 5. ฟังก์ชันเรียก Roboflow
# ==========================================

def detect_flower(image_file):

    # ตรวจสอบว่ามี URL หรือไม่
    if not WORKFLOW_URL:
        raise Exception("ยังไม่ได้ตั้งค่า WORKFLOW_URL ใน Render")

    if not ROBOFLOW_API_KEY:
        raise Exception("ยังไม่ได้ตั้งค่า ROBOFLOW_API_KEY ใน Render")


    # --------------------------------------
    # อ่านรูป
    # --------------------------------------

    image_bytes = image_file.read()


    # --------------------------------------
    # แปลงรูปเป็น Base64
    # --------------------------------------

    image_base64 = base64.b64encode(image_bytes).decode("utf-8")


    # --------------------------------------
    # เตรียมข้อมูลส่ง Roboflow
    # --------------------------------------

    payload = {
        "inputs": {
            "image": {
                "type": "base64",
                "value": image_base64
            }
        }
    }


    # --------------------------------------
    # Header
    # --------------------------------------

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {ROBOFLOW_API_KEY}"
    }


    # --------------------------------------
    # ส่งรูปไป Roboflow
    # --------------------------------------

    response = requests.post(
        WORKFLOW_URL,
        headers=headers,
        json=payload,
        timeout=60
    )


    # --------------------------------------
    # Debug ใน Render Logs
    # --------------------------------------

    print("Roboflow Status:", response.status_code)
    print("Roboflow Response:", response.text)


    # --------------------------------------
    # ตรวจสอบ Error
    # --------------------------------------

    if response.status_code != 200:

        raise Exception(
            f"Roboflow Error {response.status_code}: "
            f"{response.text}"
        )


    # --------------------------------------
    # แปลง Response เป็น JSON
    # --------------------------------------

    data = response.json()


    return data


# ==========================================
# 6. หน้าเว็บไซต์
# ==========================================

@app.route("/", methods=["GET", "POST"])
def home():

    results = None
    error = None
    image_data = None


    # ======================================
    # เมื่อผู้ใช้กดตรวจจับ
    # ======================================

    if request.method == "POST":

        # ----------------------------------
        # ตรวจสอบไฟล์
        # ----------------------------------

        if "image" not in request.files:

            error = "ไม่พบรูปภาพ"

            return render_template(
                "index.html",
                results=None,
                error=error,
                image_data=None
            )


        image = request.files["image"]


        # ----------------------------------
        # ตรวจสอบชื่อไฟล์
        # ----------------------------------

        if image.filename == "":

            error = "กรุณาเลือกรูปภาพ"

            return render_template(
                "index.html",
                results=None,
                error=error,
                image_data=None
            )


        try:

            # --------------------------------
            # อ่านรูปเก็บไว้สำหรับแสดงบนเว็บ
            # --------------------------------

            image_bytes = image.read()

            image_data = (
                "data:"
                + image.content_type
                + ";base64,"
                + base64.b64encode(image_bytes).decode("utf-8")
            )


            # --------------------------------
            # ส่งรูปไป Roboflow
            # --------------------------------

            image.seek(0)

            data = detect_flower(image)


            # --------------------------------
            # ตรวจสอบ predictions
            # --------------------------------

            predictions = []


            # =================================
            # Roboflow Workflow อาจส่งข้อมูล
            # อยู่ภายใน outputs
            # =================================

            if "outputs" in data:

                outputs = data["outputs"]

                if isinstance(outputs, dict):

                    if "predictions" in outputs:

                        predictions = outputs["predictions"]


            # =================================
            # รองรับกรณี predictions อยู่ด้านบน
            # =================================

            if not predictions and "predictions" in data:

                predictions = data["predictions"]


            # --------------------------------
            # ไม่พบดอกไม้
            # --------------------------------

            if not predictions:

                error = "ไม่พบดอกไม้ที่ AI รู้จักในรูปภาพ"

                return render_template(
                    "index.html",
                    results=None,
                    error=error,
                    image_data=image_data
                )


            # =================================
            # เก็บผลการตรวจจับทุกดอก
            # =================================

            results = []


            for prediction in predictions:

                flower_name = prediction.get(
                    "class",
                    "unknown"
                )


                confidence = prediction.get(
                    "confidence",
                    0
                )


                confidence = round(
                    confidence * 100,
                    2
                )


                # --------------------------------
                # ตำแหน่งกรอบ
                # --------------------------------

                x = prediction.get("x", 0)
                y = prediction.get("y", 0)

                width = prediction.get(
                    "width",
                    0
                )

                height = prediction.get(
                    "height",
                    0
                )


                # --------------------------------
                # ข้อมูลดอกไม้
                # --------------------------------

                if flower_name in flowers:

                    info = flowers[flower_name]

                    thai = info["thai"]
                    meaning = info["meaning"]
                    opportunity = info["opportunity"]

                else:

                    thai = flower_name
                    meaning = "ยังไม่มีข้อมูล"
                    opportunity = "ยังไม่มีข้อมูล"


                # --------------------------------
                # เพิ่มผลลัพธ์
                # --------------------------------

                results.append({

                    "class": flower_name,

                    "confidence": confidence,

                    "thai": thai,

                    "meaning": meaning,

                    "opportunity": opportunity,

                    "x": x,

                    "y": y,

                    "width": width,

                    "height": height
                })


        except Exception as e:

            print("ERROR:", str(e))

            error = f"เกิดข้อผิดพลาด: {str(e)}"


    # ==========================================
    # ส่งข้อมูลไป index.html
    # ==========================================

    return render_template(
        "index.html",
        results=results,
        error=error,
        image_data=image_data
    )


# ==========================================
# 7. เริ่ม Flask
# ==========================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=False
    )
