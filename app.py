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
# 3. Roboflow API
# ==========================================

# ใช้ Environment Variable
# ใน Render จะต้องสร้าง API_URL ไว้

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
        "opportunity": "วันแม่ งานมงคลต่าง ๆ เช่น งานรับปริญญา งานแต่งงาน งานขึ้นบ้านใหม่"
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
        "opportunity": "บูชาพระเพื่อเสริมสิริมงคล งานฉลอง และงานแต่งงาน"
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
        "opportunity": "งานแต่งงาน งานศพ ของขวัญวันเกิด วันครบรอบ และตกแต่งสถานที่"
    },

    "lotus": {
        "thai": "บัว",
        "meaning": "ความบริสุทธิ์ ความสำเร็จ และปัญญา",
        "opportunity": "พิธีกรรมทางศาสนา การบูชาพระ วัฒนธรรมไทย การตกแต่งสถานที่"
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
        "opportunity": "วันเกิด วันครบรอบ วันแม่ หรือมอบเพื่อแสดงความยินดีและขอบคุณ"
    },

    "redrose": {
        "thai": "กุหลาบแดง",
        "meaning": "การตกหลุมรักหรือปลื้มใครซักคน",
        "opportunity": "วันวาเลนไทน์ วันครบรอบ การขอแต่งงาน หรือการบอกรัก"
    },

    "whiterose": {
        "thai": "กุหลาบขาว",
        "meaning": "ความรักที่ใสสะอาด บริสุทธิ์ และน่าทะนุถนอม",
        "opportunity": "งานแต่งงาน วันครบรอบ การแสดงความยินดี หรือการแสดงความไว้อาลัย"
    },

    "sunflower": {
        "thai": "ทานตะวัน",
        "meaning": "ความสดใส ความหวัง และความมั่นคง",
        "opportunity": "แสดงความยินดี ให้กำลังใจ วันเกิด วันครบรอบ หรือสารภาพรัก"
    },

    "tulip": {
        "thai": "ทิวลิป",
        "meaning": "ความรักที่สมบูรณ์และมั่นคง ความสุข",
        "opportunity": "บอกรัก อวยพรวันเกิด วันครบรอบ หรือแสดงความยินดี"
    }
}


# ==========================================
# 5. หน้าเว็บไซต์
# ==========================================

@app.route("/", methods=["GET", "POST"])
def home():

    results = None
    error = None
    image_base64 = None

    # --------------------------------------
    # เมื่อผู้ใช้กดตรวจจับ
    # --------------------------------------

    if request.method == "POST":

        # ----------------------------------
        # ตรวจสอบว่ามี image หรือไม่
        # ----------------------------------

        if "image" not in request.files:

            error = "ไม่พบรูปภาพ"

            return render_template(
                "index.html",
                results=None,
                error=error,
                image_base64=None
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
                image_base64=None
            )


        # ----------------------------------
        # ตรวจสอบ API_URL
        # ----------------------------------

        if not API_URL:

            error = (
                "ไม่พบ API_URL "
                "กรุณาตั้งค่า API_URL ใน Render "
                "หรือในเครื่องของคุณ"
            )

            return render_template(
                "index.html",
                results=None,
                error=error,
                image_base64=None
            )


        try:

            # ----------------------------------
            # อ่านไฟล์รูป
            # ----------------------------------

            image_data = image.read()


            # ----------------------------------
            # แปลงรูปเป็น Base64
            # เพื่อแสดงรูปเดิมหลังตรวจจับ
            # ----------------------------------

            image_base64 = base64.b64encode(
                image_data
            ).decode("utf-8")


            # ----------------------------------
            # ส่งรูปไป Roboflow
            # ----------------------------------

            response = requests.post(

                API_URL,

                files={
                    "file": (
                        image.filename,
                        image_data,
                        image.content_type
                    )
                },

                timeout=60
            )


            # ----------------------------------
            # แสดงข้อมูลใน Render Logs
            # ----------------------------------

            print(
                "Roboflow Status:",
                response.status_code
            )

            print(
                "Roboflow Response:",
                response.text
            )


            # ----------------------------------
            # ตรวจสอบ Response
            # ----------------------------------

            if response.status_code != 200:

                error = (
                    f"Roboflow Error "
                    f"{response.status_code}: "
                    f"{response.text}"
                )

                return render_template(
                    "index.html",
                    results=None,
                    error=error,
                    image_base64=image_base64
                )


            # ----------------------------------
            # แปลงเป็น JSON
            # ----------------------------------

            data = response.json()


            # ----------------------------------
            # ตรวจสอบ predictions
            # ----------------------------------

            predictions = data.get(
                "predictions",
                []
            )


            if len(predictions) == 0:

                error = (
                    "ไม่พบดอกไม้ที่ AI รู้จัก "
                    "ในรูปภาพ"
                )

                return render_template(
                    "index.html",
                    results=None,
                    error=error,
                    image_base64=image_base64
                )


            # ==================================
            # เก็บผลการตรวจจับทุกดอก
            # ==================================

            results = []


            for prediction in predictions:

                # ------------------------------
                # ชื่อดอกไม้
                # ------------------------------

                flower_name = prediction.get(
                    "class",
                    "unknown"
                )


                # ------------------------------
                # Confidence
                # ------------------------------

                confidence = round(
                    prediction.get(
                        "confidence",
                        0
                    ) * 100,
                    2
                )


                # ------------------------------
                # ตำแหน่งกรอบ
                # Roboflow ส่งเป็น center x,y
                # ------------------------------

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


                # ------------------------------
                # ถ้ามีข้อมูลดอกไม้
                # ------------------------------

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


                # ------------------------------
                # ถ้ายังไม่มีข้อมูลดอกไม้
                # ------------------------------

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


        except requests.exceptions.RequestException as e:

            print(
                "Request Error:",
                str(e)
            )

            error = (
                "ไม่สามารถเชื่อมต่อ Roboflow ได้: "
                + str(e)
            )


        except ValueError as e:

            print(
                "JSON Error:",
                str(e)
            )

            error = (
                "Roboflow ส่งข้อมูลกลับมาไม่ถูกต้อง: "
                + str(e)
            )


        except Exception as e:

            print(
                "Error:",
                str(e)
            )

            error = (
                "เกิดข้อผิดพลาด: "
                + str(e)
            )


    # ==========================================
    # ส่งข้อมูลไป index.html
    # ==========================================

    return render_template(

        "index.html",

        results=results,

        error=error,

        image_base64=image_base64

    )


# ==========================================
# 6. เริ่ม Flask
# ==========================================

if __name__ == "__main__":

    port = int(
        os.environ.get(
            "PORT",
            5000
        )
    )

    app.run(
        host="0.0.0.0",
        port=port,
        debug=True
    )
