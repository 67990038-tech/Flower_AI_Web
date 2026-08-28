from flask import Flask, render_template, request
import requests
import base64
import os

app = Flask(__name__)

API_URL = os.environ.get("API_URL")


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
        "meaning": "ความบริสุทธิ์ ความรัก และความหวัง",
        "opportunity": "งานแต่งงาน วันเกิด วันครบรอบ และการตกแต่งสถานที่"
    },

    "lotus": {
        "thai": "บัว",
        "meaning": "ความบริสุทธิ์ ความสำเร็จ และปัญญา",
        "opportunity": "พิธีกรรมทางศาสนา การบูชาพระ และวัฒนธรรมไทย"
    },

    "orchids": {
        "thai": "กล้วยไม้",
        "meaning": "ความมั่งคั่ง ความสง่างาม และความรักที่มั่นคง",
        "opportunity": "แสดงความยินดี ให้เป็นของขวัญ หรือแสดงความเคารพ"
    },

    "peony": {
        "thai": "โบตั๋น",
        "meaning": "ความรัก ความโรแมนติก และความสุข",
        "opportunity": "การอวยพรให้มั่งคั่ง โชคดี และมีเกียรติยศ"
    },

    "pinkrose": {
        "thai": "กุหลาบสีชมพู",
        "meaning": "ความสง่างาม ความอ่อนโยน และความรัก",
        "opportunity": "วันเกิด วันครบรอบ วันแม่ หรือแสดงความขอบคุณ"
    },

    "redrose": {
        "thai": "กุหลาบแดง",
        "meaning": "ความรักและความรู้สึกที่ดี",
        "opportunity": "วันวาเลนไทน์ วันครบรอบ หรือโอกาสพิเศษ"
    },

    "whiterose": {
        "thai": "กุหลาบขาว",
        "meaning": "ความรักที่บริสุทธิ์และอ่อนโยน",
        "opportunity": "งานแต่งงาน วันครบรอบ และการแสดงความยินดี"
    },

    "sunflower": {
        "thai": "ทานตะวัน",
        "meaning": "ความสดใส ความหวัง และความมั่นคง",
        "opportunity": "แสดงความยินดี ให้กำลังใจ วันเกิด และวันครบรอบ"
    },

    "tulip": {
        "thai": "ทิวลิป",
        "meaning": "ความรักที่สมบูรณ์และมั่นคง",
        "opportunity": "บอกรัก วันเกิด วันครบรอบ และแสดงความยินดี"
    }
}


@app.route("/", methods=["GET", "POST"])
def home():

    results = None
    error = None
    image_data = None
    predictions = []

    if request.method == "POST":

        if "image" not in request.files:

            error = "ไม่พบรูปภาพ"

            return render_template(
                "index.html",
                results=None,
                error=error,
                image_data=None,
                predictions=[]
            )

        image = request.files["image"]

        if image.filename == "":

            error = "กรุณาเลือกรูปภาพ"

            return render_template(
                "index.html",
                results=None,
                error=error,
                image_data=None,
                predictions=[]
            )

        if not API_URL:

            error = "ยังไม่ได้ตั้งค่า API_URL ใน Render"

            return render_template(
                "index.html",
                results=None,
                error=error,
                image_data=None,
                predictions=[]
            )

        try:

            # ==========================================
            # อ่านรูปภาพ
            # ==========================================

            image_bytes = image.read()

            # เก็บรูปไว้ส่งกลับไปแสดงบนหน้าเว็บ
            image_base64 = base64.b64encode(
                image_bytes
            ).decode("utf-8")

            image_data = (
                "data:"
                + (image.content_type or "image/jpeg")
                + ";base64,"
                + image_base64
            )


            # ==========================================
            # ส่งรูปไป Roboflow
            # ==========================================

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


            print(
                "Roboflow Status:",
                response.status_code
            )

            print(
                "Roboflow Response:",
                response.text
            )


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
                    image_data=image_data,
                    predictions=[]
                )


            # ==========================================
            # อ่าน JSON จาก Roboflow
            # ==========================================

            data = response.json()


            if (
                "predictions" not in data
                or len(data["predictions"]) == 0
            ):

                error = (
                    "ไม่พบดอกไม้ที่ AI รู้จักในรูปภาพ"
                )

                return render_template(
                    "index.html",
                    results=None,
                    error=error,
                    image_data=image_data,
                    predictions=[]
                )


            # ==========================================
            # เก็บข้อมูล Bounding Box
            # ==========================================

            predictions = data["predictions"]


            # ==========================================
            # สร้างผลลัพธ์
            # ==========================================

            results = []

            for prediction in predictions:

                flower_name = prediction["class"]

                confidence = round(
                    prediction["confidence"] * 100,
                    2
                )


                if flower_name in flowers:

                    info = flowers[flower_name]

                    results.append({

                        "class": flower_name,

                        "confidence": confidence,

                        "thai": info["thai"],

                        "meaning": info["meaning"],

                        "opportunity":
                            info["opportunity"]

                    })

                else:

                    results.append({

                        "class": flower_name,

                        "confidence": confidence,

                        "thai": "ยังไม่มีข้อมูล",

                        "meaning": "ยังไม่มีข้อมูล",

                        "opportunity": "ยังไม่มีข้อมูล"

                    })


        except Exception as e:

            print("Error:", str(e))

            error = (
                f"เกิดข้อผิดพลาด: {str(e)}"
            )


    return render_template(

        "index.html",

        results=results,

        error=error,

        image_data=image_data,

        predictions=predictions

    )


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
