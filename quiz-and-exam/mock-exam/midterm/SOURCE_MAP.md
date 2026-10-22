# Question Source Map

แผนผังแหล่งเก่าสำหรับตรวจย้อนกลับ ไม่พิมพ์เฉลย/ตารางนี้ปนในฉบับสอบ ดูผลเทียบข้อเขียนครบทุกข้อใน [REFERENCE_AUDIT.md](REFERENCE_AUDIT.md)

## แหล่งหลักที่ตรวจยืนยัน

- E03: ข้อสอบ CPE326 Operating System ปี 2561 ไฟล์ 1_ต.ค.2561.pdf หน้า 2–4
- E05: ไฟล์ OS-Midterm-2022 ชื่อยาว หน้า 3–6 เป็นภาพช้อยส์ถึงข้อ 51; หน้า 7–9 เป็นสรุป text ถึงข้อ 40
- E09 = os midterm exam.pdf และ E06 = Backroom.pdf เป็นชุดซ้ำที่ใช้เทียบตัวเลือก ไม่ใช้ชื่อสองไฟล์นี้ยืนยันปีเอง
- E10 = ยำรวมมิตรข้อเขียน.pdf

ปรนัย 5 ข้ออิง E03 และ 36 ข้ออิง E05 คัดและปรับ grammar/ตัวเลือกให้ตอบได้ข้อเดียว ไม่ใช่สำเนาคำต่อคำ ต้นฉบับปี 2561 เป็น multiple-select และโน้ตเฉลยในชุด 2022 บางข้อผิด จึงไม่คัดตามทั้งหมด

## Multiple Choice: 41 ข้อ

| ข้อใหม่ | Lecture | ปีต้นทาง | ข้อ/หน้าต้นทาง | คำถามในฉบับนี้ | เฉลย |
|---:|---:|---|---|---|:---:|
| 1 | 1 | 2022 | E05 หน้า 3 ข้อ 1 | What is a trap in an operating system? | b |
| 2 | 1 | 2022 | E05 หน้า 3 ข้อ 2 | What could happen without separation between user mode and privileged mode? | c |
| 3 | 2 | 2561 | E03 หน้า 4 ข้อ 14 | In UNIX, which numeric identifier identifies a live process on the system? | c |
| 4 | 2 | 2561 | E03 หน้า 2 ข้อ 5 | Which register holds the address of the next instruction to execute? | b |
| 5 | 1 | 2022 | E05 หน้า 3 ข้อ 5 | Which OS concern protects one application from unauthorized access by another? | c |
| 6 | 2 | 2022 | E05 หน้า 3 ข้อ 6 | Which listed facility is required specifically for voluntary process switching in a non-preemptive system? | d |
| 7 | 2 | 2022 | E05 หน้า 3 ข้อ 7 | Which part of a process is normally maintained in kernel space? | b |
| 8 | 2 | 2022 | E05 หน้า 3 ข้อ 8 | In the conventional address-space layout, the heap grows upward. Which region typically grows in the opposite direction? | c |
| 9 | 2 | 2022 | E05 หน้า 3 ข้อ 9 | In the basic three-state model, when can a ready process move directly to blocked? | d |
| 10 | 2 | 2561 | E03 หน้า 4 ข้อ 12 | The state of a process is defined by which of the following? | d |
| 11 | 2 | 2022 | E05 หน้า 3 ข้อ 11 | A process is blocked on a disk read. What is it waiting for? | a |
| 12 | 2 | 2022 | E05 หน้า 3 ข้อ 12 | What does it mean when a process is a zombie? | b |
| 13 | 2 | 2022 | E05 หน้า 4 ข้อ 13 | Which data structure keeps a process's state, saved registers, and scheduling information? | c |
| 14 | 2 | 2022 | E05 หน้า 4 ข้อ 14 | A child prints before exiting. Its parent successfully waits for that child and then prints. Which order is guaranteed? | d |
| 15 | 3 | 2022 | E05 หน้า 4 ข้อ 15 | Which non-preemptive policy executes ready jobs in their arrival order? | a |
| 16 | 2 | 2561 | E03 หน้า 3 ข้อ 7 | Starting with one process, every process executes two successful calls: fork(); fork(); then prints once. How many prints occur in total? Assume no earlier buffered output. | d |
| 17 | 3 | 2022 | E05 หน้า 4 ข้อ 17 | Which statement about standard MLFQ is NOT true? | a |
| 18 | 6 | 2022 | E05 หน้า 4 ข้อ 18 | Which statement about virtual memory is NOT true? | c |
| 19 | 1 | 2022 | E05 หน้า 3 ข้อ 3 | Which statement describes CPU virtualization provided by a modern operating system? | a |
| 20 | 4 | 2022 | E05 หน้า 4 ข้อ 20 | Which statement about memory allocation is true? | b |
| 21 | 3 | 2022 | E05 หน้า 4 ข้อ 21 | What does a CPU process-selection algorithm select? | c |
| 22 | 6 | 2022 | E05 หน้า 4 ข้อ 22 | What does a page-replacement algorithm select? | a |
| 23 | 2 | 2561 | E03 หน้า 3 ข้อ 6 | Which of the following calls does not return to the original calling point when it succeeds? | b |
| 24 | 5 | 2022 | E05 หน้า 4 ข้อ 24 | What is a disadvantage of basic segmentation? | b |
| 25 | 6 | 2022 | E05 หน้า 4 ข้อ 26 | What does demand paging mean? | c |
| 26 | 6 | 2022 | E05 หน้า 5 ข้อ 27 | Which is NOT a normal step in handling a legal, not-present page fault? | d |
| 27 | 5 | 2022 | E05 หน้า 5 ข้อ 29 | Which pair is used to relocate and bounds-check an address in a segment? | d |
| 28 | 5 | 2022 | E05 หน้า 5 ข้อ 30 | For a fixed virtual-address-space size and fixed PTE size, what is an effect of increasing the page size? | a |
| 29 | 3 | 2022 | E05 หน้า 5 ข้อ 34 | Which scheduling policy does not require timer-driven preemption? | d |
| 30 | 6 | 2022 | E05 หน้า 5 ข้อ 35 | Where can virtual-memory pages be kept when they are not resident in RAM? | b |
| 31 | 3 | 2022 | E05 หน้า 5 ข้อ 36 | What is response time in CPU scheduling? | c |
| 32 | 3 | 2022 | E05 หน้า 5 ข้อ 37 | What is turnaround time? | a |
| 33 | 4 | 2022 | E05 หน้า 5 ข้อ 38 | Which problem can arise with variable-size contiguous partitions? | d |
| 34 | 5 | 2022 | E05 หน้า 5 ข้อ 39 | With a fixed page size and PTE size, what happens to a full single-level page table when the virtual address space becomes larger? | b |
| 35 | 5 | 2022 | E05 หน้า 5 ข้อ 40 | Why can a multilevel page table save memory? | a |
| 36 | 3 | 2022 | E05 หน้า 6 ข้อ 44 | What is a possible disadvantage of SJF when short jobs keep arriving? | c |
| 37 | 5 | 2022 | E05 หน้า 6 ข้อ 47 | Which statement about basic segmentation is NOT true? | d |
| 38 | 5 | 2022 | E05 หน้า 6 ข้อ 48 | Which statement about paging is true? | b |
| 39 | 6 | 2022 | E05 หน้า 6 ข้อ 49 | Which replacement policy requires future page references to make its ideal decisions? | c |
| 40 | 6 | 2022 | E05 หน้า 6 ข้อ 50 | When does a demand-paging page fault occur? | a |
| 41 | 3 | 2022 | E05 หน้า 6 ข้อ 51 | Which policy rotates equal-priority ready jobs using a fixed time quantum? | c |

## Short Answer: 10 ข้อ

| ข้อ | Lecture | แนวอ้างอิง | คำถาม |
|---:|---:|---|---|
| 1 | 3 | L3 MLFQ and STCF; E09 Q17; E06 p23-24 Q24 | Write the full names of MLFQ and STCF. |
| 2 | 2 | E10 p1 Q6 | What is the difference between a process and a program? |
| 3 | 5 | L5 address translation; E09 Q23; E06 p25 Q30 | Expand MMU and state its address-translation function. |
| 4 | 2 | E10 p2 Q9 | Give two examples of CPU state saved during a context switch. |
| 5 | 2 | E10 p2 Q10 | Give two types of information stored in a PCB, other than CPU register values. |
| 6 | 2 | E10 p2 Q13 | What is an exited child process called before its living parent reaps its exit status? |
| 7 | 2 | E10 p2 Q15 (adapted to task examples); L2 I/O-bound/CPU-bound | Give one example each of an I/O-bound task and a CPU-bound task. |
| 8 | 3 | E10 p3 Q19 | Why is longest-job-first usually a poor policy for reducing average turnaround time? |
| 9 | 4 | L4 base/bounds; E10 p11 fragmentation/address protection | With base = 16 KiB and bound = 4 KiB, is virtual byte address 4200 valid? Why? |
| 10 | 5 | L5 TLB; E09 Q23 | Expand TLB and explain why a TLB miss need not cause a page fault. |

## Written Questions: 8–4–8 คะแนน

รวมโจทย์ไว้หน้า 10 โดย Part III ปรากฏเฉพาะหน้านี้ หน้า 11–12 ใช้ทด ส่วนคำตอบจริงยังทำในสมุดคำตอบ

1. Scheduling (8): E10 หน้า 4–5; ตาราง bursts/priority, arrivals 0, FIFO/SJF/RR q=1ms, turnaround, response และ averages ครบ
2. MLFQ bank analogy (4): E10 หน้า 6; algorithms/policies, suggestions, average turnaround ครบ
3. Replacement/EAT (8): E05 หน้า 2; 3 frames, FIFO/LRU/OPT, reference string 20 ตัว, 10 ns/10 ms ครบ จัดเป็น (a) ตาราง+H/F 4.5, (b) faults/hits/probability 1.5, (c) EAT 2 คะแนน

## Single-answer review

- ไม่มี All of the above หรือ Both a and b
- 5 ข้อจากปี 2561: PID (ใหม่ 3), PC (4), process state (10), fork count (16), successful exec (23)
- ปรับ qualifier เพื่อตัดความกำกวม เช่น conventional stack layout, successful exec, legal/not-present page, non-preemptive และ fixed page/PTE sizes
- รอบนี้ข้อใหม่ 13 ผูก E05 Q13 (PCB) และข้อใหม่ 19 ผูก E05 Q3 (CPU virtualization) แทนโจทย์เดิมที่มาจาก Backroom เท่านั้น
- คำตอบในเล่มเฉลยตรวจตามเนื้อหา Lecture ไม่คัด annotation ผิดมาทั้งหมด

## การคัดออก

- ข้อ 45 ของภาพปี 2022 ซ้ำข้อ 44 จึงใช้เพียงข้อ 44
- ไม่ใช้การเหมารวม storage-class speed หรือ Windows/Linux claims ที่กำกวม
- ไม่ใช้คำอ้าง policy ดีที่สุดเสมอโดยไม่ระบุ workload
- ไม่เพิ่ม threads/locks/semaphore/deadlock นอก Lecture 1–6
