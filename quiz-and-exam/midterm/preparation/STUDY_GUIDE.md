---
title: "CPE333 เตรียมสอบกลางภาค"
subtitle: "Lecture 1-6 | อ่านอะไร ฝึกอะไร เปิดข้อสอบหน้าไหน"
author: "จัดจากเอกสารในคลังรายวิชา"
date: "22 ตุลาคม 2026"
lang: th
---

# วิธีใช้ชุดนี้

ขอบเขตที่ใช้คือ Lecture 1-6 ตามที่กำลังเตรียมสอบ ไม่ได้อาศัยเพียงชื่อว่าเป็นข้อสอบ midterm เพราะข้อสอบบางปีรวม threads, semaphore และ deadlock ไว้ด้วย การจัดลำดับด้านล่างเป็นข้อเสนอจากเนื้อหาและโจทย์เก่าที่มี ไม่ใช่การทำนายคะแนนหรือยืนยันหัวข้อสอบรอบนี้

ใช้สรุป CPE333_OS_Midterm_StudyNotes เป็นเนื้อหาอ่านหลัก ใช้สไลด์รายบทตัดสินเมื่อมีข้อสงสัย และใช้ข้อสอบเก่าเป็นแบบฝึก การมีคำตอบสีเขียว วงตัวเลือก หรือจดเฉลยไว้ ไม่ได้ทำให้คำตอบนั้นถูกต้องเสมอไป มีตัวอย่างที่คำตอบขัดกันอยู่จริง

เลขหน้าในคู่มือนี้เป็น **หน้าในตัวเปิด PDF นับจาก 1** ไม่ใช่เลขพิมพ์ท้ายหน้า ตัวอย่างเช่น Lecture 1 เริ่มที่ PDF หน้า 6 ของ StudyNotes แต่เลขพิมพ์บนเล่มคือ 5

| อ่านเป็นบท | หน้าสรุป PDF เดิม | ทักษะที่ต้องทำได้ |
| --- | --- | --- |
| Lecture 1 | 6-12 | อธิบาย OS, system call, user/kernel mode และ virtualization |
| Lecture 2 | 13-22 | ไล่ process states, context switch และ fork/wait/exec |
| Lecture 3 | 23-30 | วาด Gantt chart และคำนวณ scheduling metrics |
| Lecture 4 | 31-38 | แปล base/bounds และทำโจทย์จัดสรร memory |
| Lecture 5 | 39-47 | แยก address fields ค้น page/segment table และอธิบาย TLB |
| Lecture 6 | 48-62 | ไล่ page replacement คำนวณ EAT และอธิบาย page fault |
| ทบทวนรวม | 63-67 | เชื่อม CPU, memory, I/O และ process states เข้าด้วยกัน |

แฟ้ม 01-06 รวมหน้าสรุปของแต่ละบทกับหน้าข้อสอบที่เลือกไว้แล้ว แฟ้ม 07 เป็นหน้าทบทวนรวมจากเล่มเดิม คำว่า FINAL REVIEW บนหน้าต้นฉบับหมายถึงส่วนสรุปท้ายเล่มซึ่งยังครอบคลุม Lecture 1-6

# ควรให้เวลากับอะไร

**ทักษะคำนวณหลักมี 4 กลุ่ม:** scheduling, contiguous allocation, address translation และ page replacement/EAT ขณะเดียวกันต้องอธิบาย process และกลไกของ OS ได้ เพราะเป็นทั้งคำถามแนวคิดและเหตุผลประกอบข้อเขียน

| กลุ่มฝึก | สิ่งที่ต้องลงมือทำ | หลักฐานจากชุดที่มี |
| --- | --- | --- |
| Scheduling | FIFO/SJF/STCF/RR, waiting/response/turnaround, MLFQ | Quiz หน้า 1, 3; ชุด 2022 หน้า 1; ข้อเขียนปี 2015/2018 |
| Memory allocation | วาด holes, first/best/worst fit, fragmentation | Quiz หน้า 2, 4; ชุด 2018 หน้า 5 ข้อ 2 |
| Address translation | base/bounds, segment/offset, page/frame bits, page-table size | ชุด 2018 หน้า 5 ข้อ 3-5; รวมข้อเขียน หน้า 7, 12-14 |
| Virtual memory | นับ faults, FIFO/LRU/OPT, EAT, แก้อสมการ page-fault rate | ชุด 2022 หน้า 2; ชุด 2018 หน้า 5 ข้อ 6-7 |
| Process และ OS mechanisms | วาด state diagram, ลำดับ context switch, trace fork/wait/exec | ปรนัยปี 2015/2018; รวมข้อเขียน หน้า 1-3; os midterm exam |

ทุก Lecture ยังอยู่ในขอบเขต ตารางนี้ใช้จัดเวลาฝึก ไม่ใช่เหตุผลให้ตัดบทที่เป็นแนวคิดออก

# Lecture 1: Introduction to OS

อ่าน StudyNotes PDF หน้า 6-12 ใช้แฟ้ม **01 Introduction**

## ภาพที่ต้องเข้าใจ

OS อยู่ระหว่าง application กับ hardware เพื่อจัดการทรัพยากรและให้ abstraction เช่น process และ address space โปรแกรมผู้ใช้ทำงานด้วยสิทธิ์จำกัด เมื่อต้องการบริการจาก kernel จึงใช้ system call ผ่านทางเข้าที่ควบคุมไว้

แยกให้ได้ว่า **mechanism** ทำให้ระบบทำงานได้อย่างไร ส่วน **policy** เลือกว่าจะทำกับใครหรือเลือกแบบใด เช่น timer interrupt/context switch เป็นกลไก ส่วน RR เป็นนโยบาย

## สิ่งที่ต้องเตรียม

- อธิบายหน้าที่ของ OS และเหตุผลที่ต้องมี protection/isolation
- วาด application → system-call interface → kernel → hardware และทางกลับ
- แยก user mode กับ kernel mode; privileged instruction ทำไมไม่ควรให้ application เรียกเองได้
- อธิบาย CPU virtualization และ memory virtualization ด้วยตัวอย่างคนละหนึ่งกรณี
- รู้ความหมายของ concurrency และ persistence ในภาพรวม
- แยก system call, trap และ hardware interrupt ให้ได้: system call อาศัยทางเข้า kernel แบบ synchronous ส่วน timer interrupt เป็นเหตุการณ์จากอุปกรณ์ภายนอก

## โจทย์ที่ควรทำ

- os midterm exam PDF หน้า 1 ข้อ 1-3 และหน้า 2 ข้อ 5
- ยำรวมมิตรข้อเขียน PDF หน้า 1 ข้อ 2, 5, 7

**ก่อนผ่านบท:** ปิดเอกสารแล้วอธิบายว่า “โปรแกรมอ่านไฟล์ได้อย่างไร ทั้งที่ไม่ได้มีสิทธิ์ควบคุม disk เอง” ภายในประมาณหนึ่งนาที อย่าสรุปว่า system call ทุกครั้งต้องทำให้เปลี่ยนไปใช้ process อื่น

# Lecture 2: Process and Process APIs

อ่าน StudyNotes PDF หน้า 13-22 ใช้แฟ้ม **02 Process and APIs**

## ภาพที่ต้องเข้าใจ

Program คือคำสั่งและข้อมูลที่จัดเก็บไว้ Process คือ instance ที่กำลังทำงานพร้อม CPU/memory/OS state ที่จำเป็นต่อการหยุดแล้วกลับมาทำต่อ PCB เก็บข้อมูลที่ kernel ต้องใช้จัดการ process ส่วน context switch คือการบันทึกและคืน state เพื่อเปลี่ยนผู้ใช้ CPU

แผนสถานะหลักที่ต้องวาดได้คือ Ready → Running เมื่อถูกเลือก; Running → Ready เมื่อถูก preempt/yield ตามแบบจำลอง; Running → Blocked เมื่อรอ I/O หรือ event; Blocked → Ready เมื่อสิ่งที่รอเสร็จ การรอ I/O ไม่ได้ทำให้กระโดดจาก Ready ไป Blocked โดยตรงในแผนสามสถานะนี้

## สิ่งที่ต้องเตรียม

- แยก code/data/heap/stack กับ metadata ของ process ใน kernel; บอกหน้าที่ PC, registers และ stack pointer ได้
- รู้ส่วนประกอบ process ตามแบบจำลองในสไลด์: program, data state, control state และ process state
- วาด state transitions พร้อมเหตุการณ์บนลูกศร
- อธิบาย Limited Direct Execution: รัน user code โดยตรง แต่จำกัดสิทธิ์และมีทางกลับเข้า kernel
- ไล่ context switch: เข้า handler, save state, scheduler เลือก, restore state, กลับไปรัน process ที่เลือก
- แยก cooperative control กับ non-cooperative/preemptive control และเหตุผลที่ต้องใช้ timer
- `fork()` สร้าง child; parent ได้ PID ของ child, child ได้ 0; ทั้งสองทำต่อหลัง fork เมื่อสำเร็จ
- `wait()`/`waitpid()` ใช้รอและรับสถานะ child; `exec()` แทน program image และไม่กลับมาบรรทัดถัดไปเมื่อสำเร็จ
- วาด process tree เพื่อหาจำนวนการพิมพ์และลำดับที่รับประกันได้
- อธิบาย shell แบบ fork → เปลี่ยน environment/redirect → exec; parent wait ตามเงื่อนไข
- ทบทวน pipe พื้นฐานจากท้ายบท และความต่าง CPU-bound กับ I/O-bound

## โจทย์ที่ควรทำ

- ชุดปี 2015 ที่ชื่อมี `(1)` PDF หน้า 3 ข้อ 5-7 และหน้า 7 ข้อ III(a)
- ยำรวมมิตรข้อเขียน PDF หน้า 1 ข้อ 6, 8; หน้า 2 ข้อ 9, 10, 13, 15; หน้า 3 ข้อ 18, 20
- os midterm exam หน้า 3-5 ใช้ทบทวนสถานะ, PCB และ wait

หน้าข้อเขียนบางหน้ามี threads/critical section ปนอยู่ ให้ทำเฉพาะข้อที่ระบุสำหรับขอบเขตนี้

**ก่อนผ่านบท:** ไล่โปรแกรมที่มี `fork(); fork(); printf(...)` ได้เมื่อสมมติว่าทุก fork สำเร็จและไม่มี output ค้างก่อน fork และอธิบายได้ว่าการใส่ wait ทำให้ลำดับใดแน่นอนขึ้น

# Lecture 3: Scheduling

อ่าน StudyNotes PDF หน้า 23-30 ใช้แฟ้ม **03 Scheduling**

## สิ่งที่ต้องเตรียม

- **FIFO/FCFS:** เลือกตามลำดับเข้าคิว ไม่มีการแย่ง CPU ในแบบฝึกพื้นฐาน; อธิบาย convoy effect
- **SJF:** เลือก CPU burst ที่สั้นที่สุดในงานพร้อมรัน แบบ non-preemptive
- **STCF/SRTF:** เลือกเวลาทำงานที่เหลือน้อยที่สุด แบบ preemptive; ข้อสอบเขียน “SJF preemptive” ให้ใช้ความหมายนี้
- **RR:** วน ready queue ตาม quantum; ทำให้ตอบสนองเร็วขึ้น แต่ต้องนับการรอสะสมและต้นทุน context switch
- **MLFQ:** ท่องกฎฉบับสุดท้าย 5 ข้อพร้อมเหตุผล ได้แก่เลือก priority สูง, priority เท่ากันใช้ RR, job ใหม่เข้าบนสุด, ใช้ allotment สะสมครบแล้วลดระดับ, boost ทุกช่วง S
- แยก **priority boost** ที่แก้ starvation กับ **better accounting** ที่ป้องกัน gaming
- ทบทวน lottery: ticket ให้สัดส่วน CPU ระยะยาว ไม่ใช่รับประกันจำนวนครั้งในช่วงสั้น
- เมื่อมี I/O ให้ปรับ ready queue ตามการ block และ completion ตามโจทย์

## สูตรที่ใช้

กำหนด A = arrival, S = first start, C = completion, B = CPU burst รวม

\[
T_{turnaround}=C-A,\qquad T_{response}=S-A
\]

สำหรับแบบฝึก CPU-only ที่ไม่มี I/O:

\[
T_{waiting}=C-A-B
\]

Waiting time นับเวลารอใน ready queue **ทุกช่วง** ส่วน response time นับรอจนได้ CPU ครั้งแรก จึงอาจต่างกันมากใน RR ถ้ามี I/O จะใช้ waiting = turnaround - CPU burst โดยไม่หักเวลาที่ block ไม่ได้

## วิธีทำโจทย์

1. เขียน arrival, burst, quantum, preemption และกฎกรณีเสมอกัน
2. วาด Gantt chart โดยอัปเดต ready queue ทุก arrival/completion/หมด quantum
3. จด S กับ C ของทุก process
4. คำนวณ metric ราย process แล้วจึงเฉลี่ย
5. ตรวจว่าระยะเวลารันรวมตรงกับ burst รวม และทุก process ได้ CPU ครบ

## โจทย์ที่ควรทำตามลำดับ

1. Quiz_BeforeMidterm หน้า 1: ทุก process มาพร้อมกัน, q = 1
2. Quiz_BeforeMidterm หน้า 3: คำนวณ waiting time, q = 10
3. ชุด 2022 หน้า 1: arrival ต่างกัน, FCFS/STCF/RR
4. ชุดปี 2015 `(1)` หน้า 6: อธิบายธนาคารด้วย MLFQ ให้โยงแต่ละกฎกับเหตุผล

**ค่าตรวจสำคัญ:** ชุด 2022 FCFS มี average waiting = 4.8 และ average turnaround = 8.0; ตัวเลข 7.8 ที่เขียนไว้บางสำเนาไม่ตรงกับตารางงาน ดูวิธีคำนวณใน CHECKED_DRILLS

**ก่อนผ่านบท:** ทำโจทย์ใหม่ได้โดยไม่ต้องเปิดเฉลย และอธิบายได้ว่า policy ที่ดีต่อ response ไม่จำเป็นต้องดีที่สุดต่อ turnaround

# Lecture 4: Memory Concept and Contiguous Allocation

อ่าน StudyNotes PDF หน้า 31-38 ใช้แฟ้ม **04 Contiguous Memory**

## สิ่งที่ต้องเตรียม

- แยก logical/virtual address กับ physical address และอธิบายหน้าที่ MMU
- ทบทวน address binding ช่วง compile/load/execution และ static/dynamic relocation
- ทำ base/bounds translation พร้อมตรวจ fault ก่อนบวก base
- แยก fixed-size partition ซึ่งมี internal fragmentation กับ flexible-size partition ซึ่งมี external fragmentation
- **Coalescing** รวม holes ที่ติดกัน; **compaction** ย้ายการจัดวางเพื่อรวมพื้นที่ว่าง
- วาด memory map และหา holes จาก base+size ของแต่ละ process
- ใช้ first-fit, best-fit, worst-fit ตามลำดับค้นหาและขนาดที่โจทย์ให้
- ทบทวนภาพ code/data/heap/stack และ C storage classes ที่อยู่ในสไลด์ Lecture 4 เป็นหัวข้อเสริม

## สูตรและข้อควรระวัง

แบบจำลอง bounds เป็นขนาดของพื้นที่ที่อนุญาต:

\[
0\le VA<Bounds\ \Rightarrow\ PA=Base+VA
\]

เมื่อ VA เท่ากับ Bounds ถือว่าเกินขอบเขตแล้ว อย่าสับสน bounds ที่เป็น “ขนาด” กับ physical ending address และต้องใช้หน่วยเดียวกันก่อนบวกหรือเทียบ

ในการหา hole ใช้ช่วงแบบ [start, end) โดย end = base + size ทำให้ขนาด hole เป็น next_start - previous_end ได้ตรง ไม่ต้องบวกหนึ่งแบบช่วง inclusive

## โจทย์ที่ควรทำ

- Quiz_BeforeMidterm หน้า 2: holes และรับ process ใหม่ 30 KB
- Quiz_BeforeMidterm หน้า 4: โจทย์ลักษณะเดียวกัน แต่ขนาด A/B/D เปลี่ยน จึงใช้คำตอบเดิมไม่ได้
- ยำรวมมิตรข้อเขียน หน้า 11: ใช้เป็นโจทย์อธิบาย fragmentation พร้อมวาดรูปเอง

**ก่อนผ่านบท:** เมื่อให้ memory 512 KB พร้อม process A-D ต้องวาด holes และเลือกทั้งสามวิธีได้ พร้อมอธิบายว่าทำไมมีพื้นที่ว่างรวมมากแต่ยังวาง process ไม่ได้

# Lecture 5: Noncontiguous Allocation and Address Translation

อ่าน StudyNotes PDF หน้า 39-47 ใช้แฟ้ม **05 Address Translation**

## สิ่งที่ต้องเตรียม

- **Segmentation:** แยก segment ID กับ offset; ตรวจขนาดและทิศทางก่อนแปล; อย่านำ VA ทั้งก้อนไปบวก base ของ segment
- **Paging:** page อยู่ฝั่ง virtual, frame อยู่ฝั่ง physical และมีขนาดเท่ากัน; เปลี่ยน VPN เป็น PFN แต่คง offset เดิม
- แยก address bits, จำนวน virtual pages, physical frames และขนาด page table
- อธิบาย linear, multi-level, inverted และ hashed page table พร้อม trade-off
- **Inverted page table:** มี entry ตาม physical frame; ค้นด้วยข้อมูลระบุ process และ virtual page
- **TLB:** cache ของ translations; miss อาจต้องค้น page table แต่ไม่ได้แปลว่า page ไม่อยู่ RAM
- เปรียบเทียบ segmentation กับ paging ด้าน fragmentation และ metadata
- ทบทวน hybrid segmentation+paging และ page-size trade-off หลังทำพื้นฐานได้

## สูตรที่ใช้

เมื่อ page size = $2^b$ bytes และ VA มี v bits, PA มี p bits:

\[
offset\ bits=b,\quad VPN\ bits=v-b,\quad PFN\ bits=p-b
\]

\[
VPN=\lfloor VA/PageSize\rfloor,\quad offset=VA\bmod PageSize
\]

\[
PA=PFN\times PageSize+offset
\]

Linear page-table size = จำนวน virtual pages × ขนาด PTE ที่โจทย์กำหนด หน่วย PTE เป็น bit ต้องหาร 8 เมื่อแปลงเป็น byte และต้องคำนึงถึงการปัดตามที่โจทย์กำหนด ถ้าจำนวน pages ไม่เป็นกำลังสอง ใช้จำนวน bits ขั้นต่ำเป็น ceiling ของ log ฐาน 2

## โจทย์ที่ควรทำ

- ยำรวมมิตรข้อเขียน หน้า 7: 140 pages, page 1024 bytes, physical 64 frames
- หน้า 12: page table และ inverted page table
- หน้า 13: VA 64 bits / PA 32 bits / page 1024 bytes ให้แยก fields
- หน้า 14: segmentation ใช้ฝึกแยก segment/offset และตรวจ bounds โดยอ่านรหัส segment กับทิศทาง stack ของโจทย์ให้ชัด
- ถ้าข้อมูลของ segment ID หรือทิศทางไม่พอ ให้ระบุสมมติฐานก่อนคำนวณ ไม่เดาจากคำตอบที่เขียนกำกับไว้

**ค่าตรวจ:** 140 pages × 1024 bytes ต้องใช้ address อย่างน้อย 18 bits; physical 64 frames ใช้ 16 bits ส่วนโจทย์ VA 64 / PA 32 / page 1 KiB มี fields 54+10 และ 22+10 bits ตามลำดับ

**ก่อนผ่านบท:** ให้ VA กับ page size และ mapping แล้วต้องหา PA ได้ พร้อมแยกได้ว่ากรณีใดเป็น TLB miss, page fault หรือ protection/bounds fault

# Lecture 6: Virtual Memory

อ่าน StudyNotes PDF หน้า 48-62 ใช้แฟ้ม **06 Virtual Memory**

## สิ่งที่ต้องเตรียม

- อธิบาย demand paging และความต่าง context switching กับ swapping
- ไล่ page fault ครบ: ตรวจ PTE → trap เข้า handler → หาที่อยู่ page/หา frame และเลือก victim ถ้าจำเป็น → I/O ระหว่าง process block → update mapping เมื่อเสร็จ → ready → กลับไป restart instruction เมื่อถูก schedule
- **FIFO:** เอาหน้าที่เข้า RAM เก่าที่สุดออก; hit ไม่เปลี่ยนลำดับ queue
- **LRU:** เอาหน้าที่ไม่ได้ใช้นานที่สุดออก; hit ต้องปรับ recency
- **OPT:** เลือกหน้าที่จะใช้ครั้งต่อไปไกลที่สุดหรือไม่ใช้อีก; ใช้เป็น benchmark เพราะต้องรู้อ้างอิงอนาคต
- นับ initial/cold-start faults เมื่อเริ่ม frames ว่าง
- ทบทวน LFU และ Second Chance ตามสรุป; ถ้าใช้ LFU ต้องระบุกฎกรณีจำนวนครั้งเสมอ
- อธิบาย Belady's anomaly และข้อจำกัดของการอ้างว่าเพิ่ม frame แล้ว fault ต้องลดเสมอสำหรับทุก policy
- คำนวณ EAT และแก้อสมการ page-fault rate; แปลงหน่วยให้ถูก
- อธิบาย thrashing, locality, working set, global/local replacement และ TLB reach

## สูตรที่ใช้

\[
p_f=\frac{\text{จำนวน page faults}}{\text{จำนวน references}}
\]

ตามแบบจำลองอย่างง่ายของ Lecture 6:

\[
EAT=(1-p_f)m_a+p_fd_a
\]

โดย $m_a$ คือ memory access time และ $d_a$ คือเวลา disk/fault ตามที่โจทย์ใช้ ถ้าโจทย์กำหนดขั้นตอน fault เพิ่ม ให้คำนวณตามข้อมูลของโจทย์นั้นก่อนแทนสูตร ห้ามรวมสมมติฐานคนละแบบเข้าด้วยกัน

ถ้าต้องการ $EAT\le k m_a$ และ $d_a>m_a$:

\[
p_f\le\frac{(k-1)m_a}{d_a-m_a}
\]

หน่วย: 1 ms = 1,000,000 ns; 1 us = 1,000 ns และ probability 0.01 เท่ากับ 1% ไม่ใช่ 0.01%

Working-set demand ใช้ $D=\sum_i WS_i$ ถ้า demand เกิน available frames ตามแบบจำลองใน Lecture จะเกิดความเสี่ยง thrashing; TLB reach = จำนวน TLB entries × page size

## วิธีทำตาราง

ทำคอลัมน์ reference, frame contents, hit/fault และ victim ทุกครั้ง เขียนสถานะ queue/recency ข้างตาราง ตรวจจำนวน references, จำนวน frames และ reference string จากโจทย์จริง เพราะไฟล์เก่ามีตัวเลขคล้ายกันหลายชุด

## โจทย์ที่ควรทำ

1. ชุด 2022 ฉบับ 9 หน้า PDF หน้า 2: 3 frames, FIFO/LRU/OPT, memory 10 ns, disk 10 ms
2. ยำรวมมิตรข้อเขียน หน้า 16-17: LRU 4 frames และหาเงื่อนไข EAT ไม่เกิน 100 เท่าของ RAM
3. หน้า 8: โจทย์อีกสำเนาระบุ 5 frames; อย่าคัดตาราง 3/4 frames จากหน้าข้างเคียงมาใช้
4. หน้า 15: ใช้ฝึกอธิบายผลของ page size แต่ตรวจเหตุผลกับสไลด์แทนการจำคำตอบสแกนทั้งหมด

**ค่าตรวจ:** string ปี 2022 มี faults FIFO=13, LRU=13, OPT=10 เมื่อใช้ 3 frames เริ่มว่าง ส่วน string คลาสสิกอีกชุดใช้ LRU 4 frames ได้ 8 faults ตัวเลขสองชุดนี้นำมาปนกันไม่ได้

# แผนอ่านที่นำไปใช้ได้

## เริ่มด้วยตรวจพื้นฐาน 6 ข้อ

1. อธิบาย system call กับ privilege boundary
2. วาด Ready/Running/Blocked และ trace fork/wait/exec
3. ทำ Gantt chart พร้อมสาม metrics
4. หา holes และ first/best/worst fit
5. แยก VPN/offset/PFN แล้วหา PA
6. ทำ replacement table และ EAT

ข้อที่ทำไม่ได้ให้กลับไปอ่านบทนั้นก่อน ถ้าทำได้แต่ผิดเลข ให้เพิ่มรอบทำโจทย์และตรวจหน่วย ไม่จำเป็นต้องอ่านเล่ม 67 หน้าซ้ำตั้งแต่ต้นทุกครั้ง

## ถ้ามีประมาณ 3 วัน

| วัน | รอบที่ 1 | รอบที่ 2 | รอบที่ 3 |
| --- | --- | --- | --- |
| 1 | L1-2 ภาพรวมและ state diagram | fork/wait/exec + context-switch ข้อเขียน | L3 Quiz หน้า 1, 3 แล้วตรวจ metric |
| 2 | L4 Quiz หน้า 2, 4 | L5 address bits และ page/segment table | L6 page fault + เริ่มตาราง replacement |
| 3 | L6 replacement/EAT จนทำเองได้ | จับเวลาชุดผสม | แก้ error log แล้วตอบคำถามทบทวนท้ายเล่ม |

เริ่มรอบละประมาณ 45-60 นาทีแล้วเพิ่มเวลาตามความยากของตนเอง แผนนี้เป็นลำดับงาน ไม่ใช่เวลาที่รับประกันว่าจะอ่านครบสำหรับทุกคน

## ถ้าเหลือหนึ่งวัน

เก็บ L1-2 เป็นการตอบปากเปล่าและวาด flow ก่อน จากนั้นทำ Quiz 4 หน้าให้ครบ ตามด้วยชุด 2022 สองหน้า และโจทย์ address bits/EAT ที่เลือกจากชุด 2018 หากเวลาจำกัดให้ทำโจทย์ตัวแทนจนเข้าใจวิธีคิด มากกว่าทำชุดซ้ำหลายสำเนา

## แบบฝึกผสมที่เสนอ: 70 นาที

- 10 นาที: อธิบาย system call, process states และ context switch จากความจำ
- 20 นาที: scheduling ปี 2022 หน้า 1 เลือก FCFS และ STCF หรือ RR
- 10 นาที: holes/first-best-worst fit จาก Quiz หน้า 2
- 10 นาที: address bits และแปล VA ด้วย page table
- 20 นาที: replacement ปี 2022 หน้า 2 เลือกสอง policy แล้วคำนวณ EAT

นี่เป็นแบบฝึกที่จัดขึ้นใหม่ ไม่ใช่การจำลองรูปแบบหรือเวลาสอบจริง ปิดเฉลยขณะทำและจดว่าแต่ละข้อผิดเพราะแนวคิด การไล่ขั้นตอน หรือเลข/หน่วย

# ข้อสอบเก่าที่ใช้ก่อนและหลัง

1. **Quiz_BeforeMidterm:** เริ่มก่อน มี scheduling และ memory allocation รวม 4 หน้า แต่มี handwritten answers จึงควรปิดเฉลย
2. **ชุด 2022 ฉบับ 9 หน้า:** หน้า 1-2 เป็นโจทย์คำนวณหลัก; หน้า 3-9 เป็น screenshots/สรุปปรนัยที่ทับกับชุดอื่น
3. **ชุด 2018 ฉบับชื่อมี 1_ต.ค.2561:** หน้า 2-4 เป็นปรนัยปน threads; หน้า 5 รวมข้อเขียนที่ครอบคลุม L3-6 ส่วนหน้าหลังเป็นคำตอบจดเพิ่ม
4. **ยำรวมมิตรข้อเขียน:** ใช้ฝึกอธิบายและคำนวณตามหน้าในดัชนี มีหัวข้อนอกขอบเขตปนต้นเล่ม
5. **os midterm exam / Backroom:** ใช้เป็นคำถาม flashcard หลังเข้าใจแล้ว เลือกเพียงหนึ่งชุดในรอบแรก เพราะปรนัยช่วงแรกทับกันมาก

รายละเอียดทุกไฟล์อยู่ใน PRACTICE_INDEX.md ไม่มีการนับสำเนาเดียวกันหลายครั้งเป็นหลักฐานว่าข้อใดจะออกบ่อย

# จุดที่ต้องตรวจคำตอบเป็นพิเศษ

- **Waiting ไม่ใช่ response:** ใน RR process กลับไปรอได้หลายครั้ง ตัวอย่างปี 2022 ที่เขียน waiting=0.8 น่าจะใช้ first-response บางลำดับแทน waiting ซึ่งคำนวณได้ 3.0 สำหรับ STCF
- **FCFS ปี 2022:** average turnaround จากข้อมูลงานคือ 8.0 ไม่ใช่ 7.8
- **Fixed partition:** มี internal fragmentation ได้; ข้อ 20 ใน Backroom บางสำเนาเลือก “none true” ทั้งที่มีตัวเลือกนี้อยู่ ให้ตรวจ Lecture 4
- **Ready → Blocked:** ในแผนสามสถานะพื้นฐาน process ต้องได้รันก่อนจึงเริ่ม blocking I/O คำตอบกำกับในสองไฟล์ไม่ตรงกัน
- **Timer กับ cooperative:** timer ช่วย preempt/regain CPU โดยไม่รอความร่วมมือ อย่าจำประโยคว่า non-preemptive จำเป็นต้องใช้ timer เป็นคำตอบทั่วไป
- **Zombie:** child ที่จบแล้วแต่สถานะยังไม่ถูกเก็บด้วย wait เป็นคนละประเด็นกับ orphan ที่ parent จบก่อน คำตอบในข้อ 31 ของบางชุดใช้ถ้อยคำชวนสับสน
- **Segmentation:** จุดเด่น/ข้อเสียต้องแยก external fragmentation ออกจาก overhead ของ page table ซึ่งเกี่ยวกับ paging โดยตรง
- **EAT:** 10 ms ไม่ใช่ $10^{-3}$ วินาที แต่เป็น $10\times10^{-3}$ วินาที และ 10 ns ไม่ใช่ $10^{-9}$ วินาทีเฉย ๆ
- **Page-table size ในสไลด์:** $2^{20}\times33$ ได้หน่วย bit เมื่อแปลงเป็น byte จะประมาณ 4.125 MiB สรุปเดิม PDF หน้า 43 ได้ชี้หน่วยนี้ไว้แล้ว
- คำตอบเช่น “STCF throughput สูงสุดเสมอ” หรือ “คอมพิวเตอร์ทำงานไม่ได้ถ้าไม่มี OS” กว้างเกินสมมติฐาน ควรตอบเหตุผลตาม workload/โมเดลของคำถาม ไม่ท่องเป็นข้อเท็จจริงสากล

CHECKED_DRILLS มีตัวเลขและสมมติฐานที่คำนวณใหม่ให้ใช้ตรวจตัวอย่างหลัก แต่ไม่ได้เป็นเฉลยทางการครบทุกข้อของทั้ง 10 ไฟล์

# แหล่งข้อมูลและขอบเขต

เนื้อหาหลัก: lectures/CPE333_OS_Midterm_StudyNotes.pdf (67 หน้า) และสไลด์ Lecture1_IntroductionToOS, Lecture2_ProcessAndProcessAPIs, Lecture3_Scheduling, Lecture4_MemoryConceptAndContiguousMemoryAllocation, Lecture5_NoncontiguousMemoryAllocation, Lecture6_VirtualMemory

โจทย์: PDF 10 ไฟล์ที่อยู่ระดับบนของ quiz-and-exam/midterm; ชื่อเต็ม จำนวนหน้า หน้าที่แนะนำ และความซ้ำระบุใน PRACTICE_INDEX.md

นอกขอบเขตที่กำหนดครั้งนี้: รายละเอียด threads/user-vs-kernel threads, locks/critical sections, semaphores, deadlock และ Banker algorithm ซึ่งพบปนในข้อสอบบางปีและเป็นเนื้อหาหลัง Lecture 6 คำว่า concurrency ในภาพรวมของ Lecture 1 ยังควรรู้

ไม่มีประกาศวันสอบ สัดส่วนคะแนน หรือการรับรองเฉลยของผู้สอนในข้อมูลที่ใช้ จึงจัดเป็นแผนเตรียมตามขอบเขตที่ผู้ใช้ระบุและโจทย์ที่มีอยู่
