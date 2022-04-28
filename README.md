# SLMail Buffer Overflow Exploit

This repo contains a fuzzer bad char generator and an exploit for The POP3
server of Seattle Lab Mail 5.5 (SLMail) which is vulnerable to a buffer
overflow.

This can be simply be exploited by executing steps 8-12 below. However if you
are interested in my complete process you can find all the steps below.

I included 2 exploit scripts:

-- exploit_final.py: simply change the IP insert your payload and run against
the target.

-- exploit_blank.py: exploit template if you want to follow all the steps from
the beginning.

## Exploit steps

1. Edit fuzzer.py entering the IP address your SLMail instance. Run fuzzer.py.
   When the program crashes the last amount of bytes sent is the estimated
   offset.

```
./fuzzer.py
```

2. Install SLMail 5.5 with default settings and immunity debugger with mona a
   windows 7 32 bit machine.

3. Run SLMail start the POP3 service in the control tab. Open Immunity debugger
   and attach s

4. User Metasploit's pattern_create to generate a pattern 400 bytes longer than
   the estimated offset.

```
/usr/share/metasploit-framework/tools/pattern_create.rb -l <estimated offset + 400>
```

3.
