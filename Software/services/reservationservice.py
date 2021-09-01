def reservePlaceForTicketNumber(new_number):
    for count, place in enumerate(list_of_places):
        # Search an empty place
        if (place.state == PlaceState.FREE):
            # Found one - register ticket number to place
            print("Register ticket: " +
                  str(new_number) + " to free place")

            place.state = PlaceState.REGISTERED
            place.ticket_number = new_number
            list_of_labels_to_display_place_number[count].config(
                bg="green")
            list_of_labels_to_display_ticket_number[count].config(bg="yellow",
                                                                  text="Reserviert für " + str(place.ticket_number))
            break
        if (place == list_of_places[-1]):
            # Found no vacant place - put number in queue
            print("New number " + str(new_number))
            list_of_ticket_numbers.append(new_number)
            update_queue()