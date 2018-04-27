##simple testing routines
class chessd_test:
	_t_counter = 0
	_failed = 0

	def _assert(msg, expr):
		chessd_test._t_counter += 1
		if expr:
			print('chessd_test: [{}] passed'.format(msg))
		else:
			print('chessd_test: [{}] failed!'.format(msg))
			chessd_test._failed += 1
	def _finish():
		print('chessd_test: {}/{} tests failed'.format(chessd_test._failed, chessd_test._t_counter))


from chessd import *

##nanokv tests
testdb = chessd_nanokv()

testdb.execute('store test', ['a', 'b'])
chessd_test._assert('nanokv store/get', testdb.execute('get test')==['a', 'b'])
chessd_test._assert('nanokv search', testdb.execute('search test'))


##stockfish tests
stockfish.set_position(['e2e4'])
chessd_test._assert('stockfish correct 1/2', stockfish.is_move_correct('d7d5'))
chessd_test._assert('stockfish move', stockfish.get_best_move()=='d7d5')
stockfish.set_position(['e2e4', 'd7d5'])

chessd_test._assert('stockfish correct 2/2', not stockfish.is_move_correct('d7d5'))




chessd_test._finish()

