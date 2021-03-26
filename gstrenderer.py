#!/usr/bin/env python3

import gi
gi.require_version('Gst', '1.0')
from gi.repository import Gst
gi.require_version('GstWebRTC', '1.0')
from gi.repository import GstWebRTC
gi.require_version('GstSdp', '1.0')
from gi.repository import GstSdp
gi.require_version('Rsvg', '2.0')
from gi.repository import Rsvg
import cairo
from ctypes import *
from contextlib import contextmanager
import time

Gst.init(None)

class GstMapInfo(Structure):
    _fields_ = [("memory", c_void_p),        # GstMemory *memory
                ("flags", c_int),            # GstMapFlags flags
                ("data", POINTER(c_byte)),   # guint8 *data
                ("size", c_size_t),          # gsize size
                ("maxsize", c_size_t),       # gsize maxsize
                ("user_data", c_void_p * 4), # gpointer user_data[4]
                ("_gst_reserved", c_void_p * 4)]

libgst = CDLL("libgstreamer-1.0.so.0")

GST_MAP_INFO_POINTER = POINTER(GstMapInfo)

# gst_buffer_map
libgst.gst_buffer_map.argtypes = [c_void_p, GST_MAP_INFO_POINTER, c_int]
libgst.gst_buffer_map.restype = c_int

# gst_buffer_unmap
libgst.gst_buffer_unmap.argtypes = [c_void_p, GST_MAP_INFO_POINTER]
libgst.gst_buffer_unmap.restype = None

# gst_mini_object_is_writable
libgst.gst_mini_object_is_writable.argtypes = [c_void_p]
libgst.gst_mini_object_is_writable.restype = c_int

def map_gst_buffer(pbuffer, flags):
    if pbuffer is None:
        raise TypeError("Cannot pass NULL to map_gst_buffer")

    ptr = hash(pbuffer)
    if flags & 2 and libgst.gst_mini_object_is_writable(ptr) == 0:
        raise ValueError("Writable array requested but buffer is not writeable")

    mapping = GstMapInfo()
    success = libgst.gst_buffer_map(ptr, mapping, flags)

    if not success:
        raise RuntimeError("Couldn't map buffer")

    try:
        # Cast POINTER(c_byte) to POINTER to array of c_byte with size mapping.size
        # Returns not pointer but the object to which pointer points
        return cast(mapping.data, POINTER(c_byte * mapping.size)).contents
    finally:
        libgst.gst_buffer_unmap(ptr, mapping)

class GstRenderer(object):
    def __init__(self, width, height, output):
        self.width, self.height = width, height

        self.surface = cairo.ImageSurface(cairo.FORMAT_RGB24, self.width, self.height)
        self.context = cairo.Context(self.surface)
        self.context.scale(1.0, 1.0)

        pipeline = "appsrc name=input emit-signals=false format=time do-timestamp=false is-live=false block=false caps=video/x-raw,width=%d,height=%d,format=BGRA,framerate=25/1,pixel-aspect-ratio=1/1,interlace-mode=progressive" % (self.width, self.height)
        pipeline += " ! videoconvert"
        pipeline += " ! queue"
        if output.endswith(".mov"):
            pipeline += " ! qtmux"
        else:
            raise Exception("Unsupported file ending for gst renderer: %s" % output)

#        if output.endswith(".ts"):
#            pipeline += " ! mpeg2enc format=5 aspect=3 framerate=3 bitrate=10000"
#            pipeline += " ! mpegvideoparse"
#            pipeline += " ! mpegtsmux"
#        elif output.endswith(".mkv"):
#            pipeline += " ! x264enc"
#            pipeline += " ! matroskamux"
#        else:
#            raise Exception("Unsupported file ending for gst renderer: %s" % output)

        pipeline += " ! filesink name=filesink"

        self.framebuf = Gst.Buffer.new_wrapped(b'\x00' * (4*width*height))
        self.framebuf.duration = 10**9 / 25
        self.framebuf.dts = 0
        self.framebuf.pts = 0
        self.mapped_framebuf = map_gst_buffer(self.framebuf, Gst.MapFlags.READ | Gst.MapFlags.WRITE)

        self.pipe = Gst.parse_launch(pipeline)
        self.appsrc = self.pipe.get_by_name("input")
        self.filesink = self.pipe.get_by_name("filesink")
        self.filesink.set_property("location", output)

        self.bus = self.pipe.get_bus()
        self.bus.add_signal_watch()

        self.pipe.set_state(Gst.State.PLAYING)

    def render_frame(self, svg):
        handle = Rsvg.Handle()
        svghandle = handle.new_from_data(svg.encode())

        width, height = svghandle.get_dimensions().width, svghandle.get_dimensions().height
        self.context.scale(self.width / width, self.height / height)
        svghandle.render_cairo(self.context)

        frame = bytes(self.surface.get_data())
        memmove(self.mapped_framebuf, frame, len(frame))

        self.framebuf.dts += self.framebuf.duration
        self.framebuf.pts = self.framebuf.dts

        self.appsrc.emit("push-buffer", self.framebuf)

    def close(self):
        self.appsrc.emit("end-of-stream")
        self.pipe.send_event(Gst.Event.new_eos())

        while True:
            message = self.bus.pop()
            if not message:
                time.sleep(0.1)
                continue
            if message.type == Gst.MessageType.EOS:
                break


        self.pipe.set_state(Gst.State.NULL)
