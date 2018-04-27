from flask import *
import uuid
import stockfish
stockfish = stockfish.Stockfish()

app = Flask(__name__)

#commands:
#nanokv.execute('store <key>', value) -> None
#nanokv.execute('search <key>') -> Bool
#nanokv.execute('get <key>') -> List


class chessd_nanokv:
	def __init__(self):
		self._kv = dict()
	def execute(self, cmd, lst=None):
		cmd = cmd.split()
		if cmd[0] == 'store':
			self._kv[cmd[1]] = lst
			return
		if cmd[0] == 'search':
			if cmd[1] in self._kv.keys():
				return True
			return False

		if cmd[0] == 'get':
			return self._kv[cmd[1]]


@app.route('/', methods=['GET'])
def default():
	return render_template('static.html'), 200

db = chessd_nanokv()

@app.route('/new', methods = ['POST', 'GET'])
def new_instance():
	token = uuid.uuid4().hex
	print('chessd: new instance with token:', token)
	db.execute('store {}'.format(token), list())
	return token, 200

@app.route('/move/<token>/<move>', methods = ['POST', 'GET'])
def move(token, move):
	try:
		pos = db.execute('get {}'.format(token))
		stockfish.set_position(pos)
		if stockfish.is_move_correct(move):
			pos.append(move)
		else:
			return 'incorrect move', 400
		db.execute('store {}'.format(token), pos)
		print('chessd: responded with token:', token)
		return str(pos), 200
	except KeyError as e:
		print('rngd: 404 with token:', token)
		return 'no such token', 404

@app.route('/best/<token>', methods = ['POST', 'GET'])
def best(token):
	try:
		pos = db.execute('get {}'.format(token))
		stockfish.set_position(pos)
		move = stockfish.get_best_move()
		print('chessd: responded with token:', token)
		return move, 200
	except KeyError as e:
		print('rngd: 404 with token:', token)
		return 'no such token', 404


if __name__ == '__main__':
	app.run(debug=True)