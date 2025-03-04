# This file has been autogenerated by the pywayland scanner

# Copyright © 2008-2011 Kristian Høgsberg
# Copyright © 2010-2011 Intel Corporation
# Copyright © 2012-2013 Collabora, Ltd.
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice (including the
# next paragraph) shall be included in all copies or substantial
# portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import enum

from pywayland.protocol_core import Argument, ArgumentType, Global, Interface, Proxy, Resource
from .wl_surface import WlSurface


class WlPointer(Interface):
    """Pointer input device

    The :class:`WlPointer` interface represents one or more input devices, such
    as mice, which control the pointer location and pointer_focus of a seat.

    The :class:`WlPointer` interface generates motion, enter and leave events
    for the surfaces that the pointer is located over, and button and axis
    events for button presses, button releases and scrolling.
    """

    name = "wl_pointer"
    version = 8

    class error(enum.IntEnum):
        role = 0

    class button_state(enum.IntEnum):
        released = 0
        pressed = 1

    class axis(enum.IntEnum):
        vertical_scroll = 0
        horizontal_scroll = 1

    class axis_source(enum.IntEnum):
        wheel = 0
        finger = 1
        continuous = 2
        wheel_tilt = 3


class WlPointerProxy(Proxy):
    interface = WlPointer

    @WlPointer.request(
        Argument(ArgumentType.Uint),
        Argument(ArgumentType.Object, interface=WlSurface, nullable=True),
        Argument(ArgumentType.Int),
        Argument(ArgumentType.Int),
    )
    def set_cursor(self, serial, surface, hotspot_x, hotspot_y):
        """Set the pointer surface

        Set the pointer surface, i.e., the surface that contains the pointer
        image (cursor). This request gives the surface the role of a cursor. If
        the surface already has another role, it raises a protocol error.

        The cursor actually changes only if the pointer focus for this device
        is one of the requesting client's surfaces or the surface parameter is
        the current pointer surface. If there was a previous surface set with
        this request it is replaced. If surface is NULL, the pointer image is
        hidden.

        The parameters hotspot_x and hotspot_y define the position of the
        pointer surface relative to the pointer location. Its top-left corner
        is always at (x, y) - (hotspot_x, hotspot_y), where (x, y) are the
        coordinates of the pointer location, in surface-local coordinates.

        On surface.attach requests to the pointer surface, hotspot_x and
        hotspot_y are decremented by the x and y parameters passed to the
        request. Attach must be confirmed by :func:`WlSurface.commit()
        <pywayland.protocol.wayland.WlSurface.commit>` as usual.

        The hotspot can also be updated by passing the currently set pointer
        surface to this request with new values for hotspot_x and hotspot_y.

        The current and pending input regions of the
        :class:`~pywayland.protocol.wayland.WlSurface` are cleared, and
        :func:`WlSurface.set_input_region()
        <pywayland.protocol.wayland.WlSurface.set_input_region>` is ignored
        until the :class:`~pywayland.protocol.wayland.WlSurface` is no longer
        used as the cursor. When the use as a cursor ends, the current and
        pending input regions become undefined, and the
        :class:`~pywayland.protocol.wayland.WlSurface` is unmapped.

        The serial parameter must match the latest :func:`WlPointer.enter()`
        serial number sent to the client. Otherwise the request will be
        ignored.

        :param serial:
            serial number of the enter event
        :type serial:
            `ArgumentType.Uint`
        :param surface:
            pointer surface
        :type surface:
            :class:`~pywayland.protocol.wayland.WlSurface` or `None`
        :param hotspot_x:
            surface-local x coordinate
        :type hotspot_x:
            `ArgumentType.Int`
        :param hotspot_y:
            surface-local y coordinate
        :type hotspot_y:
            `ArgumentType.Int`
        """
        self._marshal(0, serial, surface, hotspot_x, hotspot_y)

    @WlPointer.request(version=3)
    def release(self):
        """Release the pointer object

        Using this request a client can tell the server that it is not going to
        use the pointer object anymore.

        This request destroys the pointer proxy object, so clients must not
        call wl_pointer_destroy() after using this request.
        """
        self._marshal(1)
        self._destroy()


class WlPointerResource(Resource):
    interface = WlPointer

    @WlPointer.event(
        Argument(ArgumentType.Uint),
        Argument(ArgumentType.Object, interface=WlSurface),
        Argument(ArgumentType.Fixed),
        Argument(ArgumentType.Fixed),
    )
    def enter(self, serial, surface, surface_x, surface_y):
        """Enter event

        Notification that this seat's pointer is focused on a certain surface.

        When a seat's focus enters a surface, the pointer image is undefined
        and a client should respond to this event by setting an appropriate
        pointer image with the set_cursor request.

        :param serial:
            serial number of the enter event
        :type serial:
            `ArgumentType.Uint`
        :param surface:
            surface entered by the pointer
        :type surface:
            :class:`~pywayland.protocol.wayland.WlSurface`
        :param surface_x:
            surface-local x coordinate
        :type surface_x:
            `ArgumentType.Fixed`
        :param surface_y:
            surface-local y coordinate
        :type surface_y:
            `ArgumentType.Fixed`
        """
        self._post_event(0, serial, surface, surface_x, surface_y)

    @WlPointer.event(
        Argument(ArgumentType.Uint),
        Argument(ArgumentType.Object, interface=WlSurface),
    )
    def leave(self, serial, surface):
        """Leave event

        Notification that this seat's pointer is no longer focused on a certain
        surface.

        The leave notification is sent before the enter notification for the
        new focus.

        :param serial:
            serial number of the leave event
        :type serial:
            `ArgumentType.Uint`
        :param surface:
            surface left by the pointer
        :type surface:
            :class:`~pywayland.protocol.wayland.WlSurface`
        """
        self._post_event(1, serial, surface)

    @WlPointer.event(
        Argument(ArgumentType.Uint),
        Argument(ArgumentType.Fixed),
        Argument(ArgumentType.Fixed),
    )
    def motion(self, time, surface_x, surface_y):
        """Pointer motion event

        Notification of pointer location change. The arguments surface_x and
        surface_y are the location relative to the focused surface.

        :param time:
            timestamp with millisecond granularity
        :type time:
            `ArgumentType.Uint`
        :param surface_x:
            surface-local x coordinate
        :type surface_x:
            `ArgumentType.Fixed`
        :param surface_y:
            surface-local y coordinate
        :type surface_y:
            `ArgumentType.Fixed`
        """
        self._post_event(2, time, surface_x, surface_y)

    @WlPointer.event(
        Argument(ArgumentType.Uint),
        Argument(ArgumentType.Uint),
        Argument(ArgumentType.Uint),
        Argument(ArgumentType.Uint),
    )
    def button(self, serial, time, button, state):
        """Pointer button event

        Mouse button click and release notifications.

        The location of the click is given by the last motion or enter event.
        The time argument is a timestamp with millisecond granularity, with an
        undefined base.

        The button is a button code as defined in the Linux kernel's
        linux/input-event-codes.h header file, e.g. BTN_LEFT.

        Any 16-bit button code value is reserved for future additions to the
        kernel's event code list. All other button codes above 0xFFFF are
        currently undefined but may be used in future versions of this
        protocol.

        :param serial:
            serial number of the button event
        :type serial:
            `ArgumentType.Uint`
        :param time:
            timestamp with millisecond granularity
        :type time:
            `ArgumentType.Uint`
        :param button:
            button that produced the event
        :type button:
            `ArgumentType.Uint`
        :param state:
            physical state of the button
        :type state:
            `ArgumentType.Uint`
        """
        self._post_event(3, serial, time, button, state)

    @WlPointer.event(
        Argument(ArgumentType.Uint),
        Argument(ArgumentType.Uint),
        Argument(ArgumentType.Fixed),
    )
    def axis(self, time, axis, value):
        """Axis event

        Scroll and other axis notifications.

        For scroll events (vertical and horizontal scroll axes), the value
        parameter is the length of a vector along the specified axis in a
        coordinate space identical to those of motion events, representing a
        relative movement along the specified axis.

        For devices that support movements non-parallel to axes multiple axis
        events will be emitted.

        When applicable, for example for touch pads, the server can choose to
        emit scroll events where the motion vector is equivalent to a motion
        event vector.

        When applicable, a client can transform its content relative to the
        scroll distance.

        :param time:
            timestamp with millisecond granularity
        :type time:
            `ArgumentType.Uint`
        :param axis:
            axis type
        :type axis:
            `ArgumentType.Uint`
        :param value:
            length of vector in surface-local coordinate space
        :type value:
            `ArgumentType.Fixed`
        """
        self._post_event(4, time, axis, value)

    @WlPointer.event(version=5)
    def frame(self):
        """End of a pointer event sequence

        Indicates the end of a set of events that logically belong together. A
        client is expected to accumulate the data in all events within the
        frame before proceeding.

        All :class:`WlPointer` events before a :func:`WlPointer.frame()` event
        belong logically together. For example, in a diagonal scroll motion the
        compositor will send an optional :func:`WlPointer.axis_source()` event,
        two :func:`WlPointer.axis()` events (horizontal and vertical) and
        finally a :func:`WlPointer.frame()` event. The client may use this
        information to calculate a diagonal vector for scrolling.

        When multiple :func:`WlPointer.axis()` events occur within the same
        frame, the motion vector is the combined motion of all events. When a
        :func:`WlPointer.axis()` and a :func:`WlPointer.axis_stop()` event
        occur within the same frame, this indicates that axis movement in one
        axis has stopped but continues in the other axis. When multiple
        :func:`WlPointer.axis_stop()` events occur within the same frame, this
        indicates that these axes stopped in the same instance.

        A :func:`WlPointer.frame()` event is sent for every logical event
        group, even if the group only contains a single :class:`WlPointer`
        event. Specifically, a client may get a sequence: motion, frame,
        button, frame, axis, frame, axis_stop, frame.

        The :func:`WlPointer.enter()` and :func:`WlPointer.leave()` events are
        logical events generated by the compositor and not the hardware. These
        events are also grouped by a :func:`WlPointer.frame()`. When a pointer
        moves from one surface to another, a compositor should group the
        :func:`WlPointer.leave()` event within the same
        :func:`WlPointer.frame()`. However, a client must not rely on
        :func:`WlPointer.leave()` and :func:`WlPointer.enter()` being in the
        same :func:`WlPointer.frame()`. Compositor-specific policies may
        require the :func:`WlPointer.leave()` and :func:`WlPointer.enter()`
        event being split across multiple :func:`WlPointer.frame()` groups.
        """
        self._post_event(5)

    @WlPointer.event(
        Argument(ArgumentType.Uint),
        version=5,
    )
    def axis_source(self, axis_source):
        """Axis source event

        Source information for scroll and other axes.

        This event does not occur on its own. It is sent before a
        :func:`WlPointer.frame()` event and carries the source information for
        all events within that frame.

        The source specifies how this event was generated. If the source is
        :func:`WlPointer.axis_source()`.finger, a :func:`WlPointer.axis_stop()`
        event will be sent when the user lifts the finger off the device.

        If the source is :func:`WlPointer.axis_source()`.wheel,
        :func:`WlPointer.axis_source()`.wheel_tilt or
        :func:`WlPointer.axis_source()`.continuous, a
        :func:`WlPointer.axis_stop()` event may or may not be sent. Whether a
        compositor sends an axis_stop event for these sources is hardware-
        specific and implementation-dependent; clients must not rely on
        receiving an axis_stop event for these scroll sources and should treat
        scroll sequences from these scroll sources as unterminated by default.

        This event is optional. If the source is unknown for a particular axis
        event sequence, no event is sent. Only one
        :func:`WlPointer.axis_source()` event is permitted per frame.

        The order of :func:`WlPointer.axis_discrete()` and
        :func:`WlPointer.axis_source()` is not guaranteed.

        :param axis_source:
            source of the axis event
        :type axis_source:
            `ArgumentType.Uint`
        """
        self._post_event(6, axis_source)

    @WlPointer.event(
        Argument(ArgumentType.Uint),
        Argument(ArgumentType.Uint),
        version=5,
    )
    def axis_stop(self, time, axis):
        """Axis stop event

        Stop notification for scroll and other axes.

        For some :func:`WlPointer.axis_source()` types, a
        :func:`WlPointer.axis_stop()` event is sent to notify a client that the
        axis sequence has terminated. This enables the client to implement
        kinetic scrolling. See the :func:`WlPointer.axis_source()`
        documentation for information on when this event may be generated.

        Any :func:`WlPointer.axis()` events with the same axis_source after
        this event should be considered as the start of a new axis motion.

        The timestamp is to be interpreted identical to the timestamp in the
        :func:`WlPointer.axis()` event. The timestamp value may be the same as
        a preceding :func:`WlPointer.axis()` event.

        :param time:
            timestamp with millisecond granularity
        :type time:
            `ArgumentType.Uint`
        :param axis:
            the axis stopped with this event
        :type axis:
            `ArgumentType.Uint`
        """
        self._post_event(7, time, axis)

    @WlPointer.event(
        Argument(ArgumentType.Uint),
        Argument(ArgumentType.Int),
        version=5,
    )
    def axis_discrete(self, axis, discrete):
        """Axis click event

        Discrete step information for scroll and other axes.

        This event carries the axis value of the :func:`WlPointer.axis()` event
        in discrete steps (e.g. mouse wheel clicks).

        This event is deprecated with :class:`WlPointer` version 8 - this event
        is not sent to clients supporting version 8 or later.

        This event does not occur on its own, it is coupled with a
        :func:`WlPointer.axis()` event that represents this axis value on a
        continuous scale. The protocol guarantees that each axis_discrete event
        is always followed by exactly one axis event with the same axis number
        within the same :func:`WlPointer.frame()`. Note that the protocol
        allows for other events to occur between the axis_discrete and its
        coupled axis event, including other axis_discrete or axis events. A
        :func:`WlPointer.frame()` must not contain more than one axis_discrete
        event per axis type.

        This event is optional; continuous scrolling devices like two-finger
        scrolling on touchpads do not have discrete steps and do not generate
        this event.

        The discrete value carries the directional information. e.g. a value of
        -2 is two steps towards the negative direction of this axis.

        The axis number is identical to the axis number in the associated axis
        event.

        The order of :func:`WlPointer.axis_discrete()` and
        :func:`WlPointer.axis_source()` is not guaranteed.

        :param axis:
            axis type
        :type axis:
            `ArgumentType.Uint`
        :param discrete:
            number of steps
        :type discrete:
            `ArgumentType.Int`
        """
        self._post_event(8, axis, discrete)

    @WlPointer.event(
        Argument(ArgumentType.Uint),
        Argument(ArgumentType.Int),
        version=8,
    )
    def axis_value120(self, axis, value120):
        """Axis high-resolution scroll event

        Discrete high-resolution scroll information.

        This event carries high-resolution wheel scroll information, with each
        multiple of 120 representing one logical scroll step (a wheel detent).
        For example, an axis_value120 of 30 is one quarter of a logical scroll
        step in the positive direction, a value120 of -240 are two logical
        scroll steps in the negative direction within the same hardware event.
        Clients that rely on discrete scrolling should accumulate the value120
        to multiples of 120 before processing the event.

        The value120 must not be zero.

        This event replaces the :func:`WlPointer.axis_discrete()` event in
        clients supporting :class:`WlPointer` version 8 or later.

        Where a :func:`WlPointer.axis_source()` event occurs in the same
        :func:`WlPointer.frame()`, the axis source applies to this event.

        The order of :class:`WlPointer`.axis_value120 and
        :func:`WlPointer.axis_source()` is not guaranteed.

        :param axis:
            axis type
        :type axis:
            `ArgumentType.Uint`
        :param value120:
            scroll distance as fraction of 120
        :type value120:
            `ArgumentType.Int`
        """
        self._post_event(9, axis, value120)


class WlPointerGlobal(Global):
    interface = WlPointer


WlPointer._gen_c()
WlPointer.proxy_class = WlPointerProxy
WlPointer.resource_class = WlPointerResource
WlPointer.global_class = WlPointerGlobal
