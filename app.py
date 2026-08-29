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
# 3. Roboflow API
# ==========================================


RF_WORKFLOW_URL = os.environ.get(
    "RF_WORKFLOW_URL"
)

RF_API_KEY = os.environ.get(
    "RF_API_KEY"
)


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
    # ถ้ายังไม่ได้กดตรวจจับ
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
        # ตรวจว่ามีไฟล์หรือไม่
        # ----------------------------------

        if "image" not in request.files:

            error = "ไม่พบรูปภาพ"

            return render_template(
                "index.html",
                results=None,
                error=error,
                image_preview=None
            )


        image = request.files["image"]


        # ----------------------------------
        # ตรวจชื่อไฟล์
        # ----------------------------------

        if image.filename == "":

            error = "กรุณาเลือกรูปภาพ"

            return render_template(
                "index.html",
                results=None,
                error=error,
                image_preview=None
            )


        # ----------------------------------
        # ตรวจ Roboflow
        # ----------------------------------

        if not RF_WORKFLOW_URL:

            error = (
                "ไม่พบ RF_WORKFLOW_URL "
                "กรุณาตั้งค่าใน Render"
            )

            return render_template(
                "index.html",
                results=None,
                error=error,
                image_preview=None
            )


        if not RF_API_KEY:

            error = (
                "ไม่พบ RF_API_KEY "
                "กรุณาตั้งค่าใน Render"
            )

            return render_template(
                "index.html",
                results=None,
                error=error,
                image_preview=None
            )


        # ==================================
        # อ่านรูป
        # ==================================

        image_bytes = image.read()


        # ==================================
        # แสดงรูปเดิมในหน้าเว็บ
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
                f"Bearer {RF_API_KEY}"

        }


        payload = {

            "inputs": {

                "image": {

                    "type": "base64",

                    "value": image_base64

                }

            }

        }


        response = requests.post(

            RF_WORKFLOW_URL,

            headers=headers,

            json=payload,

            timeout=60

        )


        # ==================================
        # Debug ใน Render Logs
        # ==================================

        print(
            "Roboflow Workflow Status:",
            response.status_code
        )

        print(
            "Roboflow Workflow Response:",
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
        # แปลง JSON
        # ==================================

        try:

            data = response.json()

        except Exception:

            error = (
                "Roboflow ไม่ได้ส่งข้อมูล JSON กลับมา"
            )

            return render_template(
                "index.html",
                results=None,
                error=error,
                image_preview=image_preview
            )


        # ==================================
        # อ่าน Predictions จาก Workflow
        # ==================================

        predictions = []


        # ----------------------------------
        # แบบที่ 1
        # predictions อยู่ตรง root
        # ----------------------------------

        if isinstance(data, dict):

            if "predictions" in data:

                predictions = data.get(
                    "predictions",
                    []
                )


        # ----------------------------------
        # แบบที่ 2
        # predictions อยู่ใน outputs
        # ----------------------------------

        if not predictions:

            if isinstance(data, dict):

                outputs = data.get(
                    "outputs"
                )


                if isinstance(outputs, dict):

                    predictions = outputs.get(
                        "predictions",
                        []
                    )


                elif isinstance(outputs, list):

                    for output in outputs:

                        if isinstance(
                            output,
                            dict
                        ):

                            if "predictions" in output:

                                predictions = (
                                    output.get(
                                        "predictions",
                                        []
                                    )
                                )

                                break


        # ----------------------------------
        # แบบที่ 3
        # Workflow คืน list
        # ----------------------------------

        if not predictions:

            if isinstance(data, list):

                if len(data) > 0:

                    first_result = data[0]

                    if isinstance(
                        first_result,
                        dict
                    ):

                        predictions = (
                            first_result.get(
                                "predictions",
                                []
                            )
                        )


        # ==================================
        # ตรวจ Predictions
        # ==================================

        if not predictions:

            print(
                "ไม่พบ predictions จาก Workflow"
            )

            print(
                "ข้อมูลทั้งหมด:",
                data
            )

            error = (
                "ไม่พบดอกไม้ที่ AI รู้จักในรูปภาพ "
                "หรือ Workflow ไม่ได้ส่ง predictions กลับมา"
            )

            return render_template(
                "index.html",
                results=None,
                error=error,
                image_preview=image_preview
            )


        # ==================================
        # สร้างผลลัพธ์
        # ==================================

        results = []


        # ==================================
        # วนทุกดอกที่ตรวจพบ
        # ==================================

        for prediction in predictions:


            # ------------------------------
            # ชื่อ Class
            # ------------------------------

            flower_name = prediction.get(
                "class",
                prediction.get(
                    "class_name",
                    "unknown"
                )
            )


            # ------------------------------
            # Confidence
            # ------------------------------

            confidence = prediction.get(
                "confidence",
                0
            )


            confidence = round(
                confidence * 100,
                2
            )


            # ------------------------------
            # Bounding Box
            # ------------------------------

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
            # ถ้ามีข้อมูลดอกไม้
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


            # ==================================
            # ถ้าไม่มีข้อมูล
            # ==================================

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
        # ส่งกลับหน้าเว็บ
        # ==================================

        return render_template(

            "index.html",

            results=results,

            error=None,

            image_preview=image_preview

        )


    # ======================================
    # Error
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
