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
# 3. ตั้งค่า Roboflow
# ==========================================

WORKFLOW_URL = os.environ.get("WORKFLOW_URL")
ROBOFLOW_API_KEY = os.environ.get("ROBOFLOW_API_KEY")


# ==========================================
# 4. ข้อมูลดอกไม้
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
        "opportunity": "ให้เพื่อแสดงความห่วงใย หรือร่วมแสดงความยินดีในช่วงเวลาพิเศษ"
    },

    "dandelion": {
        "thai": "แดนดิไลออน",
        "meaning": "ความหวัง อิสระ การเริ่มต้นใหม่ ความเข้มแข็ง และการบอกลา",
        "opportunity": "การบอกลาเพื่อเริ่มต้นใหม่ การให้กำลังใจ หรือการอวยพร"
    },

    "gardenia": {
        "thai": "พุด",
        "meaning": "ความเจริญรุ่งเรืองและความมั่นคงของชีวิต",
        "opportunity": "บูชาพระ งานแต่งงาน และโอกาสที่ต้องการความเป็นสิริมงคล"
    },

    "hibiscus": {
        "thai": "ชบา",
        "meaning": "รักครั้งใหม่ ความเจริญก้าวหน้า และความสำเร็จ",
        "opportunity": "โอกาสแสดงความรัก ความอบอุ่น และความยินดี"
    },

    "hydrangeas": {
        "thai": "ไฮเดรนเยีย",
        "meaning": "ความขอบคุณ ความเข้าใจ และความจริงใจ",
        "opportunity": "โอกาสที่ต้องการสื่อสารความรู้สึกจากใจอย่างอ่อนโยน"
    },

    "lily": {
        "thai": "ลิลลี่",
        "meaning": "ความบริสุทธิ์ ความรัก ความหวัง และการจากลา",
        "opportunity": "งานแต่งงาน งานศพ วันเกิด วันครบรอบ หรือใช้ตกแต่งสถานที่"
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
        "meaning": "ความสง่างาม ความอ่อนโยน และความรัก",
        "opportunity": "วันเกิด วันครบรอบ วันแม่ หรือมอบเพื่อแสดงความยินดี"
    },

    "redrose": {
        "thai": "กุหลาบแดง",
        "meaning": "ความรักและความหลงใหล",
        "opportunity": "วันวาเลนไทน์ วันครบรอบ หรือโอกาสที่ต้องการแสดงความรัก"
    },

    "whiterose": {
        "thai": "กุหลาบขาว",
        "meaning": "ความรักที่บริสุทธิ์และความจริงใจ",
        "opportunity": "งานแต่งงาน วันครบรอบ การแสดงความยินดี หรือการไว้อาลัย"
    },

    "sunflower": {
        "thai": "ทานตะวัน",
        "meaning": "ความสดใส ความหวัง และความมั่นคง",
        "opportunity": "แสดงความยินดี ให้กำลังใจ วันเกิด วันครบรอบ หรือสารภาพรัก"
    },

    "tulip": {
        "thai": "ทิวลิป",
        "meaning": "ความรักที่สมบูรณ์ ความมั่นคง และความสุข",
        "opportunity": "บอกรัก วันเกิด วันครบรอบ และแสดงความยินดี"
    }
}


# ==========================================
# 5. ฟังก์ชันค้นหา predictions
# ==========================================

def find_predictions(data):
    """
    ค้นหา predictions จากข้อมูลที่ Roboflow ส่งกลับมา
    รองรับกรณีที่ predictions อยู่ในหลายระดับของ JSON
    """

    if isinstance(data, dict):

        # กรณีปกติ
        if "predictions" in data:

            predictions = data["predictions"]

            if isinstance(predictions, list):
                return predictions

            # บาง workflow อาจส่งเป็น dict
            if isinstance(predictions, dict):

                if "predictions" in predictions:
                    return predictions["predictions"]

        # ค้นหาต่อในข้อมูลด้านใน
        for value in data.values():

            result = find_predictions(value)

            if result:
                return result

    elif isinstance(data, list):

        for item in data:

            result = find_predictions(item)

            if result:
                return result

    return []


# ==========================================
# 6. หน้าเว็บหลัก
# ==========================================

@app.route("/", methods=["GET", "POST"])
def home():

    results = []
    error = None

    # ข้อมูลรูปสำหรับแสดงกลับหน้าเว็บ
    image_data = None

    # ขนาดรูป
    image_width = 0
    image_height = 0


    # ==========================================
    # GET
    # ==========================================

    if request.method == "GET":

        return render_template(
            "index.html",
            results=results,
            error=error,
            image_data=image_data,
            image_width=image_width,
            image_height=image_height
        )


    # ==========================================
    # POST
    # ==========================================

    try:

        # --------------------------------------
        # ตรวจสอบไฟล์
        # --------------------------------------

        if "image" not in request.files:

            error = "ไม่พบรูปภาพ"

            return render_template(
                "index.html",
                results=results,
                error=error,
                image_data=image_data,
                image_width=image_width,
                image_height=image_height
            )


        image = request.files["image"]


        # --------------------------------------
        # ตรวจสอบชื่อไฟล์
        # --------------------------------------

        if image.filename == "":

            error = "กรุณาเลือกรูปภาพ"

            return render_template(
                "index.html",
                results=results,
                error=error,
                image_data=image_data,
                image_width=image_width,
                image_height=image_height
            )


        # --------------------------------------
        # ตรวจสอบ Workflow URL
        # --------------------------------------

        if not WORKFLOW_URL:

            error = "ยังไม่ได้ตั้งค่า WORKFLOW_URL ใน Render"

            return render_template(
                "index.html",
                results=results,
                error=error,
                image_data=image_data,
                image_width=image_width,
                image_height=image_height
            )


        # --------------------------------------
        # ตรวจสอบ API Key
        # --------------------------------------

        if not ROBOFLOW_API_KEY:

            error = "ยังไม่ได้ตั้งค่า ROBOFLOW_API_KEY ใน Render"

            return render_template(
                "index.html",
                results=results,
                error=error,
                image_data=image_data,
                image_width=image_width,
                image_height=image_height
            )


        # ======================================
        # อ่านรูป
        # ======================================

        image_bytes = image.read()


        # --------------------------------------
        # ตรวจสอบว่ามีข้อมูลรูปจริง
        # --------------------------------------

        if not image_bytes:

            error = "ไม่สามารถอ่านรูปภาพได้"

            return render_template(
                "index.html",
                results=results,
                error=error,
                image_data=image_data,
                image_width=image_width,
                image_height=image_height
            )


        # ======================================
        # แปลงรูปเป็น Base64
        # ======================================

        encoded_image = base64.b64encode(image_bytes).decode("utf-8")


        # ======================================
        # เก็บรูปไว้แสดงหน้าเว็บ
        # ======================================

        image_type = image.content_type or "image/jpeg"

        image_data = (
            f"data:{image_type};base64,{encoded_image}"
        )


        # ======================================
        # ส่งรูปไป Roboflow Workflow
        # ======================================

        payload = {

            "inputs": {

                "image": {

                    "type": "base64",

                    "value": encoded_image

                }

            }

        }


        headers = {

            "Content-Type": "application/json",

            "Authorization":
                f"Bearer {ROBOFLOW_API_KEY}"

        }


        # ======================================
        # POST ไป Roboflow
        # ======================================

        response = requests.post(

            WORKFLOW_URL,

            headers=headers,

            json=payload,

            timeout=60

        )


        # ======================================
        # แสดง Log
        # ======================================

        print(
            "Roboflow Status:",
            response.status_code
        )

        print(
            "Roboflow Response:",
            response.text
        )


        # ======================================
        # ตรวจสอบ Status
        # ======================================

        if response.status_code != 200:

            error = (
                f"Roboflow Error "
                f"{response.status_code}: "
                f"{response.text}"
            )

            return render_template(
                "index.html",
                results=results,
                error=error,
                image_data=image_data,
                image_width=image_width,
                image_height=image_height
            )


        # ======================================
        # แปลง JSON
        # ======================================

        try:

            data = response.json()

        except Exception:

            error = (
                "Roboflow ส่งข้อมูลกลับมา "
                "ไม่ใช่ JSON"
            )

            return render_template(
                "index.html",
                results=results,
                error=error,
                image_data=image_data,
                image_width=image_width,
                image_height=image_height
            )


        # ======================================
        # ค้นหา predictions
        # ======================================

        predictions = find_predictions(data)


        # ======================================
        # ไม่มีผลตรวจจับ
        # ======================================

        if not predictions:

            error = (
                "ไม่พบดอกไม้ที่ AI รู้จักในรูปภาพ"
            )

            return render_template(
                "index.html",
                results=results,
                error=error,
                image_data=image_data,
                image_width=image_width,
                image_height=image_height
            )


        # ======================================
        # ประมวลผล predictions
        # ======================================

        for prediction in predictions:

            if not isinstance(prediction, dict):
                continue


            # ----------------------------------
            # ชื่อ class
            # ----------------------------------

            flower_name = (
                prediction.get("class")
                or prediction.get("class_name")
                or prediction.get("label")
                or "unknown"
            )


            # ----------------------------------
            # Confidence
            # ----------------------------------

            confidence = prediction.get(
                "confidence",
                0
            )


            try:

                confidence = float(confidence)

            except:

                confidence = 0


            # ถ้าเป็น 0-1 ให้เปลี่ยนเป็น %
            if confidence <= 1:

                confidence *= 100


            confidence = round(
                confidence,
                2
            )


            # ----------------------------------
            # ข้อมูลดอกไม้
            # ----------------------------------

            info = flowers.get(
                flower_name.lower(),
                {}
            )


            thai_name = info.get(
                "thai",
                flower_name
            )


            meaning = info.get(
                "meaning",
                "ยังไม่มีข้อมูล"
            )


            opportunity = info.get(
                "opportunity",
                "ยังไม่มีข้อมูล"
            )


            # ==================================
            # Bounding Box
            # ==================================

            x = prediction.get("x", 0)
            y = prediction.get("y", 0)
            width = prediction.get("width", 0)
            height = prediction.get("height", 0)


            try:

                x = float(x)
                y = float(y)
                width = float(width)
                height = float(height)

            except:

                x = 0
                y = 0
                width = 0
                height = 0


            # ==================================
            # เพิ่มผลลัพธ์
            # ==================================

            results.append({

                "class": flower_name,

                "confidence": confidence,

                "thai": thai_name,

                "meaning": meaning,

                "opportunity": opportunity,

                "x": x,

                "y": y,

                "width": width,

                "height": height

            })


        # ======================================
        # ตรวจสอบอีกครั้ง
        # ======================================

        if not results:

            error = (
                "AI ส่งข้อมูลกลับมา "
                "แต่ไม่พบผลการตรวจจับ"
            )


    # ==========================================
    # Error
    # ==========================================

    except requests.exceptions.Timeout:

        error = (
            "เชื่อมต่อ Roboflow นานเกินไป "
            "กรุณาลองใหม่"
        )


    except requests.exceptions.RequestException as e:

        print(
            "Request Error:",
            str(e)
        )

        error = (
            "ไม่สามารถเชื่อมต่อ Roboflow ได้"
        )


    except Exception as e:

        print(
            "Error:",
            str(e)
        )

        error = (
            f"เกิดข้อผิดพลาด: {str(e)}"
        )


    # ==========================================
    # ส่งข้อมูลกลับ index.html
    # ==========================================

    return render_template(

        "index.html",

        results=results,

        error=error,

        image_data=image_data,

        image_width=image_width,

        image_height=image_height

    )


# ==========================================
# 7. เริ่ม Server
# ==========================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(
            os.environ.get(
                "PORT",
                5000
            )
        )
    )
