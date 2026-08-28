from flask import Flask, render_template, request
import requests
import os

app = Flask(__name__)

API_URL = os.environ.get("API_URL")


flowers = {
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
        "meaning": "ความหวัง อิสระ การเริ่มต้นใหม่ และความเข้มแข็ง",
        "opportunity": "การบอกลาเพื่อเริ่มต้นใหม่ การให้กำลังใจ หรือการอวยพร"
    },

    "gardenia": {
        "thai": "พุด",
        "meaning": "ความเจริญรุ่งเรืองและความมั่นคงของชีวิต",
        "opportunity": "บูชาพระ งานแต่งงาน และงานมงคล"
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
        "opportunity": "งานแต่งงาน งานศพ วันเกิด หรือวันครบรอบ"
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
        "meaning": "ความรัก ความโรแมนติก และความสุข",
        "opportunity": "การอวยพรให้มั่งคั่ง โชคดี และมีเกียรติยศ"
    },

    "pinkrose": {
        "thai": "กุหลาบสีชมพู",
        "meaning": "ความสง่างาม ความอ่อนโยน และความรักโรแมนติก",
        "opportunity": "วันเกิด วันครบรอบ วันแม่ หรือแสดงความยินดี"
    },

    "redrose": {
        "thai": "กุหลาบแดง",
        "meaning": "ความรักและการตกหลุมรัก",
        "opportunity": "วันวาเลนไทน์ วันครบรอบ หรือการบอกรัก"
    },

    "whiterose": {
        "thai": "กุหลาบขาว",
        "meaning": "ความรักที่บริสุทธิ์และน่าทะนุถนอม",
        "opportunity": "งานแต่งงาน วันครบรอบ หรือแสดงความยินดี"
    },

    "sunflower": {
        "thai": "ทานตะวัน",
        "meaning": "ความสดใส ความหวัง และความมั่นคง",
        "opportunity": "แสดงความยินดี ให้กำลังใจ วันเกิด หรือวันครบรอบ"
    },

    "tulip": {
        "thai": "ทิวลิป",
        "meaning": "ความรักที่สมบูรณ์และมั่นคง",
        "opportunity": "บอกรัก วันเกิด วันครบรอบ หรือแสดงความยินดี"
    }
}


@app.route("/", methods=["GET", "POST"])
def home():

    results = None
    error = None

    if request.method == "POST":

        if "image" not in request.files:
            error = "ไม่พบรูปภาพ"
            return render_template(
                "index.html",
                results=results,
                error=error
            )

        image = request.files["image"]

        if image.filename == "":
            error = "กรุณาเลือกรูปภาพ"
            return render_template(
                "index.html",
                results=results,
                error=error
            )

        if not API_URL:
            error = "ไม่พบ API_URL กรุณาตั้งค่าใน Render"
            return render_template(
                "index.html",
                results=results,
                error=error
            )

        try:

            # ส่งรูปไป Roboflow
            response = requests.post(
                API_URL,
                files={
                    "file": (
                        image.filename,
                        image.read(),
                        image.content_type
                    )
                }
            )

            print("Roboflow Status Code:", response.status_code)
            print("Roboflow Response:", response.text)

            if response.status_code != 200:
                error = (
                    f"Roboflow Error {response.status_code}: "
                    f"{response.text}"
                )

                return render_template(
                    "index.html",
                    results=results,
                    error=error
                )

            data = response.json()

            # ตรวจสอบ predictions
            predictions = data.get("predictions", [])

            if len(predictions) == 0:
                error = "ไม่พบดอกไม้ที่ AI รู้จักในรูปภาพ"

                return render_template(
                    "index.html",
                    results=None,
                    error=error
                )

            results = []

            # รองรับการตรวจจับหลายดอก
            for prediction in predictions:

                flower_name = prediction.get("class", "unknown")

                confidence = round(
                    prediction.get("confidence", 0) * 100,
                    2
                )

                # ตำแหน่งกรอบ
                x = prediction.get("x", 0)
                y = prediction.get("y", 0)
                width = prediction.get("width", 0)
                height = prediction.get("height", 0)

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

        except Exception as e:

            print("Error:", str(e))

            error = f"เกิดข้อผิดพลาด: {str(e)}"

    return render_template(
        "index.html",
        results=results,
        error=error
    )


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", 5000))
    )
