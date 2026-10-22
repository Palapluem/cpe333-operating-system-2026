# ชุดเตรียมสอบกลางภาค CPE333: Lecture 1-6

จัดทำวันที่ 22 ตุลาคม 2026 จากสรุปที่มีอยู่ สไลด์ Lecture 1-6 และข้อสอบกลางภาค 10 ไฟล์ในโฟลเดอร์นี้

เริ่มที่ [คู่มืออ่านและฝึกโจทย์ PDF](output/pdf/00_Study_Guide.pdf) หรือ [ฉบับข้อความ](STUDY_GUIDE.md) แล้วเลือกแฟ้มบทที่ต้องการทบทวน ด้านหน้าของแต่ละแฟ้มบอกหน้าสรุปและข้อสอบที่นำมารวมไว้ พร้อมข้อที่ควรทำในหน้าที่ปนหลายหัวข้อ

| แฟ้ม | เนื้อหา | หน้าจาก StudyNotes เดิม |
| --- | --- | --- |
| [01 Introduction](output/pdf/01_Introduction.pdf) | OS, system calls, privilege, virtualization | PDF 6-12 |
| [02 Process and APIs](output/pdf/02_Process_and_APIs.pdf) | process states, PCB, context switch, fork/wait/exec | PDF 13-22 |
| [03 Scheduling](output/pdf/03_Scheduling.pdf) | Gantt chart, metrics, FIFO/SJF/STCF/RR, MLFQ | PDF 23-30 |
| [04 Contiguous Memory](output/pdf/04_Contiguous_Memory.pdf) | base/bounds, fragmentation, first/best/worst fit | PDF 31-38 |
| [05 Address Translation](output/pdf/05_Address_Translation.pdf) | segmentation, paging, address bits, page tables, TLB | PDF 39-47 |
| [06 Virtual Memory](output/pdf/06_Virtual_Memory.pdf) | page fault, FIFO/LRU/OPT, EAT, working set | PDF 48-62 |
| [07 Integrated Review](output/pdf/07_Integrated_Review.pdf) | แผนภาพเชื่อมบท ตารางเปรียบเทียบ และคำถามทบทวน | PDF 63-67 |

เอกสารช่วยฝึก:

- [ดัชนีข้อสอบและชุดที่ซ้ำกัน](PRACTICE_INDEX.md): ระบุครบทั้ง 10 ไฟล์ว่าใช้ทำอะไรและควรเปิดหน้าไหน
- [ตัวอย่างคำนวณที่ตรวจใหม่](CHECKED_DRILLS.md): scheduling, holes, address bits, page replacement และ EAT พร้อมสมมติฐาน
- [แผนที่หน้าของแฟ้มใหม่](PACK_CONTENTS.md): เทียบหน้าในแต่ละแฟ้มกับหน้า PDF ต้นฉบับ

**แนวใช้:** อ่านหนึ่งบท ปิดเอกสารอธิบายจากความจำ ทำโจทย์ของบทนั้น แล้วบันทึกสาเหตุที่ผิด การจัดลำดับเน้นรูปแบบที่พบในไฟล์เก่า ไม่ใช่การยืนยันข้อสอบหรือสัดส่วนคะแนนรอบนี้

เลขหน้าที่อ้างในคู่มือหมายถึง **ลำดับหน้า PDF เริ่มจาก 1** ส่วนเลขพิมพ์ท้ายหน้า StudyNotes เดิมมักน้อยกว่า 1 หน้า หน้าข้อสอบที่ถูกรวมในแฟ้มยังมีคำตอบ/ไฮไลต์ของเดิม ควรปิดส่วนคำตอบระหว่างฝึกและใช้ CHECKED_DRILLS ตรวจตัวอย่างที่มีข้อสงสัย

ไฟล์ต้นฉบับยังอยู่ตำแหน่งเดิม แฟ้ม PDF ใหม่นำหน้าที่เกี่ยวข้องมาจัดกลุ่มและเพิ่มสารบัญ/ที่มา ไม่ได้แก้เนื้อหาหรือรับรองเฉลยเดิมทุกข้อ
