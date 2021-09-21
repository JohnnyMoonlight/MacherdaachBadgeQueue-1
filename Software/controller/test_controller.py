import json
from unittest import TestCase

from controller import Controller
from model.place import Place, PlaceState

c = Controller()


class TestController(TestCase):

    def test_reserve_place_for_ticket_number(self):
        reserved_place = c.reservePlaceForTicketNumber(0, 1)
        self.assertTrue(c.model.list_of_places[0] == Place(PlaceState.REGISTERED, 1))
        reserved_place.clear_place()

    def test_occupy_place(self):
        occupied_place = c.occupyPlace(1)
        self.assertTrue(occupied_place.state == PlaceState.OCCUPIED)

    def test_handle_message_from_place_for_illegal_json(self):
        illegal_json_from_place = json.loads('{"place_number": 1,"place_occupiedTYPOERROR": false}')
        self.assertRaises(Exception, c.handle_message_from_place, illegal_json_from_place)

    def test_handle_message_from_place_for_number_out_of_capacity(self):
        illegal_json_from_place = json.loads(
            '{"place_number": ' + str(9999) + ',"place_occupied": false}')
        self.assertRaises(Exception, c.handle_message_from_place, illegal_json_from_place)

    def test_handle_new_ticket_number(self):
        new_ticket_json = json.loads('{"new_number":2}')
        c.handle_message_from_controller(new_ticket_json)
        self.assertTrue(c.model.list_of_places[0] == Place(PlaceState.REGISTERED, 2))

        # Assigning the same ticket number again raises exception
        self.assertRaises(Exception, c.handle_message_from_controller, new_ticket_json)

        for i in range(3, 13):
            next_new_ticket = json.loads('{"new_number":' + str(i) + '}')
            c.handle_message_from_controller(next_new_ticket)
        self.assertTrue(len(c.model.list_of_ticket_numbers) == 3)
