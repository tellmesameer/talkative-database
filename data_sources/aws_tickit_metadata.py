tickit_metadata = """
Database: sample_data_dev
Schema: tickit

Table: sample_data_dev.tickit.category
- catid (integer): Unique category ID.
- catgroup (varchar): Group this category belongs to.
- catname (varchar): Name of the category.
- catdesc (varchar): Description of the category.

Table: sample_data_dev.tickit.date
- dateid (integer): Date surrogate key.
- caldate (date): Calendar date.
- day (integer): Day of the month.
- week (integer): Week number.
- month (integer): Month number.
- qtr (integer): Quarter.
- year (integer): Year.
- holiday (boolean): Whether the day is a holiday.

Table: sample_data_dev.tickit.event
- eventid (integer): Unique ID for each event.
- venueid (integer): Foreign key to venue.
- catid (integer): Foreign key to category.
- dateid (integer): Foreign key to date.
- eventname (varchar): Name of the event.
- starttime (timestamp): Event start time.

Table: sample_data_dev.tickit.listing
- listid (integer): Unique listing ID.
- sellerid (integer): Foreign key to users.
- eventid (integer): Foreign key to event.
- dateid (integer): Foreign key to date.
- numtickets (integer): Number of tickets available.
- priceperticket (decimal): Price per ticket.
- totalprice (decimal): Total price.
- listtime (timestamp): Time listing was created.

Table: sample_data_dev.tickit.sales
- salesid (integer): Unique sale ID.
- listid (integer): Foreign key to listing.
- sellerid (integer): Seller user ID.
- buyerid (integer): Buyer user ID.
- eventid (integer): Event ID.
- dateid (integer): Date ID.
- qtysold (integer): Number of tickets sold.
- pricepaid (decimal): Total price paid.
- commission (decimal): Commission taken.
- saletime (timestamp): Time of the sale.

Table: sample_data_dev.tickit.users
- userid (integer): Unique user ID.
- username (varchar): User’s full name.
- city (varchar): User's city.
- state (varchar): User's state.
- email (varchar): User's email.
- phone (varchar): Phone number.
- likesports (boolean): User likes sports.
- liketheatre (boolean): User likes theatre.
- likeconcerts (boolean): User likes concerts.
- likejazz (boolean): User likes jazz.
- likeclassical (boolean): User likes classical.
- likeopera (boolean): User likes opera.
- likerock (boolean): User likes rock.
- likevegas (boolean): User likes Vegas shows.
- likebroadway (boolean): User likes Broadway.
- likemusicals (boolean): User likes musicals.

Table: sample_data_dev.tickit.venue
- venueid (integer): Unique venue ID.
- venuename (varchar): Name of the venue.
- venuecity (varchar): City.
- venuestate (varchar): State.
- venueseats (integer): Total number of seats.
"""
