class SupermarketCatalogue():
    prices = {
        "A" : 50, 
        "B" : 30, 
        "C" : 20,
        "D" : 15,
        "E" : 40,
        "F" : 10,
        "G" : 20,
        "H" : 10,
        "I" : 35,
        "J" : 60,
        "K" : 70,
        "L" : 90,
        "M" : 15,
        "N" : 40,
        "O" : 10,
        "P" : 50,
        "Q" : 30,
        "R" : 50,
        "S" : 20,
        "T" : 20,
        "U" : 40,
        "V" : 50,
        "W" : 20,
        "X" : 17,
        "Y" : 20,
        "Z" : 21
    }

    specialOffers = { # (qty,price,freebies)
        "A": [(5, 200, ()), (3,130, ())], # store offers in reverse i.e best value -> least value
        "B" : [(2,45, ())],
        "E" : [(2,80, ("B",1))],
        "F" : [(3,20, ())], # 'buy 2 get 1 free'
        "H" : [(10, 80, ()), (5, 45, ())],
        "K" : [(2, 120, ())],
        "N" : [(3, 120, ("M",1))],
        "P" : [(5, 200, ())],
        "Q" : [(3,80, ())],
        "R" : [(3,150, ("Q",1))],
        "U":  [(4, 120, ())],
        "V" : [(3, 130, ()), (2,90, ())]
    }

    groupDiscounts = {
        "options" :[3, "S","T","X","Y","Z"], # options[0] from options[1..N]
        "price" : 45,
    }

    def getPrices(self):
        return self.prices
    
    def getSpecialOffers(self):
        return self.specialOffers
    
    def getGroupDiscounts(self):
        return self.groupDiscounts