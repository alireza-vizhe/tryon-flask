# from flask import Flask, request, send_file
# import cv2
# import numpy as np
# import io

# app = Flask(__name__)

# def clean_watermark(image_bytes):
#     # 1. Tabdil bytes be format OpenCV
#     nparr = np.frombuffer(image_bytes, np.uint8)
#     img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

#     # 2. Tashkhis Watermark (Logic: Masking)
#     # Ma inja peyda mikonim kodom pixel-ha kheli sefid hastan (Watermark)
#     # Range: (240, 240, 240) ta (255, 255, 255) --> Ranghaye nazdik be sefid
#     lower_white = np.array([240, 240, 240])
#     upper_white = np.array([255, 255, 255])
#     mask = cv2.inRange(img, lower_white, upper_white)

#     # 3. Kami mask ro bozorg mikonim ta lakk-haye sefid baghi namone (Dilation)
#     kernel = np.ones((3, 3), np.uint8)
#     mask_dilated = cv2.dilate(mask, kernel, iterations=1)

#     # 4. Hazf Watermark (Inpainting - Telea Algorithm)
#     # In dastor pixel-haye mask shode ro ba range-haye atraf por mikone
#     result = cv2.inpaint(img, mask_dilated, 3, cv2.INPAINT_TELEA)

#     # 5. Tabdil natije baraye ersal
#     is_success, buffer = cv2.imencode(".jpg", result)
#     io_buf = io.BytesIO(buffer)
#     io_buf.seek(0)
#     return io_buf

# @app.route('/process', methods=['POST'])
# def process_image():
#     if 'file' not in request.files:
#         return {"error": "No file provided"}, 400
    
#     file = request.files['file']
    
#     try:
#         processed_image = clean_watermark(file.read())
#         return send_file(processed_image, mimetype='image/jpeg')
#     except Exception as e:
#         print(f"Error: {e}")
#         return {"error": "Processing failed"}, 500

# if __name__ == '__main__':
#     # Run on port 5000
#     app.run(port=5000, debug=True)





# from flask import Flask, request, send_file
# import cv2
# import numpy as np
# import io

# app = Flask(__name__)

# def clean_watermark(image_bytes):
#     # 1. تبدیل بایت به عکس
#     nparr = np.frombuffer(image_bytes, np.uint8)
#     img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
#     # تبدیل به خاکستری برای پردازش دقیق‌تر
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#     # --- مرحله ساخت ماسک هوشمند ---
    
#     # الف) پیدا کردن رنگ‌های خیلی روشن (سفید)
#     # هر پیکسلی که روشنایی‌اش بیشتر از 200 باشد
#     _, mask_white = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)

#     # ب) پیدا کردن رنگ‌های خیلی تیره (مشکی)
#     # هر پیکسلی که روشنایی‌اش کمتر از 50 باشد
#     _, mask_black = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY_INV)

#     # ج) ترکیب ماسک‌ها (سفید یا مشکی)
#     mask = cv2.bitwise_or(mask_white, mask_black)

#     # د) ضخیم کردن ماسک (Dilation)
#     # این کار باعث می‌شود کل ضخامت لوگو پوشش داده شود نه فقط خط‌های نازک
#     # اگر لوگو هنوز کامل پاک نشد، عدد (5, 5) را به (7, 7) تغییر دهید
#     kernel = np.ones((5, 5), np.uint8) 
#     mask_dilated = cv2.dilate(mask, kernel, iterations=2)

#     # --- مرحله حذف (Inpainting) ---
    
#     # استفاده از روش Navier-Stokes (معمولاً برای بازسازی بافت‌ها طبیعی‌تر عمل می‌کند)
#     result = cv2.inpaint(img, mask_dilated, 3, cv2.INPAINT_NS)

#     # تبدیل نتیجه به فرمت قابل ارسال
#     is_success, buffer = cv2.imencode(".jpg", result)
#     io_buf = io.BytesIO(buffer)
#     io_buf.seek(0)
#     return io_buf

# @app.route('/process', methods=['POST'])
# def process_image():
#     if 'file' not in request.files:
#         return {"error": "No file provided"}, 400
    
#     file = request.files['file']
    
#     try:
#         processed_image = clean_watermark(file.read())
#         return send_file(processed_image, mimetype='image/jpeg')
#     except Exception as e:
#         print(f"Error: {e}")
#         return {"error": "Processing failed"}, 500

# if __name__ == '__main__':
#     app.run(port=5000, debug=True)












# from flask import Flask, request, send_file
# import cv2
# import numpy as np
# import io

# app = Flask(__name__)

# # تابعی که مختصات را مستقیماً دریافت می‌کند
# def clean_specified_area(image_bytes, x, y, w, h):
#     # 1. تبدیل بایت به عکس
#     nparr = np.frombuffer(image_bytes, np.uint8)
#     img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
#     # گرفتن ابعاد عکس اصلی
#     img_height, img_width = img.shape[:2]

#     # 2. ساخت ماسک (Mask) بر اساس مختصات
#     mask = np.zeros(img.shape[:2], dtype="uint8")
    
#     # *نکته مهم*: مختصات y باید از پایین تصویر محاسبه شود.
#     # اگر y نقطه پایین را نشان دهد:
#     # نقطه شروع Y (بالای واترمارک) = (ارتفاع کل عکس) - (موقعیت Y از پایین) - (ارتفاع واترمارک)
    
#     # اینجا فرض می‌کنیم مختصات ارسالی (x, y) نقطه گوشه بالا سمت چپ ناحیه واترمارک است.
#     # (اگر از پایین محاسبه می‌کنید، باید در Node.js محاسبات را انجام دهیم.)
    
#     # برای اطمینان از اینکه واترمارک در تصویر است، مختصات را چک می‌کنیم
#     x_start = max(0, x)
#     y_start = max(0, y)
#     x_end = min(img_width, x + w)
#     y_end = min(img_height, y + h)

#     # ناحیه مربوط به واترمارک را در ماسک سفید می‌کنیم (255)
#     mask[y_start:y_end, x_start:x_end] = 255
    
#     # 3. حذف ناحیه ماسک شده (Inpainting)
#     # 3 یک پارامتر برای شعاع منطقه در نظر گرفته شده در فرآیند inpainting است.
#     result = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)

#     # 4. تبدیل نتیجه به فرمت قابل ارسال
#     is_success, buffer = cv2.imencode(".jpg", result)
#     io_buf = io.BytesIO(buffer)
#     io_buf.seek(0)
#     return io_buf

# @app.route('/process', methods=['POST'])
# def process_image():
#     if 'file' not in request.files:
#         return {"error": "No file provided"}, 400
    
#     file = request.files['file']
    
#     # دریافت مختصات از فرم Node.js
#     try:
#         x = int(request.form.get('x', 0))
#         y = int(request.form.get('y', 0))
#         w = int(request.form.get('width', 0))
#         h = int(request.form.get('height', 0))
#     except (ValueError, TypeError):
#         return {"error": "Invalid coordinates provided"}, 400

#     if w == 0 or h == 0:
#          return {"error": "Width or height cannot be zero"}, 400

#     try:
#         processed_image = clean_specified_area(file.read(), x, y, w, h)
#         return send_file(processed_image, mimetype='image/jpeg')
#     except Exception as e:
#         print(f"Processing Error: {e}")
#         return {"error": "Processing failed"}, 500

# if __name__ == '__main__':
#     app.run(port=5000, debug=True)





# from flask import Flask, request, send_file
# import cv2
# import numpy as np
# import io

# app = Flask(__name__)

# # مختصات ثابت پدینگ و ابعاد واترمارک
# # توجه: اینها همان مقادیری هستند که از Node.js ارسال می‌شوند
# WATERMARK_WIDTH = 300
# WATERMARK_HEIGHT = 100
# PADDING_X = 10  # فاصله از چپ
# PADDING_Y = 10  # فاصله از پایین

# def clean_specified_area(image_bytes, x_pad, y_pad, w, h):
#     # 1. تبدیل بایت به عکس
#     nparr = np.frombuffer(image_bytes, np.uint8)
#     img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
#     img_height, img_width = img.shape[:2]

#     # 2. محاسبه مختصات دقیق برای گوشه پایین سمت چپ
    
#     # X شروع: فاصله از چپ (PADDING_X)
#     x_start = x_pad
    
#     # Y شروع (بالای واترمارک) = (ارتفاع کل عکس) - (ارتفاع واترمارک) - (فاصله از پایین)
#     y_start = img_height - h - y_pad
    
#     # X و Y نهایی
#     x_end = min(img_width, x_start + w)
#     y_end = min(img_height, y_start + h)

#     # 3. ساخت ماسک (Mask)
#     mask = np.zeros(img.shape[:2], dtype="uint8")
    
#     # ناحیه ماسک شده (ناحیه حذف) را سفید می‌کنیم
#     mask[y_start:y_end, x_start:x_end] = 255
    
#     # 4. حذف ناحیه ماسک شده (Inpainting)
#     # از الگوریتم Telea استفاده می‌کنیم
#     result = cv2.inpaint(img, mask, 5, cv2.INPAINT_TELEA)

#     # 5. تبدیل نتیجه به فرمت قابل ارسال (JPEG)
#     is_success, buffer = cv2.imencode(".jpg", result)
#     io_buf = io.BytesIO(buffer)
#     io_buf.seek(0)
#     return io_buf

# @app.route('/process', methods=['POST'])
# def process_image():
#     if 'file' not in request.files:
#         return {"error": "No file provided"}, 400
    
#     file = request.files['file']
    
#     # دریافت مختصات ثابت از Node.js
#     try:
#         x_pad = int(request.form.get('x', PADDING_X))
#         y_pad = int(request.form.get('y', PADDING_Y))
#         w = int(request.form.get('width', WATERMARK_WIDTH))
#         h = int(request.form.get('height', WATERMARK_HEIGHT))
#     except (ValueError, TypeError):
#         return {"error": "Invalid coordinates provided"}, 400

#     try:
#         processed_image = clean_specified_area(file.read(), x_pad, y_pad, w, h)
#         return send_file(processed_image, mimetype='image/jpeg')
#     except Exception as e:
#         print(f"Processing Error in Python: {e}")
#         return {"error": "Processing failed in Python"}, 500

# if __name__ == '__main__':
#     # پورت اختصاصی برای سرویس پردازش پایتون
#     app.run(port=5000, debug=True)






from flask import Flask, request, send_file
import cv2
import numpy as np
import io
import os

app = Flask(__name__)

# پیش‌فرض‌ها (اگر ارسال نشد از این‌ها استفاده میشه)
WATERMARK_WIDTH = 300
WATERMARK_HEIGHT = 100
DEFAULT_PADDING_X = 10
DEFAULT_PADDING_Y = 10

def clean_specified_area(image_bytes, x_pad, y_pad, w, h):
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Unable to decode image")
    img_height, img_width = img.shape[:2]

    x_start = max(0, int(x_pad))
    y_start = max(0, img_height - int(h) - int(y_pad))
    x_end = min(img_width, x_start + int(w))
    y_end = min(img_height, y_start + int(h))

    mask = np.zeros(img.shape[:2], dtype="uint8")
    mask[y_start:y_end, x_start:x_end] = 255

    result = cv2.inpaint(img, mask, 5, cv2.INPAINT_TELEA)

    is_success, buffer = cv2.imencode(".jpg", result, [int(cv2.IMWRITE_JPEG_QUALITY), 90])
    if not is_success:
        raise ValueError("Failed to encode result image")
    io_buf = io.BytesIO(buffer)
    io_buf.seek(0)
    return io_buf

@app.route('/process', methods=['POST'])
def process_image():
    if 'file' not in request.files:
        return {"error": "No file provided"}, 400

    file = request.files['file']

    try:
        x_pad = int(request.form.get('x', DEFAULT_PADDING_X))
        y_pad = int(request.form.get('y', DEFAULT_PADDING_Y))
        w = int(request.form.get('width', WATERMARK_WIDTH))
        h = int(request.form.get('height', WATERMARK_HEIGHT))
    except (ValueError, TypeError):
        return {"error": "Invalid coordinates provided"}, 400

    try:
        processed_image = clean_specified_area(file.read(), x_pad, y_pad, w, h)
        return send_file(processed_image, mimetype='image/jpeg')
    except Exception as e:
        print(f"Processing Error in Python: {e}")
        return {"error": "Processing failed in Python", "detail": str(e)}, 500

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
