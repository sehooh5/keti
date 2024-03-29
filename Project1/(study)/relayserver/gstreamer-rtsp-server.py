
from gi.repository import Gst, GstRtspServer, GObject, GLib
import gi
import sys
gi.require_versions({'Gst': '1.0', 'GstRtspServer': '1.0'})


if __name__ == '__main__':
    loop = GLib.MainLoop()
    # GObject.threads_init()
    Gst.init(None)

    class MyFactory(GstRtspServer.RTSPMediaFactory):
        def __init__(self):
            GstRtspServer.RTSPMediaFactory.__init__(self)

        def do_create_element(self, url):
            spec = """
			filesrc location=test.mp4 ! qtdemux name=demux
			demux.video_0 ! queue ! rtph264pay pt=96 name=pay0
			demux.audio_0 ! queue ! rtpmp4apay pt=97 name=pay1
			demux.subtitle_0 ! queue ! rtpgstpay pt=98 name=pay2
			"""
            return Gst.parse_launch(spec)

    class GstServer():
        def __init__(self):
            self.server = GstRtspServer.RTSPServer()
            self.server.set_service("3333")
            f = MyFactory()
            f.set_shared(True)
            m = self.server.get_mount_points()
            m.add_factory("/test", f)
            self.server.attach(None)
            print("bye")

    s = GstServer()
    loop.run()
