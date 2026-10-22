# ตัวอย่างคำนวณที่ตรวจใหม่

ใช้ตรวจหลังทำเอง ตัวเลขในส่วนนี้คำนวณจากข้อมูลโจทย์และกฎที่ระบุ ไม่ใช่เฉลยทางการหรือการรับรองคำตอบที่เขียนอยู่ใน PDF ต้นฉบับทุกข้อ ตาราง replacement เริ่มจาก frames ว่างและนับ cold-start faults

## 1. Quiz หน้า 1: waiting ต่างจาก response

ทุก process มาถึงเวลา 0 ตามลำดับ P1-P5; burst = 10, 1, 2, 2, 5 ms; RR q=1 ms; ไม่คิด switch cost กรณี SJF burst เท่ากันใช้ลำดับเข้าคิว

| Policy | Average waiting | Average turnaround | Average response |
| --- | ---: | ---: | ---: |
| FIFO | 9.8 ms | 13.8 ms | 9.8 ms |
| SJF | 3.8 ms | 7.8 ms | 3.8 ms |
| RR | 6.4 ms | 10.4 ms | 2.0 ms |

ใน RR, first-start ของ P1-P5 คือ 0,1,2,3,4 แต่ completion คือ 20,2,7,8,15 จึงใช้เพียง first-start มาคิด waiting ไม่ได้

## 2. Quiz หน้า 3: quantum เปลี่ยน ผลเปลี่ยน

ทุกงานมาเวลา 0; burst = 10,29,3,7,12 ms; q=10 ms

| Policy | Average waiting | Average turnaround |
| --- | ---: | ---: |
| FCFS | 28.0 ms | 40.2 ms |
| SJF | 13.0 ms | 25.2 ms |
| RR | 23.0 ms | 35.2 ms |

RR timeline: P1(0-10), P2(10-20), P3(20-23), P4(23-30), P5(30-40), P2(40-50), P5(50-52), P2(52-61)

## 3. Scheduling ปี 2022

| Process | Arrival A | CPU burst B |
| --- | ---: | ---: |
| P1 | 0 | 6 |
| P2 | 2 | 3 |
| P3 | 3 | 1 |
| P4 | 4 | 4 |
| P5 | 6 | 2 |

สมมติฐาน: ไม่มี I/O, ไม่มี context-switch overhead; STCF เสมอกันให้ process ปัจจุบันทำต่อ ถ้าไม่มี current ที่เสมอให้เลือก arrival เก่ากว่า; RR q=1 และนำ jobs ที่มาถึงตรงปลาย quantum เข้าคิวก่อน requeue งานที่เพิ่งหมด quantum

| Policy | Average waiting | Average turnaround | Average response |
| --- | ---: | ---: | ---: |
| FCFS | 4.8 | 8.0 | 4.8 |
| STCF | 3.0 | 6.2 | 1.6 |
| RR ตามกฎคิวข้างต้น | 5.6 | 8.8 | 1.0 |

หน่วยเวลาใช้ตามโจทย์ ตารางที่พิมพ์ไม่ได้ระบุหน่วยเฉพาะในหัวคอลัมน์

### ตรวจ FCFS แบบราย process

Timeline: P1(0-6), P2(6-9), P3(9-10), P4(10-14), P5(14-16)

| Process | Completion C | Turnaround C-A | Waiting C-A-B |
| --- | ---: | ---: | ---: |
| P1 | 6 | 6 | 0 |
| P2 | 9 | 7 | 4 |
| P3 | 10 | 7 | 6 |
| P4 | 14 | 10 | 6 |
| P5 | 16 | 10 | 8 |

Average turnaround = (6+7+7+10+10)/5 = 8.0 จึงไม่ใช่ 7.8 ที่จดไว้ในบางไฟล์

### ตรวจ STCF และกรณีเสมอ

Timeline ตามสมมติฐานข้างต้น: P1(0-2), P2(2-3), P3(3-4), P2(4-6), P5(6-8), P1(8-12), P4(12-16)

Waiting ของ P1-P5 = 6,1,0,8,0 รวม 15 จึงเฉลี่ย 3.0 ส่วน response = 0,0,0,8,0 เฉลี่ย 1.6

ที่เวลา 8 P1 และ P4 เหลือ 4 เท่ากัน ถ้าเลือก P4 ก่อน P1 ตาม diagram บางสำเนา จะได้ average response = 0.8 แต่ average waiting ยังคง 3.0 และ average turnaround ยังคง 6.2 ดังนั้น 0.8 ไม่ใช่คำตอบของ average waiting ในทั้งสองลำดับนี้

### ตรวจ RR

Timeline: P1(0-2), P2(2-3), P1(3-4), P3(4-5), P2(5-6), P4(6-7), P1(7-8), P5(8-9), P2(9-10), P4(10-11), P1(11-12), P5(12-13), P4(13-14), P1(14-15), P4(15-16)

P1(0-2) ในบรรทัดนี้รวม quantum ติดกันสองช่วงไว้ เพราะช่วงแรกยังไม่มีงานอื่นรอ ไม่ได้เปลี่ยน q จาก 1 เป็น 2

| Process | Completion | Waiting | Turnaround | Response |
| --- | ---: | ---: | ---: | ---: |
| P1 | 15 | 9 | 15 | 0 |
| P2 | 10 | 5 | 8 | 0 |
| P3 | 5 | 1 | 2 | 1 |
| P4 | 16 | 8 | 12 | 2 |
| P5 | 13 | 5 | 7 | 2 |

ถ้าผู้สอนกำหนดกฎ enqueue ตรงขอบ quantum ต่างกัน RR อาจได้ timeline/metrics ต่างออกไป จึงต้องเขียนกฎคิวก่อนเทียบคำตอบ

## 4. Quiz หน้า 2: memory holes

Memory 512 KB; OS [0,64); A [64,128), B [192,320), C [336,368), D [400,416) ใช้หน่วย KB ทั้งหมด

| Hole | Base | Size |
| --- | ---: | ---: |
| 1 | 128 | 64 |
| 2 | 320 | 16 |
| 3 | 368 | 32 |
| 4 | 416 | 96 |

ขอ 30 KB และค้นตาม base จากน้อยไปมาก: first-fit ได้ base 128 KB; best-fit ได้ 368 KB; worst-fit ได้ 416 KB

Quiz หน้า 4 เปลี่ยน occupied sizes จึงได้ holes (144,48), (256,80), (368,32), (496,16) ผล first/best/worst fit เป็น 144/368/256 KB ตามลำดับ

## 5. Address translation

### Base/bounds

Base=16 KiB, Bounds=4 KiB; VA=420 bytes อยู่ในขอบเขต จึงได้ PA=16384+420=16804 bytes แต่ VA=4200 bytes เกิน 4096 จึง fault ก่อนนำไปบวก base

### Paging

Page=4 KiB, VA=0x12345, page table ให้ VPN=0x12 ไป PFN=7:

- Offset bits = 12
- VPN = 0x12 = 18; offset = 0x345 = 837
- PA = 7×4096+837 = 29509 = 0x7345

### จำนวน bits

140 virtual pages, page 1024 bytes: ต้อง encode VPN 140 ค่า จึงใช้ 8 bits และ offset 10 bits รวมอย่างน้อย 18 bits; physical 64 frames ใช้ PFN 6 bits รวม 16 bits ค่าที่เหลือของ VPN encoding ไม่จำเป็นต้องเป็น valid pages

VA=64 bits, PA=32 bits, page 1024 bytes: VA=[VPN 54 | offset 10], PA=[PFN 22 | offset 10]

### Segmentation จากตัวอย่างในสรุป

VA=4200 อยู่ใน heap ที่ logical start 4096; offset=104 bytes; heap bound=2 KiB และ physical base=34 KiB จึงได้ PA=34816+104=34920 bytes ตัวอย่างนี้ใช้ข้อมูลจาก StudyNotes PDF หน้า 40 ไม่ใช่การเดารหัส segment ของข้อสอบปี 2015/2018

## 6. Replacement ปี 2022: reference string ไม่ใช่ชุดคลาสสิก

Reference string: 7,0,1,3,0,3,2,4,2,7,0,3,2,1,2,0,1,4,0,1; 20 references; 3 frames เริ่มว่าง

| Policy | Faults | Hits | Fault rate |
| --- | ---: | ---: | ---: |
| FIFO | 13 | 7 | 0.65 |
| LRU | 13 | 7 | 0.65 |
| OPT | 10 | 10 | 0.50 |

Memory=10 ns, disk=10 ms=10,000,000 ns และใช้ EAT=(1-p)m+p d ตาม Lecture:

- FIFO/LRU: 0.35×10 + 0.65×10,000,000 = **6,500,003.5 ns** = 6.5000035 ms
- OPT: 0.50×10 + 0.50×10,000,000 = **5,000,005 ns** = 5.000005 ms

ถ้าใช้เวลา fault-service ที่รวม memory retry หรือ write-back เพิ่มตามโจทย์อื่น ต้องเปลี่ยน d ให้ตรงโมเดลนั้น ไม่ควรถือว่าค่าทศนิยมละเอียดจากโมเดลง่ายนี้ใช้ได้กับทุกโจทย์

## 7. String คลาสสิกและอสมการ EAT

Reference string: 7,0,1,2,0,3,0,4,2,3,0,3,2,1,2,0,1,7,0,1; เริ่ม frames ว่าง

| Frames | FIFO faults | LRU faults | OPT faults |
| --- | ---: | ---: | ---: |
| 3 | 15 | 12 | 9 |
| 4 | 10 | 8 | 8 |
| 5 | 9 | 7 | 7 |

ดังนั้นตาราง 4 frames ที่ได้ 7 faults ต้องตรวจการไล่ใหม่ ตัวเลข 7 เป็นผลของ LRU/OPT 5 frames สำหรับ string นี้ ไม่ควรสลับไปใช้กับโจทย์ 4 frames

สำหรับโจทย์ 4 frames, LRU, memory=9 ns และ disk=25 ms:

\[
p=8/20=0.4,\quad EAT=0.6(9)+0.4(25,000,000)=10,000,005.4\ ns
\]

ถ้าต้องการ EAT ไม่เกิน 100 เท่าของ memory access time:

\[
9+p(25,000,000-9)\le900
\]

\[
p\le\frac{891}{24,999,991}\approx3.564\times10^{-5}
\]

ค่านี้เท่ากับประมาณ 0.003564% ต้องแยก probability ออกจาก percent ให้ชัด

## 8. วิธีตรวจงานด้วยตัวเอง

- Scheduling: CPU-only ต้องได้ turnaround - waiting = burst ของแต่ละ process; first-start ไม่เกิน completion; เวลารันรวมเท่ากับ burst รวม
- Allocation: occupied + holes ครอบคลุมทั้ง memory โดยไม่ทับและไม่ตกช่วง; best-fit เลือก hole ที่เล็กที่สุดในกลุ่มที่ใส่ได้
- Paging: offset หลังแปลต้องเท่าเดิมและอยู่ใน [0,page size); page กับ frame มีขนาดเท่ากัน
- Replacement: hits+faults=จำนวน references; OPT ต้องมี faults ไม่มากกว่า policy อื่นภายใต้ input/จำนวน frames เดียวกัน
- EAT: ต้องอยู่ระหว่างเวลา hit กับเวลา fault ตามโมเดล และแปลงทุกเวลาให้อยู่หน่วยเดียวก่อนเฉลี่ย
