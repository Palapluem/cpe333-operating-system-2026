#!/usr/bin/env python3
"""Independent arithmetic/algorithm checks plus PDF publication-contract tests."""
from functools import lru_cache
from fractions import Fraction
from itertools import permutations
import re
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

import build


class MockExamTests(unittest.TestCase):
    def test_student_header_fills_text_width(self):
        import pymupdf
        doc=pymupdf.open(build.ROOT/"output/pdf/CPE333_Midterm_Mock_Exam.pdf")
        margin=0.8*72
        for page in list(doc)[1:]:
            lines=sorted((d["rect"] for d in page.get_drawings()
                          if d["rect"].y0<60 and d["rect"].width>100),key=lambda r:r.x0)
            self.assertEqual(len(lines),2)
            self.assertAlmostEqual(lines[-1].x1,page.rect.width-margin,delta=.2)
            self.assertAlmostEqual(lines[0].y0,lines[1].y0,delta=.1)
            words=[w for w in page.get_text("words") if w[1]<60]
            self.assertEqual([w[4] for w in words],["Name","Student","ID"])
            self.assertAlmostEqual(words[0][0],margin,delta=.2)
            self.assertLess(words[0][2],lines[0].x0)
            self.assertLess(lines[0].x1,words[1][0])
            self.assertLess(words[-1][2],lines[1].x0)

    def test_cover_spacing_time_and_reference_asterisk_line(self):
        import pymupdf
        page=pymupdf.open(build.ROOT/"output/pdf/CPE333_Midterm_Mock_Exam.pdf")[0]
        lines=[]
        for block in page.get_text('dict')['blocks']:
            for line in block.get('lines',[]):
                text=''.join(s['text'] for s in line['spans'])
                lines.append((re.sub(r'\s+','',text),line['spans'][0]['origin'][1]))
        def baseline(prefix):
            return next(y for text,y in lines if text.startswith(prefix))
        y=[baseline(s) for s in ['1.ข้อสอบมี3ส่วน','ส่วนที่1','ส่วนที่2','ส่วนที่3','2.ให้ทำข้อสอบ']]
        reference_gap=baseline('3.ไม่อนุญาตให้นำตำรา')-baseline('2.อนุญาตให้ใช้เครื่องคำนวณ')
        for a,b in zip(y,y[1:]):
            self.assertAlmostEqual(b-a,reference_gap,delta=.1)
        compact=re.sub(r'\s+','',page.get_text())
        self.assertIn('09.00-12.00(3ชั่วโมง)',compact)
        self.assertIn('*ข้อสอบได้ผ่านการพิจารณาจากคณะกรรมการประจำภาควิชาวิศวกรรมคอมพิวเตอร์แล้ว*',compact)
        self.assertLess(baseline('*ข้อสอบได้ผ่านการพิจารณา'),baseline('หัวหน้าภาควิชา'))

    def test_question_counts_and_points(self):
        build.validate_bank()
        self.assertEqual(Fraction(20,41)*41+10+8+4+8,50)
        self.assertEqual(len(build.BANK["mcq"]),41)
        self.assertEqual(len(build.BANK["short"]),10)

    def test_source_selection_and_short_answer_depth(self):
        for q in build.BANK["mcq"]:
            self.assertRegex(q["ref"],r"E05|E03")
            self.assertIn(q["lecture"],range(1,7))
            self.assertFalse(any("all of the above" in c.lower() for c in q["choices"]))
        self.assertEqual(sum("E03" in q["ref"] for q in build.BANK["mcq"]),5)
        for n,answer in {3:"c",4:"b",10:"d",16:"d",23:"b"}.items():
            self.assertEqual(build.BANK["mcq"][n-1]["answer"],answer)
        self.assertEqual(sum(q["source_year"]==2022 for q in build.BANK["mcq"]),36)
        self.assertEqual(len({(q["source_year"],q["source_question"]) for q in build.BANK["mcq"]}),41)
        self.assertEqual(build.BANK["mcq"][18]["source_question"],3)
        self.assertEqual(build.BANK["mcq"][18]["answer"],"a")
        self.assertEqual(len({q["q"] for q in build.BANK["short"]}),10)
        for q in build.BANK["short"]:
            self.assertNotRegex(q["q"],r"[\u0e00-\u0e7f]")
            self.assertTrue(q["answer"].strip())
            self.assertLessEqual(len(q["answer"].split()),25)
        for abbreviation in ["MLFQ","STCF","MMU","PCB","TLB"]:
            self.assertTrue(any(abbreviation in q["q"] for q in build.BANK["short"]))
        self.assertIn("4096-byte bound",build.BANK["short"][8]["answer"])

    def test_short_answers_are_keywords_examples_or_brief_reasons(self):
        import pymupdf
        font=pymupdf.Font(fontfile=str(build.ROOT/"fonts/THSarabunNew.ttf"))
        width=595.28-2*.8*72-24
        for q in build.BANK["short"]:
            # Greedy wrapping of a concise model answer at the exam's font size.
            lines=[""]
            for word in q["answer"].split():
                trial=(lines[-1]+" "+word).strip()
                if font.text_length(trial,fontsize=12*1.33)>width:
                    lines.append(word)
                else:
                    lines[-1]=trial
            self.assertLessEqual(len(lines),2,q["n"])
        for n in [4,5]:
            self.assertIn("two",build.BANK["short"][n-1]["q"])
        self.assertIn("one example each",build.BANK["short"][6]["q"])
        self.assertEqual(build.BANK["short"][5]["answer"],"Zombie process.")
        self.assertIn("1 point",build.BANK["short"][5]["accept"])

    def test_fifo_and_lru_with_independent_recency_lists(self):
        refs=build.BANK["replacement"]["reference"]
        for policy in ["FIFO","LRU"]:
            resident=[]
            for step,page in enumerate(refs):
                hit=page in resident
                if not hit:
                    if len(resident)==3:
                        resident.pop(0)
                    resident.append(page)
                elif policy=="LRU":
                    resident.remove(page)
                    resident.append(page)
                actual=build.replacement(policy)["rows"][step]
                self.assertEqual(actual["hit"],hit,(policy,step))
                self.assertEqual(set(x for x in actual["frames"] if x is not None),set(resident))

    def test_opt_against_exhaustive_dynamic_program(self):
        refs=build.BANK["replacement"]["reference"]
        @lru_cache(None)
        def minimum_faults(i,resident):
            if i==len(refs):
                return 0
            s=set(resident)
            if refs[i] in s:
                return minimum_faults(i+1,resident)
            if len(s)<3:
                return 1+minimum_faults(i+1,tuple(sorted(s|{refs[i]})))
            return 1+min(minimum_faults(i+1,tuple(sorted((s-{victim})|{refs[i]}))) for victim in s)
        self.assertEqual(minimum_faults(0,()),10)
        self.assertEqual(build.replacement("OPT")["faults"],minimum_faults(0,()))

    def test_round_robin_using_independent_tick_model(self):
        remaining=build.BANK["scheduling"]["bursts"].copy()
        i,t=0,0
        first,done={},{}
        while any(remaining):
            if remaining[i]:
                first.setdefault(i,t)
                remaining[i]-=1
                t+=1
                if not remaining[i]:
                    done[i]=t
            i=(i+1)%5
        r=build.scheduling("RR")
        self.assertEqual(r["turnaround"],[done[i] for i in range(5)])
        self.assertEqual(r["response"],[first[i] for i in range(5)])
        self.assertEqual(t,19)

    def test_sjf_mean_over_all_nonpreemptive_orders(self):
        bursts=build.BANK["scheduling"]["bursts"]
        means=[]
        for order in permutations(range(5)):
            t,total=0,0
            for i in order:
                t+=bursts[i]
                total+=t
            means.append(total/5)
        self.assertEqual(min(means),7.0)
        self.assertEqual(build.scheduling("SJF")["mean_tat"],min(means))

    def test_eat_exact_arithmetic_and_units(self):
        self.assertEqual(10*10**6,build.BANK["replacement"]["fault_ns"])
        fifo=(1-Fraction(13,20))*10+Fraction(13,20)*10_000_000
        opt=(1-Fraction(10,20))*10+Fraction(10,20)*10_000_000
        self.assertEqual(fifo,Fraction(13_000_007,2))
        self.assertEqual(opt,5_000_005)
        self.assertLess(opt,fifo)

    def test_pdf_page_plan_and_numbered_questions(self):
        import pymupdf
        doc=pymupdf.open(build.ROOT/"output/pdf/CPE333_Midterm_Mock_Exam.pdf")
        self.assertEqual(len(doc),12)
        expected=[list(range(a,b)) for a,b in [(1,7),(7,13),(13,19),(19,25),(25,31),(31,37),(37,42)]]
        for p,nums in zip(list(doc)[1:8],expected):
            actual=re.findall(r"(?m)^(\d+)\. ",p.get_text())
            self.assertEqual([int(n) for n in actual],nums)
            self.assertNotIn("ตอบ",p.get_text())
            # Four options are on four different baselines, in one column.
            opts=[w for w in p.get_text("words") if re.fullmatch(r"\([a-d]\)",w[4])]
            self.assertEqual(len(opts),4*len(nums))
            for j in range(0,len(opts),4):
                self.assertLess(max(w[2] for w in opts[j:j+4])-min(w[2] for w in opts[j:j+4]),1)
                self.assertEqual([w[4] for w in opts[j:j+4]],["(a)","(b)","(c)","(d)"])
                self.assertTrue(all(opts[k+1][1]>opts[k][1] for k in range(j,j+3)))
        self.assertIn("ชื่อ",doc[0].get_text())
        self.assertIn("รหัส",doc[0].get_text())
        self.assertIn("Operating System",doc[0].get_text())
        self.assertNotIn("Operating Systems",doc[0].get_text())
        self.assertNotIn("Mock",doc[0].get_text())
        self.assertNotIn("20/41",doc[0].get_text())
        self.assertIn("สมุดคำตอบ",doc[0].get_text())
        all_text="\n".join(p.get_text() for p in doc)
        self.assertNotRegex(all_text,r"\(continued\)|End of examination")
        for title,index in [("Part I:",1),("Part II:",8),("Part III:",9)]:
            self.assertEqual(all_text.count(title),1)
            self.assertIn(title,doc[index].get_text())
        for i in range(1,12):
            text=doc[i].get_text()
            self.assertIn("Name",text)
            self.assertIn("Student ID",text)
            self.assertIn(f"{i+1}/12",text)
            spans=[s for b in doc[i].get_text('dict')['blocks'] if 'lines' in b for l in b['lines'] for s in l['spans']]
            footer=[s for s in spans if "หน้าที่" in s["text"]]
            self.assertTrue(footer)
            self.assertTrue(all("Italic" in s["font"] for s in footer))
            self.assertIn("กลางภาคการศึกษาที่1/2569",text.replace(" ",""))
            body="\n".join(line for line in text.splitlines() if "ข้อสอบรายวิชา" not in line and "หน้าที่" not in line)
            self.assertNotRegex(body,r"[\u0e00-\u0e7f]")
        self.assertIn("Run time (ms)",doc[9].get_text())
        self.assertIn("commercial bank",doc[9].get_text())
        self.assertIn("reference string",doc[9].get_text().replace("-\n","-"))
        for label in ["1. (8 points)","2. (4 points)","3. (8 points)"]:
            self.assertIn(label,doc[9].get_text())
        for i in [10,11]:
            # Deliberate scratch pages contain only the normal name/ID + footer.
            words=[w for w in doc[i].get_text('words') if 60<w[1]<750]
            self.assertEqual(words,[])
        short=doc[8].get_text()
        self.assertEqual([int(x) for x in re.findall(r"(?m)^(\d+)\. ",short)],list(range(1,11)))
        self.assertNotIn("คำตอบ",short)
        self.assertNotIn("Answer:",short)

    def test_written_reference_tasks_are_complete(self):
        import pymupdf
        page=pymupdf.open(build.ROOT/"output/pdf/CPE333_Midterm_Mock_Exam.pdf")[9]
        text=re.sub(r'\s+',' ',page.get_text())
        for phrase in ["run time of each process", "all at time 0", "time slice = 1 ms",
                       "turnaround time of each process", "response time of each process",
                       "minimum average turnaround time", "minimum average response time",
                       "commercial bank", "Describe the algorithms and policies used",
                       "provide suggestions on how to improve the process",
                       "optimizing the average turnaround time of customers",
                       "three initially empty frames", "FIFO, LRU, and OPT", "effective access time (EAT)",
                       "memory-access time is 10 ns", "disk-access time is 10 ms"]:
            self.assertIn(phrase,text)
        string=', '.join(str(n) for n in build.BANK['replacement']['reference'])
        self.assertIn(string,text)

    def test_written_subparts_are_compact_and_complete(self):
        import pymupdf
        page=pymupdf.open(build.ROOT/"output/pdf/CPE333_Midterm_Mock_Exam.pdf")[9]
        text=page.get_text()
        self.assertNotIn("part (a)",text)
        for phrase in ["under each policy", "(4.5 points)", "(1.5 points)",
                       "total faults, total hits, and fault probability", "in milliseconds"]:
            self.assertIn(phrase,text)
        lines=[''.join(s['text'] for s in line['spans'])
               for block in page.get_text('dict')['blocks'] for line in block.get('lines',[])]
        for phrase in ["Find the turnaround time", "Find the response time"]:
            line=next(line for line in lines if phrase in line)
            self.assertIn("under each policy.",line)
        self.assertEqual(text.count('(a)'),2)
        self.assertEqual(text.count('(b)'),2)
        self.assertEqual(text.count('(c)'),2)
        key=pymupdf.open(build.ROOT/"output/pdf/CPE333_Midterm_Mock_Solutions.pdf")
        key_text=re.sub(r'\s+','','\n'.join(p.get_text() for p in key))
        self.assertIn('ข้อ(a)',key_text)
        self.assertIn('ข้อ(b)',key_text)
        self.assertIn('ข้อ(c)',key_text)

    def test_nonpublication_checkbox_is_crossed(self):
        import pymupdf
        page=pymupdf.open(build.ROOT/"output/pdf/CPE333_Midterm_Mock_Exam.pdf")[0]
        # The two publication checkboxes are the top-left 17.5-point squares.
        drawings=page.get_drawings()
        boxes=sorted([d['rect'] for d in drawings if 17<d['rect'].width<18
                      and 17<d['rect'].height<18 and d['rect'].y0<100
                      and d['rect'].x0<200],key=lambda r:r.x0)
        self.assertEqual(len(boxes),2)
        def diagonals(box):
            return [item for d in drawings for item in d['items']
                    if item[0]=='l' and abs(item[1].x-item[2].x)>5
                    and abs(item[1].y-item[2].y)>5
                    and box.contains(item[1]) and box.contains(item[2])]
        self.assertEqual(len(diagonals(boxes[0])),0)
        self.assertEqual(len(diagonals(boxes[1])),2)

    def test_clean_only_targets_reproducible_artifacts(self):
        with TemporaryDirectory() as folder, TemporaryDirectory() as recovery:
            root=Path(folder)
            relative=['CPE333_Midterm_Exam_main.log',
                      'CPE333_Midterm Exam_main.pdf',
                      'solutions/CPE333_Midterm_Solutions.pdf',
                      'frontmatter/svg-inkscape/KMUTT_Logo_svg-tex.pdf',
                      '__pycache__/build.cpython-311.pyc']
            keep=['notes.log','chapters/CPE333_Midterm Exam.pdf',
                  'frontmatter/cover_CPE333_Midterm Exam.pdf',
                  'output/pdf/CPE333_Midterm_Mock_Exam.pdf','question-bank.json',
                  '__pycache__/unrelated.pyc']
            for name in relative+keep:
                target=root/name
                target.parent.mkdir(parents=True,exist_ok=True)
                target.touch()
            with patch.object(build,'ROOT',root), patch.object(build.tempfile,'mkdtemp',return_value=recovery):
                build.clean_build_artifacts()
            for name in relative:
                self.assertFalse((root/name).exists())
                self.assertTrue((Path(recovery)/name).is_file())
            for name in keep:
                self.assertTrue((root/name).is_file())

    def test_pdf_master_matches_component_renders(self):
        import pymupdf
        from PIL import Image,ImageChops,ImageStat
        root=build.ROOT
        main=pymupdf.open(root/"output/pdf/CPE333_Midterm_Mock_Exam.pdf")
        sources=[pymupdf.open(root/"frontmatter/cover_CPE333_Midterm Exam.pdf"),
                 pymupdf.open(root/"chapters/CPE333_Midterm Exam.pdf")]
        components=list(sources[0])+list(sources[1])
        for n,(p,q) in enumerate(zip(main,components)):
            a=p.get_pixmap();b=q.get_pixmap()
            self.assertEqual((a.width,a.height),(b.width,b.height))
            im1=Image.frombytes('RGB',(a.width,a.height),a.samples)
            im2=Image.frombytes('RGB',(b.width,b.height),b.samples)
            self.assertLess(max(ImageStat.Stat(ImageChops.difference(im1,im2)).mean),.5,f'Page {n+1}')

    def test_scheduling_table_numeric_columns_are_centered(self):
        import pymupdf
        page=pymupdf.open(build.ROOT/"output/pdf/CPE333_Midterm_Mock_Exam.pdf")[9]
        words=page.get_text('words')
        header=next(w for w in words if w[4]=="Priority" and w[1]<250)
        cells=[w for w in words if w[4].isdigit() and header[1]+15<w[1]<header[1]+110]
        runtime=[w for w in cells if 270<(w[0]+w[2])/2<345]
        priority=[w for w in cells if abs((w[0]+w[2]-header[0]-header[2])/2)<5]
        self.assertEqual([int(w[4]) for w in runtime],[10,1,2,1,5])
        self.assertEqual([int(w[4]) for w in priority],[3,1,3,4,2])
        for column in [runtime,priority]:
            centers=[(w[0]+w[2])/2 for w in column]
            self.assertLess(max(centers)-min(centers),.1)


if __name__=="__main__":
    unittest.main(verbosity=2)
