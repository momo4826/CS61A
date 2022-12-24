from hw06 import *
# mint = Mint()
# mint.year
# dime = mint.create(Dime)
# dime.year
# Mint.present_year = 2102  # Time passes
# nickel = mint.create(Nickel)
# nickel.year     # The mint has not updated its stamp yet
# nickel.worth()  # 5 cents + (80 - 50 years)
# mint.update()   # The mint's year is updated to 2102
# Mint.present_year = 2177     # More time passes
# mint.create(Dime).worth()    # 10 cents + (75 - 50 years)
# Mint().create(Dime).worth()  # A new mint has the current year
# dime.worth()     # 10 cents + (155 - 50 years)
# Dime.cents = 20  # Upgrade all dimes!
# print(dime.year)
# print(Mint.present_year)
# dime.worth()

t3 = Tree(6, [Tree(2, [Tree(4), Tree(1)]), Tree(7, [Tree(7), Tree(8)])])
print(is_bst(t3))
print("----------")

