# Kernel Development Reference

This folder contains supporting material for Mini-Project 2, covering kernel-module parameters and `/proc` read/write callbacks. The Mini-Project 2 brief mentions `/proc` or command-line arguments as possible ways to provide a process ID for the scheduler-profiler topic, so this material is useful background. It is reference material, not a separate Mini-Project 2 deliverable.

- [`Linux_Kernel_Development_Command_Line_and_procfs.pdf`](Linux_Kernel_Development_Command_Line_and_procfs.pdf): lecture exercise on module parameters and `/proc` files.
- [`example_code.c`](example_code.c): sample procfs module from the exercise.

The sample is a starting point, not a completed answer to the exercise: its read callback returns a hard-coded `HelloWorld!` string instead of the text written through `/proc`, and the shared buffer has no synchronization for concurrent reads and writes. Review and extend it for the group's assigned project topic before using it as an implementation.

See the [Mini-Project 2 brief](../../CPE333_MiniProject2_2026.pdf) for the actual project requirements and assigned topics.
