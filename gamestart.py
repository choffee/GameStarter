#!/usr/bin/env python

import sys
import time


def validate_time(this_time):
    """Chechk the time is a valid one"""
    if this_time <= 0.0:
        raise Exception('Invalid time step')


class GamePlayer(object):
    """Representation of a Game player"""

    def __init__(self, active_level, level_for_start):
        self.active_level = active_level
        self.level_for_start = level_for_start
        self.state = 'OUT'
        self.level = 0.0
        self.pushed = False

    def inc(self, current_time):
        """inc, called when button is pushed and time is stepped"""
        if self.pushed:
            validate_time(current_time)

            if self.state == 'OUT':
                self.state = 'IN'

            self.level += current_time

            # XXX Is the nececcary?
            if self.level >= self.level_for_start:
                self.level = self.level_for_start

            if self.state == 'IN' and self.level >= self.active_level:
                self.state = 'ACTIVE'

            if self.state == 'ACTIVE' and self.level >= self.level_for_start:
                self.state = 'START'

    def dec(self, current_time):
        """dec, called when button is pushed and time is stepped"""
        if not self.pushed:
            validate_time(current_time)

            self.level -= current_time

            if self.level <= 0.0:
                self.level = 0.0
                self.state = 'OUT'

            # Anyone who had not reached active should
            # drop out as soon as they release
            if self.state == 'IN':
                self.state = 'OUT'
                self.level = 0.0

            # Anyone who drops below active
            # should drop out completely
            if (self.state == 'ACTIVE') and (self.level < self.active_level):
                self.state = 'OUT'
                self.level = 0.0


    def time_step(self, current_time):
        """Take a time step, increment or decrement
            depending on button pushed state"""
        if self.pushed:
            self.inc(current_time)
        if not self.pushed:
            self.dec(current_time)

    def push(self):
        """Set button state to pushed"""
        self.pushed = True


class GameStarter(object):
    """Contains the players and runs the game"""

    def __init__(self, max_players, active_level, start_level):
        """Initialise game starter"""
        if max_players < 2:
            raise Exception('GameStarter.__init__: At least two players are required. Attempted to init GameStarter with %d players.' % max_players)
        if (active_level <= 0.0) or (start_level <= active_level):
            raise Exception('GameStarter.__init__: active_level must be greater than 0, start_level must be greater than active_level. (Active: %f, Start: %f)' % (active_level, start_level))
        self.max_players = max_players
        self.players = [GamePlayer(active_level, start_level) for i in range(self.max_players)]

    def total_in_state(self, state):
        """get total number of players in given state"""
        tot = 0
        for i in range(self.max_players):
            if self.players[i].state == state:
                tot = tot+1
        return tot

    def is_startable_player(self, player_id):
        """Check if a player is able to start in this game
           A player will join a game when it starts if they are
           in START or ACTIVE state and have their button pushed"""
        player_state = self.players[player_id].state
        player_pushed = self.players[player_id].pushed
        if player_state == 'START':
            return True
        if player_state == 'ACTIVE' and player_pushed:
            return True
        return False

    def total_startable_players(self):
        """Get total number of startable players"""
        total = 0
        for i in range(self.max_players):
            if self.is_startable_player(i):
                total = total + 1
        return total

    def should_start(self):
        """You should start if you have:
         - at least two startable players
         - at least one player who has reached the start state
         - no players who have recently pressed (in)"""
        return (self.total_startable_players() > 1) \
            and (self.total_in_state('START') > 0) \
            and (self.total_in_state('IN') == 0)

    def push(self, player_id):
        """Push the given player's button"""
        self.players[player_id].pushed = True

    def release(self, player_id):
        """Release the given player's button"""
        self.players[player_id].pushed = False

    def time_step(self, time_increment):
        """Step all players by given time"""
        for i in range(self.max_players):
            self.players[i].time_step(time_increment)

if __name__ == '__main__':

    # Visual test of GameStarter

    # Set level thresholds here
    active_level = 2.0
    start_level = 5.0

    # Bar scale is number of characters that
    # represent one second on the visualisation
    bar_scale = 20

    # Some maths for the time bar graphics
    active_bar = int(active_level * bar_scale)
    start_bar = int(start_level * bar_scale)
    active_bar_string = '-' * (active_bar-1) + '|'
    start_bar_string = '-' * (start_bar-active_bar-1) + '|'

    # Get an instance of GameStarter with four players
    starter = GameStarter(4, active_level, start_level)

    # Print header for graphics
    print 'ID|' + active_bar_string + start_bar_string
    # Pad lines ready for cursor moving back
    for i in range(4):
        print ''

    # Begin with players two and four pressed
    starter.push(1)
    starter.push(3)
    start = False
    total_time = 0.0
    while not start:

        # Set specific times for events to happen here
        if total_time > 3.0:
            starter.release(1)
        if total_time > 5.2:
            starter.push(0)
        if total_time > 6.0:
            starter.push(1)
        if total_time > 6.4:
            starter.push(2)
        # End of event timings

        # Do time calculations
        time.sleep(0.05)
        starter.time_step(0.05)
        total_time += 0.05
        # Decide if game can start
        start = starter.should_start()

        # Step back four lines
        sys.stdout.write("\x1B[4A")
        # Print graphs
        for player in range(4):
            thislevel = starter.players[player].level
            print "%d |%s%s %s %s" % (i, ("#" * int(thislevel*bar_scale)), (" " * (int(bar_scale*start_level)-int(bar_scale*thislevel))), starter.players[player].state, str(starter.isPushed(player)) + '   ')

    # When game should start, get number of players in, print IDs
    num_players_in = 0

    print "Ready to start. Players:"
    for i in range(4):
        if starter.is_startable_player(i):
            num_players_in += 1
            print "\tPlayer %d" % i

    print "Start game with %d players." % num_players_in

