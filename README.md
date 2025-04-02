# RealorCake
A repository of a cake decoration game called 'Namkhing's Cake'


**v1.0.0**
- deploy by pyinstaller, you can download dist to play the game without downloading the source code: https://tuipied.sharepoint.com/:u:/s/RealorCake/EWhcXWpK8QRCmw5VWEAqtRQBtowLSEwgm-9m9ZIpbb8Dbg?e=jjtoyu (อัพลง github ไม่ได้เพราะเกิน 25MB)
- แก้การ save image ให้เซฟบน Downloads
- แก้ path ให้รองรับ absolute path เพื่อให้ deploy ได้และเปิดแอปฯแล้วเล่นได้ทุกระบบปฎิบัติการ

**v1.0.1**
- แก้ decoration page ซึ่งมีรายละเอียดดังนี้:
    1. แก้ไม่ให้มีปุ่ม remove ใน color palette ของ base cake และเพิ่มให้มี default base cake เป็น plain milk เพื่อแก้ไขปัญหาที่เพิ่มครีมและท็อปปิงโดยไม่มี base cake ได้ เนื่องจากมันไม่สมเหตุสมผลจึงสร้างให้เปิดมาก็มีเค้กเลยและลบไม่ได้ด้วย
    2. แก้ปุ่ม reset ให้กดง่ายกว่าเดิม จากเดิมที่ต้องกดปุ่มสีก่อนแล้วค่อยกดท็อปปิง ตอนนี้สามารถกดท็อปปิงแล้วเปลี่ยนในทันทีได้แล้ว โดยรายละเอียดเพิ่มเติมคือเมื่อ reset จะเป็น plain milk base cake จากเดิมที่ reset แล้วว่าง เนื่องจากจะไม่ให้ขัดกับข้อ 1
    3. กดปิดด้วยปุ่มปิดของหน้าต่าง (ปุ่ม X) ได้ทุกหน้าแล้ว แก้ได้แบบงงๆ ตอนแก้ข้อ 1 และ 2
    4. แก้ให้ตำแหน่งครีมกลาง (middlecream) ทุกอันให้ตรงกับ thumbnail
    5. แก้เรื่องกดปุ่มยากส่วนหนึ่งแล้ว คือ thumbnail สามารถกดได้ครั้งเดียวแล้วไป แต่รอเสียงเอฟเฟคนิดนุง ส่วนปุ่มอื่นไม่รู้ว่าดีขึ้นไหม แต่ได้อยู่(มั้ง)


<hr>

**How to pyinstaller**
ทำใน terminal
1. เข้าใน directory ที่มี main.py
2. พิมพ์คำสั่ง pyinstaller --onefile --noconsole --add-data "assets:assets" --exclude Screenshots --name "NamkhingsCake-1.0.1" main.py
3. จะมี directory ชื่อ dist ที่มีไฟล์ .exe หรือไม่ก็ .app (for macOS) ขึ้นมา ให้ zip dist แล้วอัพโหลดลงไดร์ฟได้เลย
