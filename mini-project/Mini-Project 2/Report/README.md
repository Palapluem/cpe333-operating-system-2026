# CPE333 Mini-Project 2 Report

This report documents the group's Virtual Memory project: a Linux tool for inspecting a process's address space and counting page faults. It describes the design, test method, and measured results.

## Project details

- **Course:** CPE333 Operating Systems
- **Project:** Mini-Project 2 — Virtual Memory
- **Group:** มูลนิธิทนายตั้ม ช่วยสู้
- **Instructor:** Asst. Prof. Rajchawit Sarochawikasit
- **Members:** Seven students; names and student IDs appear on the cover.

## Source code

The kernel module and tools are maintained in the team repository at [merge commit 5fbcb767](https://github.com/beambeambeam/cpe333/tree/5fbcb7679298f36e2bae8b7cd3dbe6bf6a609800/mini-project-02). The report and its verification evidence are kept together here without duplicating the implementation source.

## Report files

| File | Purpose |
|---|---|
| `CPE333_MiniProject2_Report.docx` | Editable Word companion; its contents predate the 11 November verification and 19 November LaTeX sync |
| `report.tex` | LaTeX report source, matching the team repository |
| `frontpage/frontpage.tex` | Cover page with the group's details |
| `frontpage/frontpage.example.tex` | Reusable cover-page template |
| `.latexmkrc` | Selects XeLaTeX for the report source |
| `output/pdf/CPE333_MiniProject2_Report.pdf` | A4 print and reading copy |
| `frontpage/assets/` | KMUTT logo files used by the cover |
| `assets/` | Report diagrams |
| `evidence/post-merge-5fbcb76/` | Original test logs, environment details, and eight Terminal captures |
| `evidence/recheck-2026-11-11/` | Fresh VM and LaTeX logs, experiment outputs, and two cropped Terminal captures |

## Layout and typography

The report follows the visual style of PS04, PS06, and PS07: centered KMUTT cover, clear Problem/Step headings, green emphasis for key terms, and blue italic captions. Body text uses Sarabun 12 pt; commands and code use Menlo. The cover lists all seven group members and the instructor. The cover source and logo now use the same `frontpage/` structure as the team repository.

The print-ready PDF has 21 A4 portrait pages: cover on physical page 1, contents on page 2, report and references on pages 3–19 (numbered 1–17), and a two-page appendix on pages 20–21. The main report remains within the assignment's 25-page limit before the appendix. The PDF is the reference for print pagination; the editable DOCX may paginate differently in Word or Google Docs.

## Source and test results

- The original measurement tables and chart use the merged implementation at commit `5fbcb7679298f36e2bae8b7cd3dbe6bf6a609800`, tested on Ubuntu 24.04.5, Linux 6.8.0-142-generic, ARM64.
- On 11 November 2026, the full workflow was rerun from the reviewed PR revision `ed0a7a6` on Linux 6.8.0-147-generic. Build/load, demo, all five regression checks, E1–E8, live-process comparison, a separate E7 timeline, SIGCHLD cleanup, and final cleanup passed. The new records are in `evidence/recheck-2026-11-11/`; the original measurement tables and chart remain tied to the earlier kernel run.
- The LaTeX report was rebuilt on 11 November 2026 with XeLaTeX and latexmk, then rebuilt from the synchronized local source on 19 November. Both outputs are 21 A4 pages; the local build transcript is `evidence/recheck-2026-11-11/11-local-build-2026-11-19.txt`.
- The DOCX was not regenerated in this sync. Use the LaTeX source and PDF as the current report; the DOCX remains an older editable companion pending a separately rendered and reviewed update.
- The eight original Terminal captures appear beside related discussion in the report. The new recheck folder adds cropped captures for the LaTeX build and regression run, plus searchable logs. The shell `pfstat` report (PID 1622) exists only as a screenshot.
- Kbuild showed different compiler executable names, but both reported GCC 13.3.0. BTF generation was skipped because the VM did not have `vmlinux`; the module still built and loaded. Lima also logged a closed-network-connection message as its host agent shut down; the instance stopped successfully with exit status 0.
- GitHub Actions were not configured for this PR. Results are from manual runs in Lima.
- The report describes the tested configuration and limits, including unmeasured probe overhead, descendant-accounting scope, and the non-root permission check that was not rerun after merge.

## Rebuild the PDF

Install XeLaTeX, `latexmk`, Sarabun, and Menlo. From this folder, build into a temporary directory:

```sh
report_build_dir="$(mktemp -d -t cpe333-report)"
latexmk -xelatex -interaction=nonstopmode -halt-on-error \
  -outdir="$report_build_dir" report.tex
cp "$report_build_dir/CPE333_MiniProject2_Report.pdf" output/pdf/
rm -r "$report_build_dir"
```

The source uses `fontspec`, `polyglossia`, `geometry`, `graphicx`, `longtable`, `needspace`, `fancyhdr`, `titlesec`, `listings`, `xurl`, and `hyperref`. Shell escape is not required.

## Before submission

Prepare the separate 7–11 minute presentation and implementation demo required by the assignment.
