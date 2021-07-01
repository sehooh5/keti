
from gi.repository import GObject, Gst
import sys
import os
import time
import re
import time

import gi
gi.require_version('Gst', '1.0')

if __name__ == '__main__':
    # GObject.threads_init()
    Gst.init(None)

    pipeline = Gst.parse_launch("""
	 rtspsrc location=rtsp://localhost:3002/test latency=200 ! rtph264depay ! h264parse ! autovideosink
	""")

    pipeline.set_state(Gst.State.PLAYING)

    t0 = time.time()
    bus = pipeline.get_bus()
    while True:
        msg = bus.poll(Gst.MessageType.ANY, int(1e6))
        if msg is None:
            if time.time() - t0 > 10:
                print("break")
                pipeline.send_event(Gst.Event.new_eos())
                pipeline.set_state(Gst.State.NULL)
                break
            continue
        t = msg.type
        if t == Gst.MessageType.EOS:
            print("EOS")
            break
            pipeline.set_state(Gst.State.NULL)
        elif t == Gst.MessageType.ERROR:
            err, debug = msg.parse_error()
            print("Error: %s" % err, debug)
            break
        elif t == Gst.MessageType.WARNING:
            err, debug = msg.parse_warning()
            print("Warning: %s" % err, debug)
        elif t == Gst.MessageType.STATE_CHANGED:
            pass
        elif t == Gst.MessageType.STREAM_STATUS:
            pass
        else:
            print(t)
            print("Unknown message: %s" % msg)

    print("Bye bye ;)")
