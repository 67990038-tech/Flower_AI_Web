# ==========================================
# 1. Import
# ==========================================

from flask import Flask, render_template, request
import requests
import base64
import os


# ==========================================
# 2. สร้าง Flask App
# ==========================================

app = Flask(__name__)


# ==========================================
# 3. Roboflow API
# ==========================================

API_URL = os.environ.get("API_URL")


# ==========================================
# 4. ข้อมูลดอกไม้
# ==========================================

flowers = {

    "bougainvillea": {
        "thai": "เฟื่องฟ้า",
        "meaning": "ความรุ่งเรือง ความก้าวหน้า และชีวิตที่สดใส",
        "opportunity": "เลื่อนตำแหน่ง เปิดกิจการใหม่ ขึ้นบ้านใหม่ งานแต่งงาน หรืออวยพรให้ชีวิตประสบความสำเร็จและมีความสุข"
    },

    "carnation": {
        "thai": "คาร์เนชั่น",
        "meaning": "ความรัก ความนอบน้อม กตัญญูรู้คุณ และรักนิรันดร์",
        "opportunity": "วันแม่ งานรับปริญญา งานแต่งงาน และงานขึ้นบ้านใหม่"
    },

    "daisy": {
        "thai": "เดซี่",
        "meaning": "ความบริสุทธิ์ ความไร้เดียงสา และความน่าทะนุถนอม",
        "opportunity": "ให้เพื่อแสดงความห่วงใย หรือร่วมแสดงความยินดีในช่วงเวลาพิเศษ"
    },

    "dandelion": {
        "thai": "แดนดิไลออน",
        "meaning": "ความหวัง อิสระ การเริ่มต้นใหม่ และความเข้มแข็ง",
        "opportunity": "การบอกลาเพื่อเริ่มต้นใหม่ การให้กำลังใจ หรือการอวยพรให้สมหวัง"
    },

    "gardenia": {
        "thai": "พุด",
        "meaning": "ความเจริญรุ่งเรืองและความมั่นคงของชีวิต",
        "opportunity": "บูชาพระ เสริมสิริมงคล งานแต่งงาน และโอกาสสำคัญ"
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
        "opportunity": "งานแต่งงาน งานศพ วันเกิด วันครบรอบ และตกแต่งสถานที่"
    },

    "lotus": {
        "thai": "บัว",
        "meaning": "ความบริสุทธิ์ ความสำเร็จ และปัญญาในพระพุทธศาสนา",
        "opportunity": "พิธีกรรมทางศาสนา การบูชาพระ วัฒนธรรมไทย และการตกแต่งสถานที่"
    },

    "orchids": {
        "thai": "กล้วยไม้",
        "meaning": "ความมั่งคั่ง ความสง่างาม และความรักที่มั่นคง",
        "opportunity": "แสดงความยินดี ให้เป็นของขวัญ หรือแสดงความเคารพ"
    },

    "peony": {
        "thai": "โบตั๋น",
        "meaning": "ความโรแมนติกและความรักที่สมบูรณ์",
        "opportunity": "การอวยพรให้มั่งคั่ง โชคดี และมีเกียรติยศ"
    },

    "pinkrose": {
        "thai": "กุหลาบสีชมพู",
        "meaning": "ความสง่างาม ความอ่อนโยน และความรักโรแมนติก",
        "opportunity": "วันวาเลนไทน์ วันเกิด วันครบรอบ วันแม่ หรือแสดงความขอบคุณ"
    },

    "redrose": {
        "thai": "กุหลาบแดง",
        "meaning": "ความรักและการตกหลุมรัก",
        "opportunity": "วันวาเลนไทน์ วันครบรอบ การขอแต่งงาน หรือบอกรัก"
    },

    "whiterose": {
        "thai": "กุหลาบขาว",
        "meaning": "ความรักที่บริสุทธิ์และน่าทะนุถนอม",
        "opportunity": "งานแต่งงาน วันครบรอบ การแสดงความยินดี หรือการไว้อาลัย"
    },

    "sunflower": {
        "thai": "ทานตะวัน",
        "meaning": "ความสดใส ความหวัง และความมั่นคง",
        "opportunity": "แสดงความยินดี ให้กำลังใจ วันเกิด วันครบรอบ หรือสารภาพรัก"
    },

    "tulip": {
        "thai": "ทิวลิป",
        "meaning": "ความรักที่สมบูรณ์และมั่นคง",
        "opportunity": "บอกรัก วันเกิด วันครบรอบ หรือแสดงความยินดี"
    }
}


# ==========================================
# 5. หน้าเว็บไซต์
# ==========================================

@app.route("/", methods=["GET", "POST"])
def home():

    results = []
    error = None
    image_preview = None

    # ======================================
    # เปิดหน้าเว็บ
    # ======================================

    if request.method == "GET":

        return render_template(
            "index.html",
            results=results,
            error=error,
            image_preview=image_preview
        )

    # ======================================
    # เมื่อผู้ใช้ส่งรูป
    # ======================================

    try:

        # ----------------------------------
        # ตรวจสอบว่ามีไฟล์ image หรือไม่
        # ----------------------------------

        if "image" not in request.files:

            error = "ไม่พบรูปภาพ"

            return render_template(
                "index.html",
                results=results,
                error=error,
                image_preview=image_preview
            )

        image = request.files["image"]

        # ----------------------------------
        # ตรวจสอบว่าเลือกไฟล์หรือไม่
        # ----------------------------------

        if image.filename == "":

            error = "กรุณาเลือกรูปภาพ"

            return render_template(
                "index.html",
                results=results,
                error=error,
                image_preview=image_preview
            )

        # ----------------------------------
        # ตรวจสอบ API_URL
        # ----------------------------------

        if not API_URL:

            error = "ไม่พบ API_URL กรุณาตั้งค่า API_URL ใน Render"

            return render_template(
                "index.html",
                results=results,
                error=error,
                image_preview=image_preview
            )

        # ==================================
        # อ่านรูป
        # ==================================

        image_bytes = image.read()

        image_type = image.content_type or "image/jpeg"

        # ==================================
        # สร้างรูป Preview
        # ==================================

        image_base64 = base64.b64encode(
            image_bytes
        ).decode("utf-8")

        image_preview = (
            f"data:{image_type};base64,{image_base64}"
        )

        # ==================================
        # ส่งรูปไป Roboflow
        # ==================================

        response = requests.post(

            API_URL,

            files={
                "file": (
                    image.filename,
                    image_bytes,
                    image_type
                )
            },

            timeout=60
        )

        # ==================================
        # Debug
        # ==================================

        print(
            "Roboflow Status:",
            response.status_code
        )

        print(
            "Roboflow Response:",
            response.text
        )

        # ==================================
        # ตรวจสอบ Roboflow
        # ==================================

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
                image_preview=image_preview
            )

        # ==================================
        # แปลง JSON
        # ==================================

        data = response.json()

        # ==================================
        # ดึง predictions
        # ==================================

        predictions = data.get(
            "predictions",
            []
        )

        # ==================================
        # ไม่พบดอกไม้
        # ==================================

        if not predictions:

            error = "ไม่พบดอกไม้ที่ AI รู้จักในรูปภาพ"

            return render_template(
                "index.html",
                results=results,
                error=error,
                image_preview=image_preview
            )

        # ==================================
        # ตรวจดอกไม้ทุกดอก
        # ==================================

        for prediction in predictions:

            # --------------------------------
            # ชื่อดอกไม้
            # --------------------------------

            flower_name = prediction.get(
                "class",
                "unknown"
            )

            # --------------------------------
            # ความมั่นใจ
            # --------------------------------

            confidence = prediction.get(
                "confidence",
                0
            )

            confidence = round(
                confidence * 100,
                2
            )

            # --------------------------------
            # Bounding Box
            # --------------------------------

            x = prediction.get("x", 0)
            y = prediction.get("y", 0)
            width = prediction.get("width", 0)
            height = prediction.get("height", 0)

            # --------------------------------
            # ถ้ามีข้อมูลดอกไม้
            # --------------------------------

            if flower_name in flowers:

                info = flowers[flower_name]

                results.append({

                    "class": flower_name,

                    "confidence": confidence,

                    "thai": info["thai"],

                    "meaning": info["meaning"],

                    "opportunity": info["opportunity"],

                    "x": x,
                    "y": y,
                    "width": width,
                    "height": height

                })

            # --------------------------------
            # ถ้าไม่มีข้อมูลดอกไม้
            # --------------------------------

            else:

                results.append({

                    "class": flower_name,

                    "confidence": confidence,

                    "thai": "ยังไม่มีข้อมูล",

                    "meaning": "ยังไม่มีข้อมูล",

                    "opportunity": "ยังไม่มีข้อมูล",

                    "x": x,
                    "y": y,
                    "width": width,
                    "height": height

                })

        # ==================================
        # ส่งข้อมูลกลับ index.html
        # ==================================

        return render_template(

            "index.html",

            results=results,

            error=error,

            image_preview=image_preview

        )

    # ======================================
    # Error จากการเชื่อมต่อ
    # ======================================

    except requests.exceptions.RequestException as e:

        print(
            "Connection Error:",
            str(e)
        )

        error = (
            "ไม่สามารถเชื่อมต่อกับ Roboflow ได้: "
            + str(e)
        )

        return render_template(

            "index.html",

            results=results,

            error=error,

            image_preview=image_preview

        )

    # ======================================
    # Error อื่น ๆ
    # ======================================

    except Exception as e:

        print(
            "Error:",
            str(e)
        )

        error = (
            "เกิดข้อผิดพลาด: "
            + str(e)
        )

        return render_template(

            "index.html",

            results=results,

            error=error,

            image_preview=image_preview

        )


# ==========================================
# 6. เริ่มเว็บไซต์
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
