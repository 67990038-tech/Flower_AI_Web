from flask import Flask, render_template, request
import requests
import base64
import os


# ==========================================
# 1. ตั้งค่า Flask
# ==========================================

app = Flask(__name__)

# API URL ของ Roboflow
API_URL = os.environ.get("API_URL")


# ==========================================
# 2. ข้อมูลดอกไม้
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
        "opportunity": "วันแม่ งานรับปริญญา งานแต่งงาน และงานมงคลต่าง ๆ"
    },

    "daisy": {
        "thai": "เดซี่",
        "meaning": "ความบริสุทธิ์ ความไร้เดียงสา และความน่าทะนุถนอม",
        "opportunity": "แสดงความห่วงใย หรือร่วมแสดงความยินดีในช่วงเวลาพิเศษ"
    },

    "dandelion": {
        "thai": "แดนดิไลออน",
        "meaning": "ความหวัง อิสระ การเริ่มต้นใหม่ และความเข้มแข็ง",
        "opportunity": "การเริ่มต้นใหม่ การให้กำลังใจ หรือการอวยพร"
    },

    "gardenia": {
        "thai": "พุด",
        "meaning": "ความเจริญรุ่งเรืองและความมั่นคงของชีวิต",
        "opportunity": "งานมงคล งานแต่งงาน และการเสริมสิริมงคล"
    },

    "hibiscus": {
        "thai": "ชบา",
        "meaning": "รักครั้งใหม่ ความเจริญก้าวหน้า และความสำเร็จ",
        "opportunity": "แสดงความรัก ความอบอุ่น และความยินดี"
    },

    "hydrangeas": {
        "thai": "ไฮเดรนเยีย",
        "meaning": "ความขอบคุณ ความเข้าใจ และความจริงใจ",
        "opportunity": "โอกาสที่ต้องการสื่อสารความรู้สึกจากใจอย่างอ่อนโยน"
    },

    "lily": {
        "thai": "ลิลลี่",
        "meaning": "ความบริสุทธิ์ ความรัก ความหวัง และการจากลา",
        "opportunity": "งานแต่งงาน ของขวัญวันเกิด วันครบรอบ และการตกแต่งสถานที่"
    },

    "lotus": {
        "thai": "บัว",
        "meaning": "ความบริสุทธิ์ ความสำเร็จ และปัญญา",
        "opportunity": "พิธีกรรมทางศาสนา การบูชาพระ และการตกแต่งสถานที่"
    },

    "orchids": {
        "thai": "กล้วยไม้",
        "meaning": "ความมั่งคั่ง ความสง่างาม และความรักที่มั่นคง",
        "opportunity": "แสดงความยินดี มอบเป็นของขวัญ หรือแสดงความเคารพ"
    },

    "peony": {
        "thai": "โบตั๋น",
        "meaning": "ความโรแมนติกและความรักที่สมบูรณ์",
        "opportunity": "อวยพรให้มั่งคั่ง โชคดี และมีเกียรติยศ"
    },

    "pinkrose": {
        "thai": "กุหลาบสีชมพู",
        "meaning": "ความสง่างาม ความอ่อนโยน และความรักโรแมนติก",
        "opportunity": "วันเกิด วันครบรอบ วันแม่ หรือมอบเพื่อแสดงความยินดี"
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
        "opportunity": "แสดงความยินดี ให้กำลังใจ วันเกิด หรือวันครบรอบ"
    },

    "tulip": {
        "thai": "ทิวลิป",
        "meaning": "ความรักที่สมบูรณ์และมั่นคง",
        "opportunity": "บอกรัก วันเกิด วันครบรอบ และแสดงความยินดี"
    }
}


# ==========================================
# 3. หน้าเว็บไซต์
# ==========================================

@app.route("/", methods=["GET", "POST"])
def home():

    results = []
    error = None

    # รูปที่จะแสดงหลังตรวจจับ
    image_preview = None

    # ======================================
    # เมื่อกดตรวจจับ
    # ======================================

    if request.method == "POST":

        # -----------------------------
        # ตรวจสอบว่ามีไฟล์
        # -----------------------------

        if "image" not in request.files:

            error = "ไม่พบรูปภาพ"

            return render_template(
                "index.html",
                results=results,
                error=error,
                image_preview=image_preview
            )

        image = request.files["image"]

        # -----------------------------
        # ตรวจสอบชื่อไฟล์
        # -----------------------------

        if image.filename == "":

            error = "กรุณาเลือกรูปภาพ"

            return render_template(
                "index.html",
                results=results,
                error=error,
                image_preview=image_preview
            )

        # -----------------------------
        # ตรวจสอบ API
        # -----------------------------

        if not API_URL:

            error = "ไม่พบ API_URL กรุณาตั้งค่า API_URL ใน Render"

            return render_template(
                "index.html",
                results=results,
                error=error,
                image_preview=image_preview
            )

        try:

            # ==================================
            # อ่านรูป
            # ==================================

            image_bytes = image.read()

            # ==================================
            # ทำรูปเป็น Base64
            # เพื่อให้เว็บแสดงรูปหลังตรวจจับ
            # ==================================

            image_base64 = base64.b64encode(
                image_bytes
            ).decode("utf-8")

            image_preview = (
                "data:"
                + image.content_type
                + ";base64,"
                + image_base64
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
                        image.content_type
                    )
                },

                timeout=60
            )

            print("Roboflow Status:", response.status_code)
            print("Roboflow Response:", response.text)

            # ==================================
            # ตรวจสอบ Response
            # ==================================

            if response.status_code != 200:

                error = (
                    "Roboflow Error "
                    + str(response.status_code)
                    + ": "
                    + response.text
                )

                return render_template(
                    "index.html",
                    results=results,
                    error=error,
                    image_preview=image_preview
                )

            # ==================================
            # แปลงเป็น JSON
            # ==================================

            data = response.json()

            # ==================================
            # ตรวจสอบ Predictions
            # ==================================

            predictions = data.get("predictions", [])

            if len(predictions) == 0:

                error = "ไม่พบดอกไม้ที่ AI รู้จักในรูปภาพ"

                return render_template(
                    "index.html",
                    results=[],
                    error=error,
                    image_preview=image_preview
                )

            # ==================================
            # วนดูดอกไม้ทุกดอก
            # ==================================

            for prediction in predictions:

                flower_name = prediction.get(
                    "class",
                    "unknown"
                )

                confidence = round(
                    prediction.get("confidence", 0) * 100,
                    2
                )

                # ------------------------------
                # ถ้ามีข้อมูลในระบบ
                # ------------------------------

                if flower_name in flowers:

                    info = flowers[flower_name]

                    results.append({

                        "class": flower_name,

                        "confidence": confidence,

                        "thai": info["thai"],

                        "meaning": info["meaning"],

                        "opportunity": info["opportunity"]

                    })

                # ------------------------------
                # ถ้าไม่มีข้อมูล
                # ------------------------------

                else:

                    results.append({

                        "class": flower_name,

                        "confidence": confidence,

                        "thai": "ยังไม่มีข้อมูล",

                        "meaning": "ยังไม่มีข้อมูล",

                        "opportunity": "ยังไม่มีข้อมูล"

                    })

        except Exception as e:

            print("ERROR:", str(e))

            error = "เกิดข้อผิดพลาด: " + str(e)

    # ==========================================
    # ส่งข้อมูลไป HTML
    # ==========================================

    return render_template(

        "index.html",

        results=results,

        error=error,

        image_preview=image_preview

    )


# ==========================================
# 4. เริ่ม Flask
# ==========================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000)),
        debug=True
    )
