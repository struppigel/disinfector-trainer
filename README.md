# disinfector-trainer

Small command-line Python tool that applies Windows Autostart Extensibility Points (ASEPs).
It uses calc.exe as target file and logs the changes into a log file, so you can look them up later.

I use it for basic malware analysis/disinfection training (it is not sufficient on its own, of course).

Only use this tool in a VM! It is just too easy and tempting to execute it several times, resulting in lots of annoying calculators.
