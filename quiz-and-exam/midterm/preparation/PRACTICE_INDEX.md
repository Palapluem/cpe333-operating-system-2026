# ดัชนีข้อสอบกลางภาคและไฟล์ที่ซ้ำกัน

เลขหน้าเป็นลำดับใน PDF เริ่มจาก 1 คำว่า “ซ้ำ” ในที่นี้หมายถึงเนื้อหาโจทย์ซ้อนกัน ไม่ได้หมายความว่า binary file เหมือนกันทุก byte หรือเฉลยตรงกัน

## ไฟล์ทั้ง 10 ชุด

| รหัส | ไฟล์ | หน้า | ใช้ทำอะไร |
| --- | --- | ---: | --- |
| QZ | [Quiz_BeforeMidterm.pdf](../Quiz_BeforeMidterm.pdf) | 4 | ชุดเริ่มฝึก scheduling และ first/best/worst fit; มีลายมือคำตอบ |
| Y22 | [5DA7634AB1F29EA1C22F8E549A5A7B1C3DCF08A5_OS-Midterm-2022---p2-1.pdf](../5DA7634AB1F29EA1C22F8E549A5A7B1C3DCF08A5_OS-Midterm-2022---p2-1.pdf) | 9 | หน้า 1 scheduling, หน้า 2 replacement/EAT; หน้าหลังมี screenshots และสรุปปรนัย |
| Y22-S | [OS-Midterm-2022-p2-1.pdf](../OS-Midterm-2022-p2-1.pdf) | 1 | โจทย์ scheduling เดียวกับ Y22 หน้า 1 แต่คนละสำเนาพร้อมคำตอบกำกับ; ใช้เพียงชุดเดียวในรอบแรก |
| Y18-A | [20181029161937_CPE_326_Operating_System_1_ต.ค.2561.pdf](../20181029161937_CPE_326_Operating_System_1_ต.ค.2561.pdf) | 9 | หน้า 1-5 ข้อสอบปี 2018 และหน้าหลังเป็นการทำ/จดคำตอบ |
| Y18-B | [20181029161937_CPE_326_Operating_System_2561.pdf](../20181029161937_CPE_326_Operating_System_2561.pdf) | 9 | หน้า 1-5 เป็นโจทย์เดียวกับ Y18-A; ส่วนท้ายมีแบบฝึกและเฉลยเพิ่มต่างจากอีกสำเนา |
| Y15-A | [20150728113955_CPE_334_Operating_Systems_23_ก.พ.2558 (1).pdf](<../20150728113955_CPE_334_Operating_Systems_23_ก.พ.2558 (1).pdf>) | 9 | โจทย์ปี 2015 พร้อม annotation บางส่วน; MLFQ, context switch และ memory essays |
| Y15-B | [20150728113955_CPE_334_Operating_Systems_23_ก.พ.2558.pdf](../20150728113955_CPE_334_Operating_Systems_23_ก.พ.2558.pdf) | 11 | ข้อสอบเดียวกับ Y15-A แต่คำตอบ/การจัดหน้าต่างกัน; ตอนท้ายมีวิธีทำเพิ่ม |
| MC-A | [os midterm exam.pdf](<../os midterm exam.pdf>) | 16 | screenshots ปรนัย 51 ข้อ ครอบคลุมแนวคิด process/scheduling/memory; คำตอบไฮไลต์ต้องตรวจ |
| MC-B | [Backroom.pdf](../Backroom.pdf) | 31 | หน้า 1-16 ซ้อนกับ MC-A; หน้า 17-26 เป็นอีกชุด 32 ข้อ; หน้า 27-31 เป็น screenshots เสริม |
| WR | [ยำรวมมิตรข้อเขียน.pdf](../ยำรวมมิตรข้อเขียน.pdf) | 17 | รวมข้อเขียนและคำตอบหลายแหล่ง; หน้า 1-3 ปนหัวข้อนอก Lecture 1-6 |

## เปิดตามบท

| บท | แหล่งและหน้าที่เลือก | คำถามที่ควรโฟกัส |
| --- | --- | --- |
| L1 | MC-A หน้า 1-2; WR หน้า 1 | MC-A ข้อ 1-3, 5; WR ข้อ 2, 5, 7 |
| L2 | Y15-A หน้า 3, 7; WR หน้า 1-3 | Y15-A ข้อ 5-7 และ III(a); WR ข้อ 6, 8-10, 13, 15, 18, 20 |
| L3 | QZ หน้า 1, 3; Y22-S หน้า 1; Y15-A หน้า 6 | Gantt/metrics; MLFQ แบบธนาคาร |
| L4 | QZ หน้า 2, 4; WR หน้า 11 | holes/placement; internal กับ external fragmentation |
| L5 | WR หน้า 7, 12-14 | address bits, page table/inverted, segmentation และ bounds |
| L6 | Y22 หน้า 2; WR หน้า 8, 15-17 | FIFO/LRU/OPT, page size, EAT และแก้ page-fault inequality |

หน้าที่ปนหลายบทถูกนำเข้าแฟ้มได้มากกว่าหนึ่งบท เพื่อให้เปิดใช้งานแฟ้มเดียวได้ครบ ให้ทำเฉพาะคำถามที่ระบุ ไม่จำเป็นต้องทำทุกข้อบนหน้านั้น

## จุดสำคัญในแต่ละชุด

### QZ: ชุดเริ่มต้น

- หน้า 1: jobs มาพร้อมกัน, run times 10, 1, 2, 2, 5; q=1; ฝึก FIFO/SJF/RR และ turnaround
- หน้า 2: 512 KB, OS 64 KB; process sizes 64, 128, 32, 16 KB; หา holes และจัด E=30 KB
- หน้า 3: jobs 10, 29, 3, 7, 12; q=10; ฝึก waiting time
- หน้า 4: holes อีกชุด โดย process sizes เปลี่ยนเป็น 80, 64, 32, 96 KB

### Y22 และ Y22-S

- โจทย์ scheduling: arrival 0, 2, 3, 4, 6 และ burst 6, 3, 1, 4, 2
- Y22 หน้า 1 กับ Y22-S ทั้งไฟล์เป็นโจทย์เดียวกัน แต่คำตอบจดเพิ่มอาจต่างกัน
- Y22 หน้า 2 เป็น reference string ที่ขึ้นต้น 7,0,1,3,... ใช้ 3 frames ไม่ใช่ string คลาสสิกที่ขึ้นต้น 7,0,1,2,...
- Y22 หน้า 3-6 เป็น screenshot; หน้า 7-9 พิมพ์ปรนัย 40 ข้อ ซึ่งทับกับ MC-A/MC-B จึงไม่ต้องนับเป็นอีก 40 โจทย์ใหม่

### Y18-A และ Y18-B

- หน้า 2 ข้อ 1-3 scheduling; ข้อ 4-5 process
- หน้า 3 ข้อ 6-7 process API; ข้อ 8-10 มี threads ปน
- หน้า 4 ข้อ 12-14 process; ข้อ 11,15 เป็น threads
- หน้า 5 ข้อ 1 MLFQ; ข้อ 2 fragmentation; ข้อ 3 page table/inverted; ข้อ 4 address bits; ข้อ 5 segmentation; ข้อ 6 page size; ข้อ 7 LRU/EAT
- Y18-B หน้า 7-9 มีแบบฝึก address bits, replacement และ scheduling เพิ่ม ไม่ควรถือว่าเป็นเฉลยตรงข้อ 4-7 ของหน้า 5 ทุกหน้า

### Y15-A และ Y15-B

- Y15-A หน้า 2-5 กับ Y15-B หน้า 2-5 เป็นปรนัยชุดเดียวกัน ส่วน annotations ไม่เหมือนกัน
- หน้า 6 MLFQ แบบธนาคาร
- หน้า 7 III(a) context switching อยู่ใน L2; III(b) user-level thread switching เกินขอบเขตที่กำลังเตรียม
- Y15-A หน้า 8-9 เป็น memory/VM และข้อเขียนเชื่อมการจัดการ memory; Y15-B จัดคำตอบ/ส่วนท้ายเพิ่มจนเป็น 11 หน้า
- ค่า logical addresses และรูปแบบการแยก segment ให้ใช้ของแต่ละโจทย์ อย่าคัดตัวเลขจากปี 2018 มาทับ

### MC-A และ MC-B

- MC-A หน้า 1-16 เป็นชุดปรนัย 51 ข้อ; MC-B หน้า 1-16 มีโจทย์เดียวกันจำนวนมากและคำตอบไฮไลต์ต่างกันบางจุด
- MC-B หน้า 17-26 เป็นชุดปรนัยอีก 32 ข้อที่มีหัวข้อซ้อนอยู่มาก เหมาะใช้ตรวจความเข้าใจเพิ่มหลังรอบแรก
- MC-B หน้า 27-31 เป็น screenshots เสริมขนาดเล็ก ไม่ใช้เป็นชุดจำลองสอบใหม่
- ตัวอย่างข้อที่ควรตรวจเป็นพิเศษ: Ready→Blocked, fixed partition/internal fragmentation, timer ใน non-preemptive/cooperative และ zombie/orphan

### WR: รวมข้อเขียน

- หน้า 1-3: ใช้เฉพาะแนวคิด OS/process ที่ระบุไว้; ข้อ 11-12,14,16-17,21-22 เกี่ยวกับ concurrency/threads/semaphore/deadlock ซึ่งอยู่นอกขอบเขตครั้งนี้
- หน้า 4-5 scheduling อีกชุด (ต่างจาก QZ หน้า 1 และ Y22); หน้า 6 MLFQ
- หน้า 7 address bits; หน้า 8-9 replacement พร้อมการจดคำตอบหลายสี
- หน้า 10 MLFQ; หน้า 11 fragmentation; หน้า 12 page tables; หน้า 13 address fields; หน้า 14 segmentation
- หน้า 15 page-size discussion; หน้า 16-17 LRU และ EAT
- ระวังหน้า 8 โจทย์พิมพ์ 5 frames ขณะที่หน้าคำตอบใกล้กันอาจเป็นคนละจำนวน frames; อ่านโจทย์ก่อนทุกครั้ง

## แหล่งอ่านหลัก

- [StudyNotes ทั้งเล่ม](../../../lectures/CPE333_OS_Midterm_StudyNotes.pdf)
- [Lecture 1](../../../lectures/Lecture1_IntroductionToOS.pdf)
- [Lecture 2](../../../lectures/Lecture2_ProcessAndProcessAPIs.pdf)
- [Lecture 3](../../../lectures/Lecture3_Scheduling.pdf)
- [Lecture 4](../../../lectures/Lecture4_MemoryConceptAndContiguousMemoryAllocation.pdf)
- [Lecture 5](../../../lectures/Lecture5_NoncontiguousMemoryAllocation.pdf)
- [Lecture 6](../../../lectures/Lecture6_VirtualMemory.pdf)

คำแนะนำทั้งหมดอาศัยไฟล์เหล่านี้ ไม่ได้ตรวจประกาศรูปแบบสอบล่าสุดจากระบบชั้นเรียน
