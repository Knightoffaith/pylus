"""
Game message handling
"""

from pyraknet.bitstream import ReadStream, WriteStream, c_int64, c_int, c_bit, c_uint32, c_uint8

from enums import GameMessageID
from structs import ClientGameMessage, ServerGameMessage
from plugin import Action, Plugin


class GameMessageHandler(Plugin):
    """
    Game message handler
    """
    def actions(self):
        """
        Returns the actions for the game message handler
        """
        return [
            Action('pkt:client_game_message', self.client_game_message, 10),
        ]

    def packets(self):
        """
        Returns the packets for the game message handler
        """
        return [
            ClientGameMessage
        ]

    def client_game_message(self, packet, address):
        """
        Handles the game messages
        """
        if packet.extra_data:
            stream = ReadStream(packet.extra_data)

        if packet.message_id == GameMessageID.REQUEST_USE:
            self.request_use(packet, address, stream)
        elif packet.message_id == GameMessageID.MISSION_DIALOGUE_OK:
            self.mission_accept(packet, address, stream)
        elif packet.message_id == GameMessageID.REQUEST_LINKED_MISSION:
            self.request_linked_mission(packet, address, stream)
        elif packet.message_id == 888:
            pass
        else:
            print(f'Unhandled game message: {packet.message_id}')

    def request_use(self, packet, address, stream):
        """
        Handles the request use game message
        """
        session = self.server.handle_until_return('session:get_session', address)
        clone = self.server.handle_until_return('world:get_clone', session.clone)

        multiinteract = stream.read(c_bit)
        multiinteract_id = stream.read(c_uint32)
        multiinteract_type = stream.read(c_int)
        objid = stream.read(c_int64)
        secondary = stream.read(c_bit)

        print(f'Multi interact: {multiinteract}')
        print(f'Multi interact ID: {multiinteract_id}')
        print(f'Multi interact type: {multiinteract_type}')
        print(f'Object ID: {objid}')
        print(f'Secondary: {secondary}')

        obj = [x for x in clone.objects if x.objid == objid][0]

        missions = self.server.handle_until_return('world:missions_for_lot', obj.lot)

        if missions:
            mission = missions[0]

            msg = ServerGameMessage(packet.objid, GameMessageID.OFFER_MISSION, c_int(mission[0]) + c_int64(objid))

            self.server.rnserver.send(msg, address)

    def request_linked_mission(self, packet, address, stream):
        """
        Handles the request linked mission game message
        """
        objid = stream.read(c_int64)
        mission = stream.read(c_int)
        offered = stream.read(c_bit)

        print(f'Request for linked mission {mission}')
        print(f'Object ID: {objid}')
        print(f'Offered: {offered}')

    def mission_accept(self, packet, address, stream):
        """
        Handles the mission dialogue ok game message
        """
        complete = stream.read(c_bit)
        state = stream.read(c_int)
        mission_id = stream.read(c_int)
        responder_objid = stream.read(c_int64)

        print(f'Mission {mission_id} accepted')
        print(f'Complete: {complete}')
        print(f'State: {state}')
        print(f'Responder: {responder_objid}')

        session = self.server.handle_until_return('session:get_session', address)
        char = self.server.handle_until_return('char:characters', session.account.user.id)[session.account.front_character]
        self.server.handle('char:complete_mission', char.id, mission_id)

        wstr = WriteStream()
        wstr.write(c_int(mission_id))
        wstr.write(c_int(1 << 5))
        wstr.write(c_uint8(0))

        msg = ServerGameMessage(packet.objid, GameMessageID.NOTIFY_MISSION_TASK, wstr)

        self.server.rnserver.send(msg, address)
