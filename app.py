# ==========================================
# 1. Import
# ==========================================

from flask import Flask, render_template, request
import requests
import os
import base64


# ==========================================
# 2. ตั้งค่า Flask
# ==========================================

app = Flask(__name__)


# ==========================================
# 3. Roboflow Workflow API
# ==========================================


API_URL = os.environ.get("API_URL")
API_KEY = os.environ.get("API_KEY")


# ==========================================
# 4. ข้อมูลดอกไม้
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
# 5. หน้าเว็บไซต์
# ==========================================

@app.route("/", methods=["GET", "POST"])
def home():

    results = None
    error = None
    image_preview = None

    # --------------------------------------
    # GET
    # --------------------------------------

    if request.method == "GET":

        return render_template(
            "index.html",
            results=None,
            error=None,
            image_preview=None
        )

    # ======================================
    # POST
    # ======================================

    try:

        # ----------------------------------
        # ตรวจไฟล์
        # ----------------------------------

        if "image" not in request.files:

            return render_template(
                "index.html",
                results=None,
                error="ไม่พบรูปภาพ",
                image_preview=None
            )

        image = request.files["image"]

        if image.filename == "":

            return render_template(
                "index.html",
                results=None,
                error="กรุณาเลือกรูปภาพ",
                image_preview=None
            )


        # ==================================
        # ตรวจ Environment Variables
        # ==================================

        if not API_URL:

            return render_template(
                "index.html",
                results=None,
                error="ไม่พบ API_URL ใน Render",
                image_preview=None
            )


        if not API_KEY:

            return render_template(
                "index.html",
                results=None,
                error="ไม่พบ API_KEY ใน Render",
                image_preview=None
            )


        # ==================================
        # อ่านรูป
        # ==================================

        image_bytes = image.read()


        # ==================================
        # แสดงรูปที่อัปโหลดค้างไว้
        # ==================================

        image_base64 = base64.b64encode(
            image_bytes
        ).decode("utf-8")

        image_type = (
            image.content_type
            or "image/jpeg"
        )

        image_preview = (
            f"data:{image_type};base64,{image_base64}"
        )


        # ==================================
        # ส่งรูปไป Roboflow Workflow
        # ==================================

        headers = {

            "Content-Type":
                "application/json",

            "Authorization":
                f"Bearer {API_KEY}"

        }


        payload = {

            "inputs": {

                "image": {

                    "type":
                        "base64",

                    "value":
                        image_base64

                }

            }

        }


        response = requests.post(

            API_URL,

            headers=headers,

            json=payload,

            timeout=120

        )


        # ==================================
        # Debug Render Logs
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
        # ตรวจ Status
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
                results=None,
                error=error,
                image_preview=image_preview
            )


        # ==================================
        # JSON
        # ==================================

        try:

            data = response.json()

        except Exception:

            return render_template(
                "index.html",
                results=None,
                error="Roboflow ไม่ได้ส่งข้อมูล JSON กลับมา",
                image_preview=image_preview
            )


        # ==================================
        # DEBUG โครงสร้าง Response
        # ==================================

        print(
            "Roboflow JSON:",
            data
        )


        # ==================================
        # ดึง outputs จาก Workflow
        # ==================================

        outputs = data.get(
            "outputs",
            []
        )


        if not isinstance(outputs, list):

            outputs = [outputs]


        # ==================================
        # ดึง predictions
        # ==================================

        predictions = []


        for output in outputs:

            # ป้องกัน error:
            # 'str' object has no attribute 'get'

            if not isinstance(output, dict):

                continue


            output_predictions = output.get(
                "predictions",
                []
            )


            # ------------------------------
            # predictions เป็น list
            # ------------------------------

            if isinstance(
                output_predictions,
                list
            ):

                predictions.extend(
                    output_predictions
                )


            # ------------------------------
            # predictions เป็น dict
            # ------------------------------

            elif isinstance(
                output_predictions,
                dict
            ):

                # บาง Workflow อาจส่ง
                # predictions เป็น dictionary

                if isinstance(
                    output_predictions.get(
                        "predictions"
                    ),
                    list
                ):

                    predictions.extend(
                        output_predictions[
                            "predictions"
                        ]
                    )

                else:

                    predictions.append(
                        output_predictions
                    )


        # ==================================
        # ถ้า Workflow ส่ง predictions
        # มาในรูปแบบอื่น
        # ==================================

        if not predictions:

            top_predictions = data.get(
                "predictions",
                []
            )

            if isinstance(
                top_predictions,
                list
            ):

                predictions = (
                    top_predictions
                )

            elif isinstance(
                top_predictions,
                dict
            ):

                predictions = [
                    top_predictions
                ]


        # ==================================
        # ตรวจว่ามี Prediction หรือไม่
        # ==================================

        valid_predictions = []


        for prediction in predictions:

            if isinstance(
                prediction,
                dict
            ):

                valid_predictions.append(
                    prediction
                )


        predictions = valid_predictions


        if not predictions:

            return render_template(
                "index.html",
                results=None,
                error=(
                    "ไม่พบดอกไม้ที่ AI รู้จักในรูปภาพ"
                ),
                image_preview=image_preview
            )


        # ==================================
        # สร้างผลลัพธ์
        # ==================================

        results = []


        for prediction in predictions:


            # --------------------------------
            # Class
            # --------------------------------

            flower_name = prediction.get(
                "class",
                prediction.get(
                    "class_name",
                    "unknown"
                )
            )


            # --------------------------------
            # Confidence
            # --------------------------------

            confidence = prediction.get(
                "confidence",
                0
            )


            try:

                confidence = float(
                    confidence
                )

            except:

                confidence = 0


            # Roboflow confidence
            # ปกติเป็น 0-1

            if confidence <= 1:

                confidence = (
                    confidence * 100
                )


            confidence = round(
                confidence,
                2
            )


            # --------------------------------
            # Bounding Box
            # --------------------------------

            x = prediction.get(
                "x",
                0
            )

            y = prediction.get(
                "y",
                0
            )

            width = prediction.get(
                "width",
                0
            )

            height = prediction.get(
                "height",
                0
            )


            # ==================================
            # ข้อมูลดอกไม้
            # ==================================

            if flower_name in flowers:

                info = flowers[
                    flower_name
                ]

                results.append({

                    "class":
                        flower_name,

                    "confidence":
                        confidence,

                    "thai":
                        info["thai"],

                    "meaning":
                        info["meaning"],

                    "opportunity":
                        info["opportunity"],

                    "x":
                        x,

                    "y":
                        y,

                    "width":
                        width,

                    "height":
                        height

                })


            else:

                results.append({

                    "class":
                        flower_name,

                    "confidence":
                        confidence,

                    "thai":
                        "ยังไม่มีข้อมูล",

                    "meaning":
                        "ยังไม่มีข้อมูล",

                    "opportunity":
                        "ยังไม่มีข้อมูล",

                    "x":
                        x,

                    "y":
                        y,

                    "width":
                        width,

                    "height":
                        height

                })


        # ==================================
        # ส่งผลกลับ HTML
        # ==================================

        return render_template(

            "index.html",

            results=results,

            error=None,

            image_preview=image_preview

        )


    # ======================================
    # Request Error
    # ======================================

    except requests.exceptions.RequestException as e:

        print(
            "Request Error:",
            str(e)
        )

        error = (
            "ไม่สามารถเชื่อมต่อ Roboflow ได้: "
            + str(e)
        )


    # ======================================
    # General Error
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
# 6. เริ่ม Flask
# ==========================================

if __name__ == "__main__":

    app.run(

        host="0.0.0.0",

        port=int(
            os.environ.get(
                "PORT",
                5000
            )
        ),

        debug=True

    )
