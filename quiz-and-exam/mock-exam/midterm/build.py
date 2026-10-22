#!/usr/bin/env python3
"""Rebuild the unchanged cover -> chapters -> pdfpages publication workflow.

Only questions.generated.tex / solutions.generated.tex are generated text.
Authored templates and question-bank.json are the editable sources of truth.
Requires Python 3.10+, PyMuPDF, XeLaTeX, exam.cls, polyglossia and Inkscape.
"""
import argparse
from collections import deque
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parent
BANK = json.loads((ROOT / "question-bank.json").read_text())


def tex(value):
    table = {"\\":r"\textbackslash{}", "&":r"\&", "%":r"\%", "$":r"\$",
             "#":r"\#", "_":r"\_", "{":r"\{", "}":r"\}",
             "~":r"\textasciitilde{}", "^":r"\textasciicircum{}"}
    return "".join(table.get(c, c) for c in str(value))


def scheduling(policy):
    bursts = BANK["scheduling"]["bursts"]
    remaining = bursts.copy()
    queue = deque(sorted(range(5), key=lambda i: (bursts[i], i)) if policy == "SJF" else range(5))
    t, trace, first, completion = 0, [], {}, {}
    while queue:
        i = queue.popleft()
        first.setdefault(i, t)
        run = min(remaining[i], 1) if policy == "RR" else remaining[i]
        trace.append((t, t + run, i + 1))
        t += run
        remaining[i] -= run
        if remaining[i]:
            queue.append(i)
        else:
            completion[i] = t
    tat = [completion[i] for i in range(5)]  # All arrivals zero.
    response = [first[i] for i in range(5)]
    wait = [tat[i] - bursts[i] for i in range(5)]
    return dict(trace=trace, turnaround=tat, response=response, waiting=wait,
                mean_tat=sum(tat)/5, mean_response=sum(response)/5,
                mean_wait=sum(wait)/5)


def replacement(policy):
    refs = BANK["replacement"]["reference"]
    frames, fifo, last, rows, faults = [None]*3, deque(), {}, [], 0
    for t, page in enumerate(refs):
        hit = page in frames
        if not hit:
            faults += 1
            if None in frames:
                slot = frames.index(None)
            elif policy == "FIFO":
                slot = fifo.popleft()
            elif policy == "LRU":
                slot = min(range(3), key=lambda i: last[frames[i]])
            else:
                def next_use(i):
                    try:
                        return refs.index(frames[i], t+1)
                    except ValueError:
                        return float("inf")
                # Tie: lowest numbered frame, so the printed trace is reproducible.
                slot = max(range(3), key=lambda i: (next_use(i), -i))
            frames[slot] = page
            if policy == "FIFO":
                fifo.append(slot)
        last[page] = t
        rows.append(dict(frames=frames.copy(), hit=hit))
    return dict(rows=rows, faults=faults, hits=len(refs)-faults)


def validate_bank():
    assert [q["n"] for q in BANK["mcq"]] == list(range(1,42))
    assert [q["n"] for q in BANK["short"]] == list(range(1,11))
    assert BANK["mcq_points"] + BANK["short_points"] + sum(BANK["essay_points"]) == 50
    assert len(BANK["essay_points"]) == 3
    assert BANK["essay_points"] == [8,4,8]
    assert len({q["q"] for q in BANK["mcq"]}) == 41
    assert sum(q["source_year"]==2561 for q in BANK["mcq"]) == 5
    assert sum(q["source_year"]==2022 for q in BANK["mcq"]) == 36
    assert len({(q["source_year"],q["source_question"]) for q in BANK["mcq"]}) == 41
    # These numerical essay assumptions are printed explicitly in the standard
    # template; changing them requires updating the prompt and expected results.
    assert BANK["scheduling"] == dict(bursts=[10,1,2,1,5],priorities=[3,1,3,4,2],arrival=0,quantum=1)
    assert BANK["replacement"] == dict(reference=[7,0,1,3,0,3,2,4,2,7,0,3,2,1,2,0,1,4,0,1],frames=3,memory_ns=10,fault_ns=10000000)
    for q in BANK["mcq"]:
        assert len(q["choices"]) == len(set(q["choices"])) == 4
        assert q["answer"] in "abcd" and 1 <= q["lecture"] <= 6
        assert not any(re.search(r"\ball of the above\b|\bboth [a-d] and [a-d]\b",c,re.I) for c in q["choices"])
    assert scheduling("FIFO")["turnaround"] == [10,11,13,14,19]
    assert scheduling("SJF")["turnaround"] == [19,1,4,2,9]
    assert scheduling("RR")["turnaround"] == [19,2,7,4,14]
    assert scheduling("RR")["response"] == [0,1,2,3,4]
    assert [replacement(p)["faults"] for p in ("FIFO","LRU","OPT")] == [13,13,10]


def exam_source():
    out = []
    offset = 0
    for page, count in enumerate([6, 6, 6, 6, 6, 6, 5]):
        group = BANK["mcq"][offset:offset+count]
        offset += count
        if page == 0:
            out.append(r"\sectiontitle{Part I: Multiple Choice (20 points)}")
            out.append(r"\noindent Circle the one correct answer in each question.\par\smallskip")
        out.append(r"\begin{questions}\setlength{\itemsep}{0.12cm}\setcounter{question}{"+str(group[0]["n"]-1)+"}")
        for q in group:
            out.append(r"\question "+tex(q["q"]))
            out.append(r"\begin{verticalchoices}")
            out.extend(r"\item "+tex(c) for c in q["choices"])
            out.append(r"\end{verticalchoices}")
        out.append(r"\end{questions}\vfill\newpage")
    out.append(r"\sectiontitle{Part II: Short Answer (10 points)}")
    out.append(r"\noindent Answer all questions briefly in the spaces provided. (1 point each.)\par\smallskip")
    out.append(r"\begin{questions}\setlength{\itemsep}{0.12cm}")
    for q in BANK["short"]:
        out.append(r"\question "+tex(q["q"])+r"\par\vspace{0.90cm}")
    out.append(r"\end{questions}\vfill\newpage")
    out.append(r"""
\sectiontitle{Part III: Written Questions (20 points)}
\noindent Answer all three questions in the answer booklet. Show your work.\par\smallskip
\begin{questions}
\question \textbf{(8 points)} Consider the following set of processes (jobs), where the run time of each process is given in milliseconds (ms):
\begin{center}
\renewcommand{\arraystretch}{1.0}
\begin{tabular}{c|c|c}
Process & Run time (ms) & Priority \\\hline
$P_1$ & 10 & 3 \\
$P_2$ & 1 & 1 \\
$P_3$ & 2 & 3 \\
$P_4$ & 1 & 4 \\
$P_5$ & 5 & 2
\end{tabular}
\end{center}
The processes arrive in the order $P_1,P_2,P_3,P_4,P_5$, all at time 0. Assume zero context-switch overhead; break SJF ties by arrival order.
\begin{parts}
\part[3] Draw execution diagrams for FIFO, SJF, and RR scheduling with time slice = 1 ms.
\part[2] Find the turnaround time of each process under each policy.
\part[2] Find the response time of each process under each policy.
\part[1] Which policy gives (i) the minimum average turnaround time and (ii) the minimum average response time? Calculate both averages for all three policies.
\end{parts}

\question \textbf{(4 points)} Explain how a commercial bank handles customers during rush hours with the concept of the Multi-level Feedback Queue (MLFQ), in your opinion. Describe the algorithms and policies used and provide suggestions on how to improve the process with the goal of optimizing the average turnaround time of customers.

\question \textbf{(8 points)} Use three initially empty frames and this page-reference string (20 references):
\begin{center}
\textbf{7, 0, 1, 3, 0, 3, 2, 4, 2, 7, 0, 3, 2, 1, 2, 0, 1, 4, 0, 1}
\end{center}
Assume memory-access time is 10 ns and disk-access time is 10 ms. For EAT, treat 10 ms as the complete fault-path cost (including restart) and ignore other costs.
\begin{parts}
\part \textbf{(4.5 points)} Draw FIFO, LRU, and OPT frame tables; mark each reference as a hit or fault.
\part \textbf{(1.5 points)} Find each policy's total faults, total hits, and fault probability.
\part[2] Calculate the effective access time (EAT) of each policy in milliseconds.
\end{parts}
\end{questions}
\vfill\newpage
% Pages 11 and 12 are intentionally blank scratch pages. Written answers still
% belong in the separate answer booklet, as specified on the unchanged cover.
\null\vfill\newpage
\null\vfill
""")
    return "\n".join(out)


def table(headers, rows, spec=None):
    spec = spec or ("l" + "r"*(len(headers)-1))
    return (r"\begin{center}\renewcommand{\arraystretch}{1.15}\begin{tabular}{"+spec+"}\n"+
            " & ".join(headers)+r"\\\hline"+"\n"+
            "\n".join(" & ".join(str(c) for c in row)+r"\\" for row in rows)+
            "\n"+r"\end{tabular}\end{center}")


def gantt(result):
    # Scale every interval proportionally, including the one-ms RR slices.
    out = [r"\begin{center}\begin{tikzpicture}[x=0.75cm,y=0.65cm]"]
    for a,b,p in result["trace"]:
        out.append(rf"\draw ({a},0) rectangle ({b},1);\node at ({(a+b)/2},.5) {{$P_{p}$}};")
    boundaries = [s[0] for s in result["trace"]]+[result["trace"][-1][1]]
    for t in boundaries:
        out.append(rf"\node[below,font=\scriptsize] at ({t},0) {{{t}}};")
    out.append(r"\end{tikzpicture}\end{center}")
    return "\n".join(out)


def solutions_source():
    out = [r"\sectiontitle{เฉลยและเกณฑ์ตรวจ: CPE333 Mock Midterm ชุดที่ 1}",
           r"\noindent สำหรับตรวจหลังทำข้อสอบเท่านั้น ไม่ใช่เฉลยข้อสอบจริงของรายวิชา\\คะแนนรวม 50: ปรนัย $20c/41$ เมื่อ $c$ คือจำนวนข้อถูก; เติมคำ 10; อัตนัย $8+4+8=20$\\ไม่ปัดคะแนนรายข้อ; เมื่อสรุปผลจึงปัดคะแนนรวมเป็นทศนิยมสองตำแหน่ง ไม่มีการหักคะแนนตอบผิด\par\medskip"]
    for start,end in [(0,11),(11,22),(22,32),(32,41)]:
        if start:
            out.append(r"\newpage\sectiontitle{เฉลยส่วนที่ 1 (ต่อ)}")
        else:
            out.append(r"\sectiontitle{เฉลยส่วนที่ 1: คำตอบเดียวที่ดีที่สุด}")
        out.append(r"\begin{enumerate}[leftmargin=1.4em,start="+str(start+1)+",itemsep=0.18cm]")
        for q in BANK["mcq"][start:end]:
            out.append(r"\item \textbf{("+q["answer"]+")} "+tex(q["why"])+
                       r" {\small [L"+str(q["lecture"])+"]}")
        out.append(r"\end{enumerate}")
    out.append(r"\newpage\sectiontitle{เฉลยส่วนที่ 2: เติมคำ / ตอบสั้น}")
    out.append(r"\noindent ข้อละ 1 คะแนน ให้ partial credit ตามองค์ประกอบในแต่ละข้อ; รับถ้อยคำอื่นที่มีความหมายถูกต้อง ไม่บังคับจำประโยคเฉลย\par\smallskip")
    out.append(r"\begin{enumerate}[leftmargin=1.4em,itemsep=.25cm]")
    for q in BANK["short"]:
        if q["n"] == 6:
            out.append(r"\end{enumerate}\newpage\sectiontitle{เฉลยส่วนที่ 2: Short Answer (ต่อ)}\begin{enumerate}[leftmargin=1.4em,start=6,itemsep=.25cm]")
        out.append(r"\item \textbf{"+tex(q["answer"])+r"}\\"+tex(q["accept"])+"; "+tex(q["why"]))
    out.append(r"\end{enumerate}\newpage\sectiontitle{เฉลยอัตนัยข้อ 1: CPU Scheduling (8 คะแนน)}")
    out.append(r"\noindent Burst = (10,1,2,1,5) ms; arrival = 0 ทุกงาน; quantum = 1 ms; SJF ใช้ลำดับเดิมเมื่องานยาวเท่ากัน\par")
    for policy in ("FIFO","SJF","RR"):
        out.append(r"\noindent\textbf{"+policy+"}")
        out.append(gantt(scheduling(policy)))
    out.append(r"\noindent RR ยังคงมีจุดแบ่ง quantum แม้เหลือเพียง $P_1$; จะรวมช่วงติดกันของ $P_1$ ตอนท้ายก็ได้ถ้าระบุ quantum ถูกต้อง\par\medskip")
    out.append(r"\noindent\textbf{นิยามที่ใช้}\\$T_i=C_i-A_i$; $R_i=S_i-A_i$; $W_i=T_i-B_i$ (กรณีมี CPU burst เดียว ไม่มี I/O)\\$C$: completion, $A$: arrival, $S$: first start, $B$: CPU burst\\Response time ไม่ใช่ total waiting time โดยเฉพาะเมื่อใช้ RR\par")
    out.append(r"\newpage\sectiontitle{เฉลยอัตนัยข้อ 1 (ต่อ): ตารางและเกณฑ์ตรวจ}")
    for key,title in [("turnaround","Turnaround time (ms)"),("response","Response time (ms)"),("waiting","Waiting time (ms) - เพิ่มเพื่อเทียบ ไม่ได้ถามให้คำนวณ")]:
        out.append(r"\noindent\textbf{"+title+"}")
        out.append(table(["Policy"]+[rf"$P_{i}$" for i in range(1,6)],[[p]+scheduling(p)[key] for p in ("FIFO","SJF","RR")]))
    out.append(table(["Policy","Average turnaround","Average response"],[[p,f'{scheduling(p)["mean_tat"]:.1f} ms',f'{scheduling(p)["mean_response"]:.1f} ms'] for p in ("FIFO","SJF","RR")]))
    out.append(r"\noindent\textbf{สรุป:} SJF ให้ average turnaround ต่ำสุด 7.0 ms; RR ให้ average response ต่ำสุด 2.0 ms สำหรับ workload นี้เท่านั้น\par\medskip")
    out.append(r"""\noindent\textbf{Rubric รวม 8 คะแนน}
\begin{itemize}[leftmargin=1.4em,itemsep=.12cm]
\item (a) 3 คะแนน: FIFO, SJF, RR อย่างละ 1; แต่ละอันให้ .5 สำหรับลำดับและ .5 สำหรับขอบเวลาถูกต้อง
\item (b) 2 คะแนน: ตาราง turnaround 15 ค่า ค่าละ $2/15$ คะแนน
\item (c) 2 คะแนน: ตาราง response 15 ค่า ค่าละ $2/15$ คะแนน
\item (d) 1 คะแนน: ค่าเฉลี่ยทั้ง 6 ค่าละ .1 และเลือก policy ต่ำสุดถูกต้องอีก metric ละ .2
\end{itemize}
\noindent หากผิดจาก arithmetic ครั้งเดียวแต่ขั้นถัดไปใช้วิธีถูก ให้ follow-through credit โดยไม่หักซ้ำ; ไม่ให้ครบในส่วนที่ใช้นิยาม response ผิดเป็น waiting
\newpage\sectiontitle{เฉลยอัตนัยข้อ 2: MLFQ กับธนาคาร (4 คะแนน)}
\noindent\textbf{เกณฑ์ตรวจภาพรวม: กฎ MLFQ และการเทียบกับธนาคาร (2 คะแนน; ข้อละ .4)}
\begin{enumerate}[leftmargin=1.4em,itemsep=.18cm]
\item Priority สูงกว่าจะได้บริการก่อน: เลือกคิวระดับสูงสุดที่มีลูกค้าพร้อมทำรายการ
\item Priority เท่ากันใช้ RR: ให้บริการเป็นช่วงแล้วหมุนเวียนเมื่อถึงจุดพักที่ปลอดภัย หากยังทำไม่เสร็จ
\item งานใหม่เริ่มที่คิวบนสุด: ลูกค้าใหม่มีโอกาสจบรายการสั้นเร็ว โดยยังไม่ต้องรู้ service time ล่วงหน้า
\item เมื่อใช้ allotment สะสมของระดับนั้นครบ ให้ลด priority หนึ่งระดับ แม้เคยพัก/yield ก่อนหมด slice; ระดับล่างสุดคงอยู่ระดับเดิม
\item ทุกช่วงเวลา $S$ ให้ boost งานที่ยังไม่เสร็จกลับคิวบนสุด ป้องกันงานยาวอดรอ และรองรับพฤติกรรมงานที่เปลี่ยนไป
\end{enumerate}
\noindent\textbf{ตัวอย่าง policy ที่ใช้งานได้ (1 คะแนน)}\\
ตัวเลขและจำนวนระดับต่อไปนี้เป็นตัวอย่าง ไม่ใช่ค่าที่โจทย์บังคับ; ให้คะแนนจากความสอดคล้องของ policy และการใช้ feedback ไม่ใช่การใช้ตัวเลขเหมือนเฉลย
\begin{itemize}[leftmargin=1.4em,itemsep=.12cm]
\item ใช้ Q0, Q1, Q2 ตามลำดับสูงไปต่ำ; slice เท่ากับ 2, 4, 8 นาที; allotment ของ Q0/Q1 เท่ากับ 2/4 นาที ส่วน Q2 หมุน RR จนจบ (.25)
\item ลูกค้าใหม่เข้า Q0, จบรายการสั้นก็ออกจากระบบ; งานที่ใช้เวลาใน Q0 สะสมครบ 2 นาทีลง Q1 และครบ 4 นาทีใน Q1 ลง Q2 (.25)
\item เมื่องาน priority สูงกว่ามาถึง ให้พักงานต่ำกว่า ณ safe stage boundary ถัดไป บันทึก progress และเวลาสะสมไว้ ไม่เริ่ม financial update ค้างครึ่งทาง (.25)
\item ตั้ง boost เช่นทุก 20 นาที และคงลำดับเข้าคิวอย่างเป็นธรรม; งาน blocked รอเอกสารไม่ควรยึด counter เมื่อกลับมาพร้อมต้องใช้กติกา boost/accounting ที่ประกาศชัด (.25)
\end{itemize}
\noindent\textbf{ข้อเสนอปรับปรุงและผลต่อ turnaround (1 คะแนน)}\\
ให้ .5 สำหรับข้อเสนอเช่นคัดกรองรายการ, จัดเตรียมเอกสารล่วงหน้า, ลด slice ในคิวสูง, เพิ่ม counter ตามกำลังคน หรือปรับ boost จากข้อมูลเวลารอจริง; อีก .5 สำหรับผลและข้อจำกัด เช่น slice สั้นเพิ่ม overhead, boost ถี่รบกวนงานสั้น, เพิ่ม counter เปลี่ยนเป็นหลาย server และมีต้นทุนเพิ่ม
\par\medskip
\noindent MLFQ ไม่ได้รับประกัน average turnaround ต่ำสุดทุก workload เพราะไม่ทราบความยาวงานล่วงหน้า และธนาคารจริงไม่สามารถ preempt ทุกจุดเหมือน CPU ได้; รับ policy อื่นที่ครบกฎและอธิบายความเป็นไปได้อย่างสอดคล้อง
\newpage\sectiontitle{เฉลยอัตนัยข้อ 3: Page Replacement (8 คะแนน)}
\noindent\textbf{ข้อ (a): ตาราง frames และ hit/fault (4.5 คะแนน)}\\
แสดงสถานะหลังแต่ละ reference; F = fault, H = hit, -- = frame ว่าง\par\smallskip
""")
    refs = BANK["replacement"]["reference"]
    for p in ("FIFO","LRU","OPT"):
        if p == "OPT":
            out.append(r"\newpage\sectiontitle{เฉลยอัตนัยข้อ 3: ตาราง OPT (ต่อ)}")
        r = replacement(p)
        out.append(r"\noindent\textbf{"+p+f': {r["faults"]} faults, {r["hits"]} hits'+"}")
        # Two 10-reference blocks remain legible at the original template font.
        for a,b in [(0,10),(10,20)]:
            headers = ["Ref. no."]+[str(i+1) for i in range(a,b)]
            rows = [["Page"]+refs[a:b]]
            rows += [["Frame "+str(f+1)]+["--" if x["frames"][f] is None else x["frames"][f] for x in r["rows"][a:b]] for f in range(3)]
            rows += [["H/F"]+["H" if x["hit"] else "F" for x in r["rows"][a:b]]]
            out.append(r"{\setlength{\tabcolsep}{5pt}"+table(headers,rows,"l|"+"c"*10)+"}")
    out.append(r"\noindent ตารางตัวอย่าง OPT เลือก frame ต่ำสุดเมื่อตัดสินเสมอ; โจทย์ไม่บังคับ tie-break จึงรับ trace อื่นที่เลือกเหยื่อ optimal และได้จำนวน fault ถูกต้อง\par")
    out.append(r"""\newpage\sectiontitle{เฉลยอัตนัยข้อ 3 (ต่อ): EAT และเกณฑ์ตรวจ}
\noindent\textbf{หน่วยและโมเดลต้นทุน}\\
$m=10$ ns $=0.00001$ ms; $D=10$ ms $=10{,}000{,}000$ ns\\
$D$ รวมเส้นทาง fault และ restarted access ตามโจทย์ จึงใช้
\[\mathrm{EAT}=(1-p)m+pD\]
ไม่บวก $m$ เพิ่มอีกครั้งบนเส้นทาง fault
""")
    out.append(r"\noindent\textbf{ข้อ (b): Faults, hits และ fault probability (1.5 คะแนน); ข้อ (c): EAT (2 คะแนน)}")
    out.append(table(["Policy","Faults","Hits","p","EAT (ms)"],[[p,replacement(p)["faults"],replacement(p)["hits"],f'{replacement(p)["faults"]}/20',f'{(1-replacement(p)["faults"]/20)*.00001+(replacement(p)["faults"]/20)*10:.7f}'] for p in ("FIFO","LRU","OPT")]))
    out.append(r"""\[\mathrm{EAT}_{FIFO}=\mathrm{EAT}_{LRU}=\frac7{20}(10)+\frac{13}{20}(10{,}000{,}000)=6{,}500{,}003.5\ \mathrm{ns}\]
\[\mathrm{EAT}_{OPT}=\frac{10}{20}(10)+\frac{10}{20}(10{,}000{,}000)=5{,}000{,}005\ \mathrm{ns}\]
\noindent ดังนั้น OPT ต่ำสุด; FIFO กับ LRU เท่ากันสำหรับ string นี้ ไม่ได้หมายความว่าจะเท่ากันสำหรับ string อื่น\\รับคำตอบประมาณ 6.5 ms และ 5.0 ms เมื่อมีสูตรและหน่วยถูกต้อง; อย่าใช้ $10^{-3}$ วินาทีแทน 10 ms ซึ่งจริง ๆ เท่ากับ $10^{-2}$ วินาที
\par\medskip
\noindent\textbf{Rubric รวม 8 คะแนน}
\begin{itemize}[leftmargin=1.4em,itemsep=.18cm]
\item ข้อ (a) ตาราง frames รวม 4.5 คะแนน: แต่ละ policy 1.5 คะแนน ให้ 1 สำหรับ frame contents 20 คอลัมน์ (คอลัมน์ละ .05) และ .5 สำหรับ H/F 20 ช่อง (ช่องละ .025)
\item ข้อ (b) จำนวน faults, hits และ probability รวม 1.5 คะแนน: แต่ละ policy ชุดละ .5 คะแนน
\item ข้อ (c) EAT รวม 2 คะแนน: สูตร .5; แปลงหน่วย .5; EAT แต่ละ policy ค่าละ $1/3$ ไม่บังคับเขียนข้อสรุปเพิ่มเติมที่โจทย์ไม่ได้ถาม
\end{itemize}
\noindent ให้ follow-through credit สำหรับ EAT ที่ใช้จำนวน fault จากตารางของผู้สอบอย่างถูกวิธี แม้ตารางก่อนหน้าผิด โดยหักข้อผิดเดิมในตาราง/จำนวน faults; ต้องไม่ให้คะแนนเต็มหากแทนค่าคนละหน่วยในสมการเดียวกัน
\newpage\sectiontitle{แผนผังเนื้อหาและแหล่งอ้างอิงสำหรับตรวจทบทวน}
\noindent\textbf{ความครอบคลุมของปรนัย}
""")
    topics=["Privilege, trap, isolation","Process, state, context switch, wait",
            "FIFO/SJF/STCF/RR, MLFQ, metrics","Fixed/variable partitions, fragmentation",
            "Segmentation, paging, address translation","Virtual memory, demand paging, replacement"]
    out.append(table(["Lecture","จำนวนปรนัย","หัวข้อ"],[[str(i),sum(q["lecture"]==i for q in BANK["mcq"]),topics[i-1]] for i in range(1,7)],"lcl"))
    out.append(r"""\noindent\textbf{แหล่งเนื้อหา (path เทียบกับ root ของ repository)}
\begin{itemize}[leftmargin=1.4em,itemsep=.18cm]
\item lectures/CPE333\_OS\_Midterm\_StudyNotes.pdf และ Lecture1--Lecture6: ใช้กำหนดขอบเขต ไม่รวม threads/locks/deadlock ที่อยู่นอกชุด Lecture 1--6
\item ปรนัย 5 ข้ออิงปี 2561 (E03) และ 36 ข้ออิงปี 2022 (E05) มีเลขข้อ/หน้าต้นทางใน SOURCE\_MAP.md และ question-bank.json; E09 เป็นชุดเนื้อหาซ้ำสำหรับเทียบตัวเลือก ไม่ใช้ annotation เป็นเฉลย
\item quiz-and-exam/midterm/Backroom.pdf และข้อสอบปี 2558/2561: เทียบหัวข้อและแนวคำถาม ไม่คัดลอกหน้าที่มีคำตอบเขียนกำกับ
\item quiz-and-exam/midterm/ยำรวมมิตรข้อเขียน.pdf หน้า 4--6 และ 10: Scheduling, bank analogy และ MLFQ rules; ตัวเลข burst ใช้ 10,1,2,1,5 รวม 19 ms ตามโจทย์ชุดนี้ ไม่ใช่ Quiz อีกชุดที่ $P_4=2$
\item E05: OS-Midterm-2022 ไฟล์ชื่อยาว หน้า 2 ใช้ reference string 20 ตัว, 3 frames, 10 ns/10 ms; หน้า 3--6 เป็นภาพปรนัยถึงข้อ 51 ส่วนหน้าสรุป 7--9 มีถึงข้อ 40 เท่านั้น
\item quiz-and-exam/midterm/Quiz\_BeforeMidterm.pdf: เทียบรูปแบบโจทย์ Scheduling และ fit policy
\end{itemize}
\noindent\textbf{แม่แบบการพิมพ์}\\
Palapluem/cpe222-past-exam-main, commit e87b379d09fdeb54f964d968c9599efdea68ba5d; main wrapper, cover และ chapter templates\\
คงการประกอบ PDF, ฟอนต์ THSarabunNew, margin, student header และกล่องหน้าปก; บรรทัดดอกจันบนปกใช้ข้อความตามแม่แบบที่ผู้ใช้ขอ ไม่ใช่การตรวจยืนยันการรับรองจริง
\par\medskip
\noindent วันและเวลาตามข้อมูลที่ผู้ใช้ให้: 26 ตุลาคม 2569, 09.00--12.00 น. รายละเอียดคะแนนย่อยและเฉลยเป็นเกณฑ์ฝึกซ้อมแยกเล่ม ดู README.md และ question-bank.json สำหรับ provenance
""")
    return "\n".join(out)


def run_xelatex(folder, filename):
    compiler = shutil.which("xelatex")
    if not compiler:
        raise RuntimeError("XeLaTeX not found on PATH")
    # svg/ifplatform shell probes cannot safely use a jobname containing spaces.
    # Keep the standard public filenames, but use a space-free internal jobname.
    jobname = Path(filename).stem.replace(" ", "_")
    for _ in range(2):
        p = subprocess.run([compiler,"-shell-escape","-interaction=nonstopmode",
                            "-halt-on-error","-jobname="+jobname,filename],cwd=folder,stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT,text=True)
        if p.returncode:
            print(p.stdout[-2500:])
            raise RuntimeError(f"XeLaTeX failed: {filename}")
    if jobname != Path(filename).stem:
        shutil.copy2(folder/(jobname+".pdf"),folder/Path(filename).with_suffix(".pdf"))


def verify_pdfs(check_logs=False):
    import pymupdf as fitz
    output = ROOT/"output/pdf/CPE333_Midterm_Mock_Exam.pdf"
    doc = fitz.open(output)
    assert len(doc) == 12, f"Expected exactly 12 pages including cover, got {len(doc)}"
    all_text = "\n".join(p.get_text() for p in doc)
    for i,p in enumerate(doc):
        text = p.get_text()
        assert ("รหัส" if i==0 else "Student ID") in text, f"Missing student ID field page {i+1}"
        assert ("ชื่อ" if i==0 else "Name") in text, f"Missing student name field page {i+1}"
        assert "222" not in text, f"Old subject leaked page {i+1}"
        assert abs(p.rect.width-595.28)<1 and abs(p.rect.height-841.89)<1
        if i:
            assert f"{i+1}/12" in text, f"Wrong page label on page {i+1}"
        for b in p.get_text("blocks"):
            assert b[0]>=-1 and b[1]>=-1 and b[2]<=p.rect.width+1 and b[3]<=p.rect.height+1, f"Text outside paper page {i+1}: {b}"
    assert "41." in all_text and "Operating Systems" in all_text
    assert not re.search(r"[\u0e00-\u0e7f]",exam_source()), "Non-English question text"
    assert "mock" not in all_text.lower()
    assert "20/41" not in doc[0].get_text()
    for pattern,count in [(r"\\question ",54),(r"\\newpage",10)]:
        assert len(re.findall(pattern,exam_source())) == count
    for file in ([ROOT/"chapters/CPE333_Midterm_Exam.log",ROOT/"frontmatter/cover_CPE333_Midterm_Exam.log",ROOT/"solutions/CPE333_Midterm_Solutions.log"] if check_logs else []):
        log=file.read_text(errors="replace")
        assert "Missing character:" not in log, f"Missing glyph in {file}"
        assert "Overfull \\vbox" not in log, f"Page overflow in {file}"
        assert "Overfull \\hbox" not in log, f"Horizontal overflow in {file}"
    print(json.dumps({"exam_pages":len(doc),"mcq":41,"short":10,"essay":3,
                      "total_points":50,"answer_key_pages":len(fitz.open(ROOT/"output/pdf/CPE333_Midterm_Mock_Solutions.pdf")),
                      "scheduling":{p:{k:v for k,v in scheduling(p).items() if k!="trace"} for p in ("FIFO","SJF","RR")},
                      "faults":{p:replacement(p)["faults"] for p in ("FIFO","LRU","OPT")}},ensure_ascii=False,indent=2))


def clean_build_artifacts():
    """Move only known, reproducible build artifacts out of the repository."""
    jobs = [(ROOT,"CPE333_Midterm_Exam_main"),
            (ROOT/"frontmatter","cover_CPE333_Midterm_Exam"),
            (ROOT/"chapters","CPE333_Midterm_Exam"),
            (ROOT/"solutions","CPE333_Midterm_Solutions")]
    suffixes = (".aux",".log",".out",".toc",".synctex.gz",".xdv",
                ".fls",".fdb_latexmk",".w18",".pdf")
    candidates = [folder/(job+suffix) for folder,job in jobs for suffix in suffixes]
    candidates += [ROOT/"CPE333_Midterm Exam_main.pdf",
                   ROOT/"frontmatter/cover_CPE333_Midterm Exam.log",
                   ROOT/"frontmatter/svg-inkscape/KMUTT_Logo_svg-tex.pdf",
                   ROOT/"frontmatter/svg-inkscape/KMUTT_Logo_svg-tex.pdf_tex"]
    cache=ROOT/"__pycache__"
    candidates += list(cache.glob("build.*.pyc"))+list(cache.glob("test_mock_exam.*.pyc"))
    targets=[p for p in candidates if not p.is_symlink() and p.is_file()
             and p.resolve().is_relative_to(ROOT.resolve())]
    if not targets:
        print("No known build artifacts to clean.")
        return
    backup=Path(tempfile.mkdtemp(prefix="cpe333-build-clean-"))
    for source in targets:
        destination=backup/source.relative_to(ROOT)
        destination.parent.mkdir(parents=True,exist_ok=True)
        shutil.move(str(source),str(destination))
    for folder in (cache,ROOT/"frontmatter/svg-inkscape"):
        if folder.is_dir() and not folder.is_symlink() and not any(folder.iterdir()):
            folder.rmdir()
    print(f"Cleaned {len(targets)} reproducible artifacts; recoverable at {backup}")


def main():
    parser=argparse.ArgumentParser()
    mode=parser.add_mutually_exclusive_group()
    mode.add_argument("--check-only",action="store_true")
    mode.add_argument("--clean",action="store_true",help="Move known build artifacts to a temporary recovery folder; keep sources, components and final PDFs")
    args=parser.parse_args()
    validate_bank()
    if args.clean:
        clean_build_artifacts()
        return
    if args.check_only:
        verify_pdfs()
        return
    (ROOT/"chapters/questions.generated.tex").write_text(exam_source())
    (ROOT/"solutions/solutions.generated.tex").write_text(solutions_source())
    run_xelatex(ROOT/"frontmatter","cover_CPE333_Midterm Exam.tex")
    run_xelatex(ROOT/"chapters","CPE333_Midterm Exam.tex")
    run_xelatex(ROOT,"CPE333_Midterm Exam_main.tex")
    run_xelatex(ROOT/"solutions","CPE333_Midterm_Solutions.tex")
    (ROOT/"output/pdf").mkdir(parents=True,exist_ok=True)
    shutil.copy2(ROOT/"CPE333_Midterm Exam_main.pdf",ROOT/"output/pdf/CPE333_Midterm_Mock_Exam.pdf")
    shutil.copy2(ROOT/"solutions/CPE333_Midterm_Solutions.pdf",ROOT/"output/pdf/CPE333_Midterm_Mock_Solutions.pdf")
    verify_pdfs(check_logs=True)


if __name__ == "__main__":
    main()
