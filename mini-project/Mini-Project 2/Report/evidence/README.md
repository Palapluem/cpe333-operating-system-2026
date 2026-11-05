# หลักฐานการตรวจ Mini-Project 2

## ชุดหลักหลัง merge

`post-merge-5fbcb76/` เป็นผลจากการตรวจ source บน branch `main` หลัง PR #11 ถูก merge ด้วย commit `5fbcb7679298f36e2bae8b7cd3dbe6bf6a609800` วันที่ 4 พฤศจิกายน 2569

- Environment: Lima, Ubuntu 24.04.5, Linux 6.8.0-142-generic, ARM64, `CONFIG_KPROBES=y`, `CONFIG_KRETPROBES=y`, `CONFIG_BSD_PROCESS_ACCT=y`
- Build/load: `make clean && make all && make load` สำเร็จ
- Demo: จบด้วย exit 0 และ minor/major faults ตรงกับ `getrusage()` หลังหัก baseline
- Regression: retarget, PID reuse, thread exit 100 รอบ, lifetime reads 20,000 ครั้ง และ unload ระหว่าง blocked fault ผ่าน
- Cleanup: `SIGCHLD=SIG_IGN` ที่สืบทอดจาก parent ผ่าน; target กลับ idle และ follow กลับเป็น N
- Experiments: E1–E8 จบด้วย exit status 0; ผลเทียบ process-only กับ waited descendants อธิบายตาม scope
- Make clean: ลบ test binaries หลังจบการตรวจ

ไฟล์ระดับบนเก็บ log ของ environment, build/load, demo, regression, cleanup และ experiments ส่วน `experiment-results/` เก็บผลดิบของแต่ละกรณี E1–E8

## หลักฐานที่รวมในรายงาน

ภาพทั้งหกใบครอปเฉพาะผลลัพธ์ใน Terminal ไม่มีภาพเต็มเดสก์ท็อป ภาพแสดงหลักฐานสำคัญของแต่ละช่วง ส่วนคำสั่งและ output ฉบับเต็มเก็บเป็นไฟล์ข้อความเพื่อให้อ่าน ค้นหา และเทียบตัวเลขได้ครบ

| ไฟล์ | หลักฐานที่แสดง | ตำแหน่งในรายงาน |
|---|---|---|
| `terminal/01-kernel-options-terminal.png` | kernel options ที่จำเป็นสำหรับ kprobes และ process accounting; kernel version กับ architecture อยู่ใน environment log | Problem 2, Step 1: Test environment and method |
| `terminal/02-build-load-terminal.png` | การโหลดโมดูลและ proc interfaces | Problem 2, Step 1: Build and load |
| `terminal/03-demo-terminal.png` | exit summary จาก demo อีกรอบหนึ่ง (16,649 minor / 6,145 major); ไม่ใช่ตัวเลขจาก transcript รอบล่าสุด | Problem 2, Step 1: End-to-end demo |
| `terminal/04-regression-terminal.png` | ผล retarget, PID reuse, thread exit, lifetime reads และ unload | Problem 2, Step 3: Post-merge checks |
| `terminal/05-pfstat-report-terminal.png` | VMA, virtual size, RSS, fault counts และ mapping groups | Problem 1, Step 2: How the tool works |
| `terminal/06-experiments-terminal.png` | รายการกรณี E1–E8 ที่สคริปต์ทดลองเรียกใช้ | Problem 2, Step 1: How we checked the results |

`02-demo-terminal-capture.txt` เป็นแหล่งตัวเลขหลักของ demo รอบล่าสุด: 16,782 minor และ 4,097 major faults พร้อม workload checkpoints, interval samples และ rates ภาพ `03-demo-terminal.png` เป็นตัวอย่างจากอีกรอบซึ่งมีผลต่างกันตาม cache state จึงติดป้ายแยกไว้ในรายงาน รายละเอียด E1–E8 อยู่ใน `experiment-results/` และ `04-sigchld-cleanup.txt` เก็บผลตรวจ cleanup ที่รับ `SIGCHLD=SIG_IGN` มาจาก parent

ไฟล์จับหน้าจอเต็มเดสก์ท็อป ภาพจากรอบเก่าที่ตัวเลขไม่ตรงกับ post-merge run และ log review ก่อน merge ถูกตัดออกจากชุดส่งงาน

## ข้อจำกัด

- ไม่มี GitHub CI checks ตั้งไว้สำหรับ branch นี้ ผลเป็นการ build/test ด้วยตนเองใน Lima VM
- ทดสอบเฉพาะ Linux 6.8 ARM64 และ configuration ที่บันทึกไว้
- Build มี compiler-name/clock-skew warnings และข้าม BTF เพราะไม่มี `vmlinux`; build/load จบสำเร็จ
- ไม่ได้ทดสอบใน UTM; โจทย์ไม่ได้กำหนดให้ใช้ UTM
