# RealorCake
A repository of a cake decoration game called 'Namkhing's Cake'


**v1.0.0**
- deploy by pyinstaller, you can download dist to play the game without downloading the source code: https://tuipied.sharepoint.com/:u:/s/RealorCake/EWhcXWpK8QRCmw5VWEAqtRQBtowLSEwgm-9m9ZIpbb8Dbg?e=jjtoyu (อัพลง github ไม่ได้เพราะเกิน 25MB)
- แก้การ save image ให้เซฟบน Downloads
- แก้ path ให้รองรับ absolute path เพื่อให้ deploy ได้และเปิดแอปฯแล้วเล่นได้ทุกระบบปฎิบัติการ

<br>

**v1.0.1**
- installer: https://tuipied.sharepoint.com/:u:/s/RealorCake/EUrIVryXuMZFmurHLIhFIX4BxIzN2Xedg_RPbSLcwEqruQ?e=nZESSr
- แก้ decoration page ซึ่งมีรายละเอียดดังนี้:
    1. แก้ไม่ให้มีปุ่ม remove ใน color palette ของ base cake และเพิ่มให้มี default base cake เป็น plain milk เพื่อแก้ไขปัญหาที่เพิ่มครีมและท็อปปิงโดยไม่มี base cake ได้ เนื่องจากมันไม่สมเหตุสมผลจึงสร้างให้เปิดมาก็มีเค้กเลยและลบไม่ได้ด้วย
    2. แก้ปุ่ม reset ให้กดง่ายกว่าเดิม จากเดิมที่ต้องกดปุ่มสีก่อนแล้วค่อยกดท็อปปิง ตอนนี้สามารถกดท็อปปิงแล้วเปลี่ยนในทันทีได้แล้ว โดยรายละเอียดเพิ่มเติมคือเมื่อ reset จะเป็น plain milk base cake จากเดิมที่ reset แล้วว่าง เนื่องจากจะไม่ให้ขัดกับข้อ 1
    3. กดปิดด้วยปุ่มปิดของหน้าต่าง (ปุ่ม X) ได้ทุกหน้าแล้ว แก้ได้แบบงงๆ ตอนแก้ข้อ 1 และ 2
    4. แก้ให้ตำแหน่งครีมกลาง (middlecream) ทุกอันให้ตรงกับ thumbnail
    5. แก้เรื่องกดปุ่มยากส่วนหนึ่งแล้ว คือ thumbnail สามารถกดได้ครั้งเดียวแล้วไป แต่รอเสียงเอฟเฟคนิดนุง ส่วนปุ่มอื่นไม่รู้ว่าดีขึ้นไหม แต่ได้อยู่(มั้ง)
    6. แก้ปุ่ม element ให้ชัดกว่าเดิม
 - แก้การเซฟรูปภาพ จากเดิมที่บันทึกลง directory ชื่อ Screenshots ที่สร้างขึ้นมา เปลี่ยนเป็นบันทึกรูปลง directory ที่ชื่อ Downloads ของเครื่องนั้น ๆ

<br>

**v1.1.0**
- แก้มีรายละเอียดดังนี้:
    1. ทำหน้า optionPage ทำ normal mode/random mode ด้วย ใช้ State เดิมแต่แยก Logic ด้วย Flag ใส่รับค่าเลือก mode ไหน ไปหน้าไหน normal ข้าม random, จับเวลา, นับคะแนน
    2. เปลี่ยนไฟล์ state โค้ดเยอะ แยก class เป็นแต่ละไฟล์ไปเลย
    3. แก้ปัญหา mouse over ละกดเลือกเอง เป็น mouse button down
    4. แก้ไขคลาส SaveImgButton เปลี่ยนชื่อไฟล์เป็น pattern dateTime เซฟรูปภาพในโฟลเดอร์ Downloads/RealorCakeGallery ถ้าไม่มีก็สร้างโฟลเดอร์ขึ้นมาให้เอง เพื่อการแสดงผลหน้า gallery
    5. ทำหน้า galleryPage ใช้ dateTime sort เรียงจากใหม่ไปเก่า ใช้ปุ่มเปลี่ยนหน้าซ้ายขวา แสดงแบบ 2x3 กดรูปเพื่อดูได้ 
    6. เปลี่ยนการเซฟรูปใหม่เพื่อแสดงผลขนาดเท่ากัน จัด content layer เพื่อเซฟเฉพาะหน้าเกมทั้งหน้าไม่รวมปุ่ม กระทบหน้า message ต้องจัดแบ่งส่วนวาด content layer แล้วกล่องข้อความบังเค้ก แก้ไขให้พื้นข้อความโปร่งใส + กรอบข้อความโปร่งใส
    7. แก้ไขการแสดงส่วน message ให้มี cursor รู้ว่าพิมพ์ถึงไหนแล้ว เจอปัญหาการพิมเบิ้ล กดแช่เพื่อลบไม่ได้ แก้ให้เป็นปกติแล้ว 

<br>

**v2.0.0**
- แก้มีรายละเอียดดังนี้:
    1. ทำ balingPage มี 4 step 
        - 0 Ingredients เลือกวัตถุดิบ drag and drop ลงชาร์ม
        - 1 mix it กด blender animation รวมส้วนผสม
        - 2 cutting drag and drop knife animation ตัด
        - 3 frosting กด piping bag เลือกไส้เค้ก filling
    2. แก้ปัญหาเพิ่มการนับคะแนนส่วนของ filling
    3. ใส่ sound
    4. แก้ปัญหาปุ่มกดต่าง ๆ เปลี่ยนหน้า next back wish/remove กดไปกลับไม่ได้ กดเลยหน้า กดช้า ปุ่ม object ตกขอบ
    
<br>

<hr>

**How to pyinstaller**
- ทำใน terminal
1. เข้าใน directory ที่มี main.py
2. พิมพ์คำสั่ง pyinstaller --onefile --noconsole --add-data "assets:assets" --exclude Screenshots --name "NamkhingsCake-1.0.1" main.py
3. จะมี directory ชื่อ dist ที่มีไฟล์ .exe หรือไม่ก็ .app (for macOS) ขึ้นมา ให้ zip dist แล้วอัพโหลดลงไดร์ฟได้เลย

cd D:\RealOrCake\RealorCake
python -m PyInstaller `
  --onefile `
  --windowed `
  --name NamkhingCake-1.1.0 `
  --add-data "assets;assets" `
  --add-data "states;states" `
  main.py

git status
git branch
git add .
git commit -m ""
git push -u origin v2.0.0
