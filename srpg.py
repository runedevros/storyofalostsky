#!/usr/bin/env python2

import lostsky
import os

if __name__ == "__main__":

    #os.chdir(os.path.join('/usr', 'share', 'lostsky'))
    demo_mode = False

    if demo_mode:
        lostsky.demo_mode('touhoucon_demo')
    else:
        lostsky.bootstrap()
