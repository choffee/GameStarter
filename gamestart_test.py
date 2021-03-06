#!/usr/bin/env python

import unittest
from gamestart import GameStarter

class TestStartButtons(unittest.TestCase):
	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_single_player(self):
		#It is invalid to have only one player. This should raise an exception
		try:
			gs = GameStarter(1, 1.0, 2.0)
			self.fail('Started with 1 player')
		except Exception as e:
			self.assertEqual('GameStarter.__init__: At least two players are required. Attempted to init GameStarter with 1 players.', str(e))

	def test_negative_player(self):
		#It is invalid to have only one player. This should raise an exception
		try:
			gs = GameStarter(-99999, 1.0, 2.0)
			self.fail('Started with -99999 player')
		except Exception as e:
			self.assertEqual('GameStarter.__init__: At least two players are required. Attempted to init GameStarter with -99999 players.', str(e))


	def test_invalid_levels(self):
		#It is invalid to have a negative active level threshold. This should raise an exception
		try:
			gs = GameStarter(2, -1.0, 2.0)
			self.fail('Started with invalid levels')
		except Exception as e:
			errorMsg = 'GameStarter.__init__: activeLevel must be greater than 0, startLevel must be greater than activeLevel.'
			self.assertEqual(errorMsg, str(e)[0:len(errorMsg)])

		try:
			gs2 = GameStarter(2, 1.0, 0.5)
			self.fail('Started with invalid levels')
		except Exception as e:
			errorMsg = 'GameStarter.__init__: activeLevel must be greater than 0, startLevel must be greater than activeLevel.'
			self.assertEqual(errorMsg, str(e)[0:len(errorMsg)])

		try:
			gs3 = GameStarter(2, 1.0, -23.0)
			self.fail('Started with invalid levels')
		except Exception as e:
			errorMsg = 'GameStarter.__init__: activeLevel must be greater than 0, startLevel must be greater than activeLevel.'

	def test_two_player_start(self):
		#test that two players can start a game
		try:
			gs = GameStarter(2, 1.0, 2.0)
		except Exception as e:
			self.fail('Exception during __init__')
		#Both players push
		gs.push(0)
		gs.push(1)
		#Wait for two seconds
		gs.timeStep(2.0)
		#By now, shouldStart must be true and there should be 2 startable players
		self.assertTrue(gs.shouldStart())
		self.assertEqual(2, gs.totalStartablePlayers())

	def test_single_player_cant_start(self):
		#test that single players cannot start a game
		try:
			gs = GameStarter(2, 1.0, 2.0)
		except Exception as e:
			self.fail('Exception during __init__')
		#One player pushes
		gs.push(0)
		#Wait for two seconds
		gs.timeStep(2.0)
		#shouldStart must be false
		self.assertFalse(gs.shouldStart())

	def test_two_player_start_with_four_player_game(self):
		#test that two players can start a game
		try:
			gs = GameStarter(4, 1.0, 2.0)
		except Exception as e:
			self.fail('Exception during __init__')
		#Both players push
		gs.push(0)
		gs.push(1)
		#Wait for two seconds
		gs.timeStep(2.0)
		#By now, shouldStart must be true and there should be 2 startable players
		self.assertTrue(gs.shouldStart())
		self.assertEqual(2, gs.totalStartablePlayers())

	def test_button_spam_filtering(self):
		#test that two players can start a game even when someone is button spamming
		try:
			gs = GameStarter(4, 1.0, 2.0)
		except Exception as e:
			self.fail('Exception during __init__')
		#Both players push
		gs.push(0)
		gs.push(1)
		#Wait for 1.5 seconds (nearly there)
		gs.timeStep(1.5)
		#player three then spams
		gs.push(2)
		gs.timeStep(0.7)
		gs.release(2)
		gs.timeStep(0.5)
		#By now, shouldStart must be true and there should be 2 startable players
		self.assertTrue(gs.shouldStart())
		self.assertEqual(2, gs.totalStartablePlayers())
		#Do more buttom mashing to see if the filter still works after this
		gs.push(2)
		gs.timeStep(0.7)
		gs.release(2)
		gs.timeStep(0.5)
		gs.push(2)
		gs.timeStep(0.7)
		gs.release(2)
		gs.timeStep(0.5)
		#shouldStart must stil be true and there should still be 2 startable players
		self.assertTrue(gs.shouldStart())
		self.assertEqual(2, gs.totalStartablePlayers())

	def test_late_joiners(self):
		#test that for players can start a game even when some people take a while to join in
		try:
			gs = GameStarter(4, 1.0, 2.0)
		except Exception as e:
			self.fail('Exception during __init__')
		#One players pushes
		gs.push(0)
		#Wait for 3 seconds (player 1 fully ready)...
		gs.timeStep(3.0)
		#Player two joins in
		gs.push(1)
		#a little later...
		gs.timeStep(0.8)
		#player three then joins
		gs.push(2)
		#later still..
		gs.timeStep(0.7)
		#player four pushes too
		gs.push(3)
		#another two seconds...
		gs.timeStep(2.0)
		#and now, shouldStart must be true and there should be 4 startable players
		self.assertTrue(gs.shouldStart())
		self.assertEqual(4, gs.totalStartablePlayers())

	def test_dodgy_button(self):
		#test that a dodgy button that flickers on and off sometimes doesn't cause problems
		#this also simulates people who fail to keep their hand on the button persistently
		try:
			gs = GameStarter(2, 1.0, 20.0) #note 20 second start time on this one
		except Exception as e:
			self.fail('Exception during __init__')
		#Both players push
		gs.push(0)
		gs.push(1)
		#Wait for 1.5 seconds (nearly there)...
		gs.timeStep(1.5)
		#Player two goes dodgy
		gs.release(1)
		gs.timeStep(0.1)
		gs.push(1)
		gs.timeStep(0.3)
		gs.release(1)
		gs.timeStep(0.2)
		gs.push(1)
		gs.timeStep(0.7)
		gs.release(1)
		gs.timeStep(0.04)
		gs.push(1)
		gs.timeStep(10.8)
		gs.release(1)
		gs.timeStep(0.2)
		gs.push(1)
		gs.timeStep(0.7)
		gs.release(1)
		gs.timeStep(0.04)
		gs.push(1)
		gs.timeStep(20.0) #long one to make sure

		#shouldStart must be true and there should be 2 startable players
		self.assertTrue(gs.shouldStart())
		self.assertEqual(2, gs.totalStartablePlayers())
		
		

if __name__ == '__main__':
    unittest.main()





