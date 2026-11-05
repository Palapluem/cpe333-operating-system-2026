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

| ไฟล์ | การใช้ |
|---|---|
| `02-demo-terminal-capture.txt` | Transcript รอบล่าสุด มี workload checkpoints, samples พร้อม rates และ exit summary; แสดง inline ในเนื้อหา |
| `terminal/04-regression-terminal.png` | ภาพ Terminal ของผล regression; แสดงข้างตาราง regression |
| `terminal/05-pfstat-report-terminal.png` | ตัวอย่าง `pfstat` พร้อม VMA, virtual size, RSS, fault counts และ mapping groups; แสดงข้างคำอธิบาย |
| `experiment-results/` | Raw results ของ E1–E8 ซึ่งรองรับตารางและคำอธิบายในเนื้อหา |
| `04-sigchld-cleanup.txt` | Output ของ process summary และสถานะ idle หลัง cleanup; แสดง inline |

Transcript demo เป็นข้อความที่บันทึกจาก Terminal ไม่ใช่ภาพหน้าจอ ส่วนภาพที่รวมไว้เป็นภาพ Terminal ที่ใช้ในรายงานโดยตรง

ไฟล์จับหน้าจอเต็มเดสก์ท็อป, ภาพ Terminal ที่ตัดมาไม่ครบหรือมีตัวเลขจากรอบเก่า และ log ก่อน merge เป็นหลักฐานระหว่างทำงานเท่านั้น จึงเก็บไว้ในเครื่องและไม่รวมในชุดรายงานของ repo

## ข้อจำกัด

- ไม่มี GitHub CI checks ตั้งไว้สำหรับ branch นี้ ผลเป็นการ build/test ด้วยตนเองใน Lima VM
- ทดสอบเฉพาะ Linux 6.8 ARM64 และ configuration ที่บันทึกไว้
- Build มี compiler-name/clock-skew warnings และข้าม BTF เพราะไม่มี `vmlinux`; build/load จบสำเร็จ
- ไม่ได้ทดสอบใน UTM; โจทย์ไม่ได้กำหนดให้ใช้ UTM
