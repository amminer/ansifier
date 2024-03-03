# ASCIIFIER

The main script (image_printer_go_brrr.py, which I really should have changed before posting)
reads an image file into memory and parses it into colored text using ansi escapes,
then dumps it to stdout. I find this really fun, and sometimes even useful.

I hope to eventually evolve it into something that could be easily consumed
by other code, maybe being used in the context of something with a terminal
UI (curses, perhaps?). This might already be out there, I wouldn't know since
I don't know any curses - this is just a passion project!

It uses a handful of switches to provide highly configurable output.
Check out its output with the -h flag!

I've only tested this on Linux in gnome-terminal under X11, but I have had a friend
clone it and run it in powershell and cmd on Windows 11 with reasonable results.
Windows terminals don't seem to behave as well and there's some chop/screen tearing
going on when animated gifs are processed. I hope to resolve this soon but it takes a
lot (like real work) to get me to run Windows, to be fully honest. Regardless, here it
is working its magic on my Linux box:

https://github.com/amminer/asciifier/assets/107884857/33ef3ec5-64a6-40ec-bee2-bff622b389b2

(🎶 - Lightsleeper by Windows 96)

## Some examples of the script's utility:

* Easily generate little graphics for notes you're taking:

  ![program being used to generate a haxor guy](readme-images/haxor.png)

  ```
  ...
  metasploit of course:

                 ++$$$$--
                $$##$$##$
                $$ > <  +
              ++$$  ω  #-
          --$$@@@@#   $$
          $$@@@@@@@@####++
        --@@##$$@@@@##@@@@--    --++--
        $$@@$$$$ get pwnd $     $$@@##++--
        ####++##@@# lol #$$     $$@@@@@@##
      --####++$$$$@@##$$##$$    $$@@##@@@@
      --@@@@####$$$$##@@##$$    ##@@##@@$$
        $$####@@##++$$######++--##@@##@@++
          $$##$$##$$----$$@@##$$##@@@@@@++ ___
          ++##$$$$++++--++$$$$$$$$$$$$$$   __ |
            ----    ----                    | |
                                            | |          INTERFACES
           |````````````````````````````````` |          ___________
           | |`````````````````````````````````         | console   |
           | |                        LIBRARIES         |           |
           | |                        __________        | cli       |
           | |_______ TOOLS ======== | rex      |       |           |
           L_________                |          |       | web       |
                      PLUGINS ====== | msfcore  | ===== |           |
                                     |          |       | gui       |
                                     | msf base |       |           |
                                     ````````````       | armitage  |
                             modules      ||            `````````````
                       ___________________________________________________
                      |                                                   |
                      | payloads  exploits  encoders  post-mods auxiliary |
                      |                                                   |
                      `````````````````````````````````````````````````````

  There's also Cobalt Strike -
  ...
  ```

* Make neofetch less ugly (especially on Linux Mint):

  ![output of neofetch patched with the output from this program](readme-images/meofetch.png)

