# import ants, importlib
# importlib.reload(ants)

# beehive = ants.Hive(ants.AssaultPlan())
# dimensions = (2, 9)
# gamestate = ants.GameState(None, beehive, ants.ant_types(),ants.dry_layout, dimensions, food=20)
# ants.ants_lose = lambda: None

# print(gamestate.already_queen)
# queen = ants.QueenAnt.construct(gamestate)
# print(gamestate.already_queen)
# print(queen)
# test = ants.ScubaThrower.construct(gamestate)
# print(test)
# impostor = ants.QueenAnt.construct(gamestate)
# impostor is None # you cannot create a second QueenAnt!

# front_ant, back_ant = ants.ThrowerAnt(), ants.ThrowerAnt()
# tunnel = [gamestate.places['tunnel_0_{0}'.format(i)] for i in range(9)]
# tunnel[1].add_insect(back_ant)
# tunnel[7].add_insect(front_ant)
# tunnel[4].ant is None

# back_ant.damage 

# front_ant.damage



from ants import *
beehive, layout = Hive(AssaultPlan()),dry_layout
dimensions = (1, 9)
gamestate = GameState(None, beehive, ant_types(), layout, dimensions)
laser = LaserAnt()
ant = HarvesterAnt(2)
bee1 = Bee(2)
bee2 = Bee(2)
bee3 = Bee(2)
bee4 = Bee(2)
gamestate.places["tunnel_0_0"].add_insect(laser)
gamestate.places["tunnel_0_0"].add_insect(bee4)
gamestate.places["tunnel_0_3"].add_insect(bee1)
gamestate.places["tunnel_0_3"].add_insect(bee2)
gamestate.places["tunnel_0_4"].add_insect(ant)
gamestate.places["tunnel_0_5"].add_insect(bee3)
laser.action(gamestate)

