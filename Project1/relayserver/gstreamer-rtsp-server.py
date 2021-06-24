
from gi.repository import Gst, GstRtspServer, GObject, GLib
import sys
import gi
gi.require_version('Gst', '1.0')


if __name__ == '__main__':
    loop = GLib.MainLoop()
    # GObject.threads_init()
    Gst.init(None)

    class MyFactory(GstRtspServer.RTSPMediaFactory):
        def __init__(self):
            GstRtspServer.RTSPMediaFactory.__init__(self)

        def do_create_element(self, url):
            spec = """
			gst-launch-1.0 rtspsrc location=rtsp://keti:keti1234@192.168.100.70:8810/videoMain latency=200 ! rtph264depay ! h264parse ! autovideosink
			"""
            return Gst.parse_launch(spec)

    class GstServer():
        def __init__(self):
            self.server = GstRtspServer.RTSPServer()
            self.server.set_service("3002")
            f = MyFactory()
            f.set_shared(True)
            m = self.server.get_mount_points()
            m.add_factory("/test", f)
            self.server.attach(None)

    s = GstServer()
    loop.run()
