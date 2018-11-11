import Pyro4

@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class GameForca(object):
    def __init__(self):
        self.word = 'PARALELEPIPEDO'
        self.chance = 5
        self.letters_tried = []
        self.pos_letter = None
        self.grid = []
        for row in range(2):
            self.grid.append([])
            for col in range(13):
                self.grid[row].append(0)
        self.name = None
        self.players_online = 0


    def get_word(self):
        return list(self.word)

    def get_chance(self):
        return self.chance

    def set_players_online(self):
        self.players_online += 1

    def set_players_offline(self):
        self.players_online -= 1

    def get_players_online(self):
        return self.players_online

    def get_letters_tried(self):
        return self.letters_tried

    def get_pos_letter(self):
        return self.pos_letter

    def get_grid(self):
        return self.grid

    def set_grid(self, pos_letter):
        row, col = pos_letter
        self.grid[int(row)][int(col)] = 1

    def set_pos_letter(self, row, col):
        self.pos_letter = (row, col)

    def try_find_letter(self, letter):
        letter = str(letter)
        for _ in range(len(list(self.word))):
            if letter == str(self.word[_]):
                self.letters_tried.append(int(_))
        if not letter in list(self.word):
            return 1

    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

daemon = Pyro4.Daemon()                # make a Pyro daemon
ns = Pyro4.locateNS()                  # find the name server
uri = daemon.register(GameForca)       # register the greeting maker as a Pyro object
ns.register("game_forca", uri)         # register the object with a name in the name server
print("Ready.")
daemon.requestLoop()                   # start the event loop of the server to wait for calls