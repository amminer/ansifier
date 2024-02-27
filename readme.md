# ASCIIFIER

I wrote a scrappy little version of this program relatively early in my
foray into programming. I find it really fun and useful and have occasionally improved it over the years.

I hope to eventually evolve it into something that could be consumed
by other code and used in the context of something with a console UI
(curses, perhaps?). This might already be out there, I wouldn't know since
I don't know any curses - this is just a passion project!

It uses a handful of switches to provide highly configurable output.
Check out its output with the -h flag!

I have ideas for more options, so keep an eye out for updates
and feel free to reach out to me if you have an idea and want to
link and build, fam :)

Some examples of its utility:

* Easily generate cute graphic images for notes you're taking:

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

