# SLMail Buffer Overflow Exploit

This repo contains a fuzzer bad char generator and an exploit for The POP3
server of Seattle Lab Mail 5.5 (SLMail) which is vulnerable to a buffer
overflow.

This can be simply be exploited by executing steps 8-12 below. However if you
are interested in my complete process you can find all the steps below.

## Exploit steps

1. Edit fuzzer.py entering the IP address your SLMail instance. Run fuzzer.py.
   When the program crashes the last amount of bytes sent is the estimated
   offset.

```
./fuzzer.py
```

2. User Metasploit's pattern_create to generate a pattern 400 bytes longer than
   the estimated offset.

```
/usr/share/metasploit-framework/tools/pattern_create.rb -l <estimated offset + 400>
```
