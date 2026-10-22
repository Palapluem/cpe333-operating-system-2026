# CPE333 Mock Examinations

ข้อสอบฝึกทบทวน Lecture 1–6 ไม่ใช่ข้อสอบจริง ข้อความและช่องลงนามบนปกเป็นแม่แบบ ไม่ใช่การยืนยันการรับรองจริง

- [ข้อสอบกลางภาคพร้อมพิมพ์](midterm/output/pdf/CPE333_Midterm_Mock_Exam.pdf): 12 หน้า รวมปก, 50 คะแนน
- [เฉลยและเกณฑ์ตรวจ](midterm/output/pdf/CPE333_Midterm_Mock_Solutions.pdf)
- `final/`: เตรียมโฟลเดอร์ไว้ ยังไม่มีข้อสอบปลายภาค

ต้นฉบับ LaTeX อยู่ใน `midterm/` แก้โจทย์ที่ `chapters/questions.tex` และเฉลยที่ `solutions/answers.tex` ได้โดยตรง ไม่ต้องใช้ Python หรือ JSON

คอมไพล์ด้วย XeLaTeX สองรอบต่อไฟล์ โดยใช้ jobname ที่ไม่มีช่องว่าง: ปกใน `frontmatter/`, เนื้อหาใน `chapters/`, แล้วประกอบด้วย `CPE333_Midterm Exam_main.tex`; เฉลยใช้ `solutions/CPE333_Midterm_Solutions.tex` หากสร้าง component ใหม่ ให้คงชื่อ PDF ที่มีช่องว่างตามที่ไฟล์หลักอ้างไว้ และนำฉบับใช้งานไปแทนไฟล์ใน `output/pdf/`

คงฟอนต์ โลโก้ และโครงประกอบ PDF ตาม [แม่แบบ CPE222](https://github.com/Palapluem/cpe222-past-exam-main) ข้อสอบเก่าต้นฉบับใน `../midterm/` ไม่ถูกแก้ไข
