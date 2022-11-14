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


class WlDataOffer(Interface):
    """Offer to transfer data

    A :class:`WlDataOffer` represents a piece of data offered for transfer by
    another client (the source client).  It is used by the copy-and-paste and
    drag-and-drop mechanisms.  The offer describes the different mime types
    that the data can be converted to and provides the mechanism for
    transferring the data directly from the source client.
    """

    name = "wl_data_offer"
    version = 3

    class error(enum.IntEnum):
        invalid_finish = 0
        invalid_action_mask = 1
        invalid_action = 2
        invalid_offer = 3


class WlDataOfferProxy(Proxy):
    interface = WlDataOffer

    @WlDataOffer.request(
        Argument(ArgumentType.Uint),
        Argument(ArgumentType.String, nullable=True),
    )
    def accept(self, serial, mime_type):
        """Accept one of the offered mime types

        Indicate that the client can accept the given mime type, or NULL for
        not accepted.

        For objects of version 2 or older, this request is used by the client
        to give feedback whether the client can receive the given mime type, or
        NULL if none is accepted; the feedback does not determine whether the
        drag-and-drop operation succeeds or not.

        For objects of version 3 or newer, this request determines the final
        result of the drag-and-drop operation. If the end result is that no
        mime types were accepted, the drag-and-drop operation will be cancelled
        and the corresponding drag source will receive
        :func:`WlDataSource.cancelled()
        <pywayland.protocol.wayland.WlDataSource.cancelled>`. Clients may still
        use this event in conjunction with :func:`WlDataSource.action()
        <pywayland.protocol.wayland.WlDataSource.action>` for feedback.

        :param serial:
            serial number of the accept request
        :type serial:
            `ArgumentType.Uint`
        :param mime_type:
            mime type accepted by the client
        :type mime_type:
            `ArgumentType.String` or `None`
        """
        self._marshal(0, serial, mime_type)

    @WlDataOffer.request(
        Argument(ArgumentType.String),
        Argument(ArgumentType.FileDescriptor),
    )
    def receive(self, mime_type, fd):
        """Request that the data is transferred

        To transfer the offered data, the client issues this request and
        indicates the mime type it wants to receive.  The transfer happens
        through the passed file descriptor (typically created with the pipe
        system call).  The source client writes the data in the mime type
        representation requested and then closes the file descriptor.

        The receiving client reads from the read end of the pipe until EOF and
        then closes its end, at which point the transfer is complete.

        This request may happen multiple times for different mime types, both
        before and after :func:`WlDataDevice.drop()
        <pywayland.protocol.wayland.WlDataDevice.drop>`. Drag-and-drop
        destination clients may preemptively fetch data or examine it more
        closely to determine acceptance.

        :param mime_type:
            mime type desired by receiver
        :type mime_type:
            `ArgumentType.String`
        :param fd:
            file descriptor for data transfer
        :type fd:
            `ArgumentType.FileDescriptor`
        """
        self._marshal(1, mime_type, fd)

    @WlDataOffer.request()
    def destroy(self):
        """Destroy data offer

        Destroy the data offer.
        """
        self._marshal(2)
        self._destroy()

    @WlDataOffer.request(version=3)
    def finish(self):
        """The offer will no longer be used

        Notifies the compositor that the drag destination successfully finished
        the drag-and-drop operation.

        Upon receiving this request, the compositor will emit
        :func:`WlDataSource.dnd_finished()
        <pywayland.protocol.wayland.WlDataSource.dnd_finished>` on the drag
        source client.

        It is a client error to perform other requests than
        :func:`WlDataOffer.destroy()` after this one. It is also an error to
        perform this request after a NULL mime type has been set in
        :func:`WlDataOffer.accept()` or no action was received through
        :func:`WlDataOffer.action()`.

        If :func:`WlDataOffer.finish()` request is received for a non drag and
        drop operation, the invalid_finish protocol error is raised.
        """
        self._marshal(3)

    @WlDataOffer.request(
        Argument(ArgumentType.Uint),
        Argument(ArgumentType.Uint),
        version=3,
    )
    def set_actions(self, dnd_actions, preferred_action):
        """Set the available/preferred drag-and-drop actions

        Sets the actions that the destination side client supports for this
        operation. This request may trigger the emission of
        :func:`WlDataSource.action()
        <pywayland.protocol.wayland.WlDataSource.action>` and
        :func:`WlDataOffer.action()` events if the compositor needs to change
        the selected action.

        This request can be called multiple times throughout the drag-and-drop
        operation, typically in response to :func:`WlDataDevice.enter()
        <pywayland.protocol.wayland.WlDataDevice.enter>` or
        :func:`WlDataDevice.motion()
        <pywayland.protocol.wayland.WlDataDevice.motion>` events.

        This request determines the final result of the drag-and-drop
        operation. If the end result is that no action is accepted, the drag
        source will receive :func:`WlDataSource.cancelled()
        <pywayland.protocol.wayland.WlDataSource.cancelled>`.

        The dnd_actions argument must contain only values expressed in the
        :func:`WlDataDeviceManager.dnd_actions()
        <pywayland.protocol.wayland.WlDataDeviceManager.dnd_actions>` enum, and
        the preferred_action argument must only contain one of those values
        set, otherwise it will result in a protocol error.

        While managing an "ask" action, the destination drag-and-drop client
        may perform further :func:`WlDataOffer.receive()` requests, and is
        expected to perform one last :func:`WlDataOffer.set_actions()` request
        with a preferred action other than "ask" (and optionally
        :func:`WlDataOffer.accept()`) before requesting
        :func:`WlDataOffer.finish()`, in order to convey the action selected by
        the user. If the preferred action is not in the
        :func:`WlDataOffer.source_actions()` mask, an error will be raised.

        If the "ask" action is dismissed (e.g. user cancellation), the client
        is expected to perform :func:`WlDataOffer.destroy()` right away.

        This request can only be made on drag-and-drop offers, a protocol error
        will be raised otherwise.

        :param dnd_actions:
            actions supported by the destination client
        :type dnd_actions:
            `ArgumentType.Uint`
        :param preferred_action:
            action preferred by the destination client
        :type preferred_action:
            `ArgumentType.Uint`
        """
        self._marshal(4, dnd_actions, preferred_action)


class WlDataOfferResource(Resource):
    interface = WlDataOffer

    @WlDataOffer.event(
        Argument(ArgumentType.String),
    )
    def offer(self, mime_type):
        """Advertise offered mime type

        Sent immediately after creating the :class:`WlDataOffer` object.  One
        event per offered mime type.

        :param mime_type:
            offered mime type
        :type mime_type:
            `ArgumentType.String`
        """
        self._post_event(0, mime_type)

    @WlDataOffer.event(
        Argument(ArgumentType.Uint),
        version=3,
    )
    def source_actions(self, source_actions):
        """Notify the source-side available actions

        This event indicates the actions offered by the data source. It will be
        sent right after :func:`WlDataDevice.enter()
        <pywayland.protocol.wayland.WlDataDevice.enter>`, or anytime the source
        side changes its offered actions through
        :func:`WlDataSource.set_actions()
        <pywayland.protocol.wayland.WlDataSource.set_actions>`.

        :param source_actions:
            actions offered by the data source
        :type source_actions:
            `ArgumentType.Uint`
        """
        self._post_event(1, source_actions)

    @WlDataOffer.event(
        Argument(ArgumentType.Uint),
        version=3,
    )
    def action(self, dnd_action):
        """Notify the selected action

        This event indicates the action selected by the compositor after
        matching the source/destination side actions. Only one action (or none)
        will be offered here.

        This event can be emitted multiple times during the drag-and-drop
        operation in response to destination side action changes through
        :func:`WlDataOffer.set_actions()`.

        This event will no longer be emitted after :func:`WlDataDevice.drop()
        <pywayland.protocol.wayland.WlDataDevice.drop>` happened on the drag-
        and-drop destination, the client must honor the last action received,
        or the last preferred one set through :func:`WlDataOffer.set_actions()`
        when handling an "ask" action.

        Compositors may also change the selected action on the fly, mainly in
        response to keyboard modifier changes during the drag-and-drop
        operation.

        The most recent action received is always the valid one. Prior to
        receiving :func:`WlDataDevice.drop()
        <pywayland.protocol.wayland.WlDataDevice.drop>`, the chosen action may
        change (e.g. due to keyboard modifiers being pressed). At the time of
        receiving :func:`WlDataDevice.drop()
        <pywayland.protocol.wayland.WlDataDevice.drop>` the drag-and-drop
        destination must honor the last action received.

        Action changes may still happen after :func:`WlDataDevice.drop()
        <pywayland.protocol.wayland.WlDataDevice.drop>`, especially on "ask"
        actions, where the drag-and-drop destination may choose another action
        afterwards. Action changes happening at this stage are always the
        result of inter-client negotiation, the compositor shall no longer be
        able to induce a different action.

        Upon "ask" actions, it is expected that the drag-and-drop destination
        may potentially choose a different action and/or mime type, based on
        :func:`WlDataOffer.source_actions()` and finally chosen by the user
        (e.g. popping up a menu with the available options). The final
        :func:`WlDataOffer.set_actions()` and :func:`WlDataOffer.accept()`
        requests must happen before the call to :func:`WlDataOffer.finish()`.

        :param dnd_action:
            action selected by the compositor
        :type dnd_action:
            `ArgumentType.Uint`
        """
        self._post_event(2, dnd_action)


class WlDataOfferGlobal(Global):
    interface = WlDataOffer


WlDataOffer._gen_c()
WlDataOffer.proxy_class = WlDataOfferProxy
WlDataOffer.resource_class = WlDataOfferResource
WlDataOffer.global_class = WlDataOfferGlobal
