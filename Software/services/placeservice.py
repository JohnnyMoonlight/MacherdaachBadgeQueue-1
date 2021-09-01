def handleMessageFromPlace(json_loaded):
    if (json_loaded["place_occupied"] == True):
        # Place was taken by the owner of the ticket_number
        # Place number in MQTT-Message starts with 1 and must be decremented
        place_number = json_loaded["place_number"] - 1
        if (list_of_places[place_number].state == PlaceState.REGISTERED):
            occupyPlace(place_number)
        else:
            print(
                "Not occupied - there is no ticket registered to this place")
    else:
        # Place was given up by owner
        print("Released: " +
              str(json_loaded["place_number"]))
        place_number = json_loaded["place_number"] - 1

        if (list_of_places[place_number].state != PlaceState.OCCUPIED):
            print("Place is not in state OCCUPIED, but in state " + list_of_places[
                place_number].state + " - can not be released")
        else:
            releasePlace(place_number)
            if list_of_ticket_numbers:
                # ticket list is not empty - register number from ticket list to place
                # Take first element of list_of_ticket_numbers and register the number to the current place and display it
                ticket_number = list_of_ticket_numbers.pop(0)
                list_of_places[place_number].ticket_number = ticket_number
                list_of_places[place_number].state = PlaceState.REGISTERED
                list_of_labels_to_display_ticket_number[place_number].config(
                    text="%6d" % ticket_number)
                update_queue()


def releasePlace(place_number):
    processing_time = datetime.now(
        tz=None) - list_of_places[place_number].start_time
    list_of_places[place_number] = Place(place_number)
    list_of_labels_to_display_place_number[place_number].config(
        bg="green")
    list_of_labels_to_display_ticket_number[place_number].config(
        text="--")
    # Save processing time in
    print("Processing time: " + str(processing_time))
    list_of_processing_times.append(processing_time)
    # Search for a new number in list_of_ticket_numbers to be registered to the released place


def occupyPlace(place_number):
    print("Occupied: " + str(place_number))
    list_of_places[place_number].state = PlaceState.OCCUPIED
    list_of_labels_to_display_place_number[place_number].config(
        bg="red")
    list_of_labels_to_display_ticket_number[place_number].config(
        text="Belegt")
    list_of_places[place_number].start_time = datetime.now(
        tz=None)