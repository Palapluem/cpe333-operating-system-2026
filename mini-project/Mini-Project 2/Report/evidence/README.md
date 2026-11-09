# หลักฐานการตรวจ Mini-Project 2

## ชุดหลักหลัง merge

`post-merge-5fbcb76/` เป็นผลจากการตรวจ source บน branch `main` หลัง PR #11 ถูก merge ด้วย commit `5fbcb7679298f36e2bae8b7cd3dbe6bf6a609800` วันที่ 4 พฤศจิกายน 2569

- Environment: Lima, Ubuntu 24.04.5, Linux 6.8.0-142-generic, ARM64, `CONFIG_KPROBES=y`, `CONFIG_KRETPROBES=y`, `CONFIG_BSD_PROCESS_ACCT=y`
- Build/load: `make clean && make all && make load` สำเร็จ
- Demo: จบด้วย exit 0; ภาพ `03-demo-terminal.png` และ transcript แสดง run PID 2508, 16,521 minor และ 8,193 major faults ซึ่งตรงกับ `getrusage()` หลังหัก baseline
- Regression: retarget, PID reuse, thread exit 100 รอบ, lifetime reads 20,000 ครั้ง และ unload ระหว่าง blocked fault ผ่าน
- Cleanup: `SIGCHLD=SIG_IGN` ที่สืบทอดจาก parent ผ่าน; ภาพและ transcript ของ PID 2513 แสดง 125 minor faults, target กลับ idle และ follow กลับเป็น N
- Experiments: E1–E8 จบด้วย exit status 0; ผลเทียบ process-only กับ waited descendants อธิบายตาม scope
- Make clean: ลบ test binaries หลังจบการตรวจ

ไฟล์ระดับบนเก็บ log ของ environment, build/load, demo, regression, cleanup และ experiments ส่วน `experiment-results/` เก็บผลดิบของแต่ละกรณี E1–E8

## หลักฐานที่รวมในรายงาน

ภาพทั้งแปดใบเป็นภาพจับหน้าจอที่ครอปเฉพาะผลลัพธ์ใน Terminal ไม่มีภาพเต็มเดสก์ท็อป และแสดงหลักฐานของแต่ละช่วง ภาพ demo, E7 และ SIGCHLD cleanup จับจากรอบเดียวกับ transcript ของแต่ละงาน โดย PID และผลลัพธ์ตรงกัน ไฟล์ `.txt` เก็บผลที่บันทึกไว้ รวมคำสั่ง PID เวลา exit status และค่าผลลัพธ์เท่าที่มีในแต่ละรายการ ส่วนรายงาน `pfstat` ของ shell PID 1622 มีเฉพาะภาพ

| ไฟล์ | หลักฐานที่แสดง | ตำแหน่งในรายงาน |
|---|---|---|
| `terminal/01-kernel-options-terminal.png` | kernel options ที่จำเป็นสำหรับ kprobes และ process accounting; kernel version กับ architecture อยู่ใน environment log | Problem 2, Step 1: Test environment and method |
| `terminal/02-build-load-terminal.png` | การโหลดโมดูลและ proc interfaces | Problem 2, Step 1: Build and load |
| `terminal/03-demo-terminal.png` | interval samples และ exit summary จาก demo run PID 2508 (16,521 minor / 8,193 major), ตรงกับ `02-demo-terminal-capture.txt` | Problem 2, Step 1: End-to-end demo |
| `terminal/04-regression-terminal.png` | ผล retarget, PID reuse, thread exit, lifetime reads และ unload; ภาพแสดง PID 2613 ส่วน log แสดง PID 2579 | Problem 2, Step 3: Post-merge checks |
| `terminal/05-pfstat-report-terminal.png` | VMA, virtual size, RSS, fault counts และ mapping groups ของ bash PID 1622 (มีเฉพาะภาพ ไม่มี transcript) | Problem 1, Step 2: How the tool works |
| `terminal/06-experiments-terminal.png` | รายการกรณี E1–E8 ที่สคริปต์ทดลองเรียกใช้ | Problem 2, Step 1: How we checked the results |
| `terminal/07-e7-timeline-terminal.png` | interval samples และ exit summary จาก E7 run PID 2286, ตรงกับ `experiment-results/e7-timeline.txt` | Problem 2, Step 2: E7 virtual size and RSS over time |
| `terminal/08-sigchld-cleanup-terminal.png` | `pfcount run` ของ PID 2513 และสถานะหลัง cleanup: `follow=N`, `pid: 0`, `state: idle` | Problem 2, Step 3: Post-merge checks |

`02-demo-terminal-capture.txt` เป็น transcript ฉบับเต็มของ demo run PID 2508 (16,521 minor / 8,193 major faults) พร้อม workload checkpoints, interval samples และ rates ภาพและ transcript เป็นการรันรอบเดียวกัน ส่วน `experiment-results/e7-timeline.txt` เป็น transcript ของ E7 run PID 2286 ซึ่งรันคำสั่งเดียวกันแยกจากรอบสคริปต์ที่ได้ E1–E6 และ E8 (PID 10605–10663) และ `04-sigchld-cleanup.txt` เก็บผล run PID 2513 ที่รับ `SIGCHLD=SIG_IGN` มาจาก parent; ทั้งสองรายการมีภาพ Terminal ที่ตรงกับตัวเลขและสถานะใน transcript

log review ก่อน merge ไม่รวมอยู่ในชุดส่งงาน

## ข้อจำกัด

- ไม่มี GitHub CI checks ตั้งไว้สำหรับ branch นี้ ผลเป็นการ build/test ด้วยตนเองใน Lima VM
- ทดสอบเฉพาะ Linux 6.8 ARM64 และ configuration ที่บันทึกไว้
- ไม่ได้ทดสอบใน UTM; โจทย์ไม่ได้กำหนดให้ใช้ UTM
