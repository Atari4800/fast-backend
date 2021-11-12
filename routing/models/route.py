import copy
import os
import sys
from collections import deque
from datetime import datetime

from neomodel import StructuredNode, RelationshipTo, FloatProperty, DateTimeProperty, IntegerProperty

working_dir = os.path.abspath(os.path.join('.'))
if working_dir not in sys.path:
    sys.path.append(working_dir)

from routing.managers import LocationManager
from routing.models.location import Address, Pair, Customer, Depot
from routing.exceptions import EmptyRouteException, RouteStateException


class Route(StructuredNode):
    id = IntegerProperty()
    total_quantity = FloatProperty(index=True)
    total_distance = FloatProperty(index=True)
    total_duration = FloatProperty(index=True)
    created_on = DateTimeProperty(default=datetime.now)

    assigned_to = RelationshipTo('routing.models.driver.Driver', 'ASSIGNED_TO')

    def __init__(self, *args, **kwargs):
        super(Route, self).__init__(*args, **kwargs)
        self.customers_queue: deque = deque()
        self.total_quantity: float = 0
        self.total_duration: float = 0
        self.total_distance: float = 0
        self.is_open: bool = True
        self.departure = None
        self.stop = None
        self.tail = None

    @property
    def previous(self):
        return self.customers_queue[-1] if len(self.customers_queue) > 0 else None

    def add(self, customer: Customer, pair: Pair) -> bool:
        """
        Add a location to route based on insertion rules. Return True is addition was successful, otherwise,
        return False
        """
        if self.is_open:
            if len(self.customers_queue) == 0:
                if self.departure is None:
                    raise RouteStateException('This route has no departure. Set the departure before proceeding.')
                self.customers_queue.append(self.departure)
                # self.departure.is_assigned = True
                self.tail = self.departure
            if customer and (not customer.is_assigned):
                if len(self.customers_queue) == 1:
                    self.insert_front(customer=customer)
                elif pair.is_first(customer) and not pair.first.is_assigned:
                    print(f'Location {customer} is first and head is {self.departure.next}')
                    if self.is_exterior(pair.last):
                        print(f'Location {pair.last} is exterior')
                        if pair.last == self.departure.next:
                            if self.departure.next.next is None:
                                self.insert_front(customer)
                                print(f'Inserting {customer} to the front')
                            else:
                                self.insert_back(location=customer)
                                print(f'Inserting {customer} to the back')
                        elif pair.last == self.tail:
                            self.insert_front(customer=customer)
                            print(f'Inserting {customer} to the front')
                elif pair.is_last(customer) and not pair.last.is_assigned:
                    print(f'Location {customer} is last and tail is {self.tail}')
                    if self.is_exterior(pair.first):
                        print(f'Location {pair.first} is exterior')
                        if pair.first == self.departure.next:
                            if self.departure.next.next is None:
                                self.insert_front(customer)
                                print(f'Inserting {customer} to the front')
                            else:
                                self.insert_back(customer)
                                print(f'Inserting {customer} to the back')
                        elif pair.first == self.tail:
                            self.insert_front(customer)
                            print(f'Inserting {customer} to the front')
                print('\t\t\033[1mProcessing location\033[0m {} \033[1mCapacity:\033[0m {} \033[1mAssigned:\033[0m {}'
                      .format(customer, customer.demand, customer.is_assigned))
                print('\t\t\t\033[1mLocations: \033[0m {}'.format(self))
                return True
            else:
                print(f'{customer} is already assigned.')
            if self.previous == self.departure:
                self.undo()
        return False if customer is None else customer.is_assigned

    def insert_front(self, customer: Customer):
        """Inserts this customer at the beginning of this route.

        This customer is inserted after the departure.
        """
        if len(self.customers_queue) == 0 or self.departure is None:
            raise RouteStateException('This route has no departure. Set the departure before proceeding.')
        else:
            self.total_duration += self.tail.duration(other=customer)
            self.total_distance += self.tail.distance(other=customer)
            self.total_quantity += customer.demand

            if len(self.customers_queue) == 1:
                self.departure.locate.next = customer.locate
                customer.locate.previous = self.departure.locate
            else:
                customer.locate.previous = self.tail.locate
                self.tail.locate.next = customer.locate
            self.tail = customer
            self.customers_queue.append(customer)
            customer.is_assigned = True

    def insert_back(self, location: Address):
        """Insert this location at the end of this route."""
        if len(self.customers_queue) == 0 or self.departure is None:
            raise RouteStateException('This route has no departure. Set the departure before proceeding.')
        elif len(self.customers_queue) == 1:
            raise RouteStateException('No insertion can\'t be made on the rear.')
        else:
            self.total_duration = (
                    self.total_duration
                    - LocationManager.get_duration(location1=self.departure, location2=self.departure.next)
                    + LocationManager.get_duration(self.departure, location)
                    + LocationManager.get_duration(location, self.departure.next)
            )
            self.total_distance = (
                    self.total_distance
                    - LocationManager.get_distance(location1=self.departure, location2=self.departure.next)
                    + LocationManager.get_distance(self.departure, location)
                    + LocationManager.get_distance(location, self.departure.next)
            )
            self.total_quantity += location.demand
            location.next = self.departure.next
            self.departure.next.previous = location
            location.previous = self.departure
            self.departure.next = location
            self.customers_queue.append(location)
            location.is_assigned = True

    def is_exterior(self, location: Address):
        if len(self.customers_queue) == 0:
            raise EmptyRouteException('This route is empty')

        return self.departure.next == location or self.tail == location

    def undo(self):
        """Removes last inserted location.

        The last inserted location is the last entry in the deque. It is either the head or the tail of the route.
        """
        if self.previous is not None:
            last_inserted = self.customers_queue.pop()
            if last_inserted == self.departure:
                self.customers_queue.append(last_inserted)
                self.total_quantity = 0
                self.total_duration = 0
                self.total_distance = 0
            else:
                if last_inserted == self.departure.next:
                    last_inserted.previous.next = last_inserted.next
                    if last_inserted.next:
                        last_inserted.next.previous = last_inserted.previous

                    self.total_duration = (
                            self.total_duration - LocationManager.get_duration(self.departure, last_inserted)
                            - LocationManager.get_duration(last_inserted, self.departure.next)
                            + LocationManager.get_duration(self.departure, self.departure.next)
                    )

                    self.total_distance = (
                            self.total_distance - LocationManager.get_distance(self.departure, last_inserted)
                            - LocationManager.get_distance(last_inserted, self.departure.next)
                            + LocationManager.get_distance(self.departure, self.departure.next)
                    )
                elif last_inserted == self.tail:
                    last_inserted.previous.next = last_inserted.next
                    self.tail = last_inserted.previous

                    # Adjust route distance and duration
                    self.total_duration = (
                            self.total_duration - LocationManager.get_duration(self.previous, last_inserted)
                    )
                    self.total_distance = (
                            self.total_distance - LocationManager.get_distance(self.previous, last_inserted)
                    )
                self.total_quantity -= last_inserted.demand
                last_inserted.is_assigned = False

    def last_location(self) -> Address:
        return self.customers_queue[-1] if len(self.customers_queue) > 0 else None

    def close_route(self):
        if self.departure and self.departure.next is None:
            self.customers_queue = deque()
            self.departure = None
        elif self.is_open:
            self.stop = copy.deepcopy(self.departure)
            self.customers_queue.append(self.stop)
            self.stop.previous = self.tail
            self.tail.next = self.stop
            self.stop.next = None
            self.tail = self.stop
            self.stop.is_assigned = True
            self.is_open = False
            self.total_duration += LocationManager.get_duration(self.tail, self.stop)
            self.total_distance += LocationManager.get_distance(self.tail, self.stop)

    def get_total_distance(self):
        return self.total_distance

    def get_total_duration(self):
        return self.total_duration

    def get_total_demand(self):
        return self.total_quantity

    def get_created_on(self):
        return self.created_on

    def serialize(self):
        pass

    def __len__(self):
        return len(self.customers_queue)

    def __str__(self):
        location = self.departure
        path = ''
        while location:
            if location.next:
                path += str(location) + '\033[1m --> \033[0m'
            else:
                path += str(location)
            location = location.next
        return path

    def __eq__(self, other):
        if not isinstance(other, type(self)):
            return NotImplemented

        if len(self.customers_queue) != len(other.customers_queue):
            return False

        for index in range(len(self.customers_queue)):
            if self.customers_queue[index] != other.customers_queue[index]:
                return False

        return True

    @classmethod
    def category(cls):
        pass
