
class CheckoutSolution: 
    prices = {
        "A" : 50,
        "B" : 30,
        "C" : 20,
        "D" : 15,
        "E" : 40
    }

    specialOffers = { # (qty,price,freebies)
        "A": [(5, 200, ()), (3,130, ())], # store offers in reverse i.e best value -> least value
        "B" : [(2,45, ())],
        "C" : [(2,40, ("B",1))]
    }

    def offerCalculator(self, item, qty, itemsOrdered):
        regularPrice = self.prices[item]
        offers = self.specialOffers[item]

        # 1) evaluate the quantity against each offer to calculate best possible deal
        # 2) deduct the price of any freebies (if in the basket)
        totalPrice = 0
        qtyRemaining = qty # claim offers greedily
        for offer in offers:
            if qty < offer[0]: # not enough bought to claim the offer
                totalPrice += (regularPrice * qty)
                break
            elif qty == offer[0]: # quantity matches offer perfectly
                totalPrice += offer[1]
                break   
            else: 
                if qtyRemaining > 0: # can claim at least one offer
                    numOffer = qtyRemaining // offer[0]
                    qtyRemaining -= (numOffer*offer[0]) 
                    # price = (offer[1] * numOffer) + (remaining * regularPrice)
                    totalPrice += (offer[1] * numOffer)

        if qtyRemaining > 0: # include any remaining items
            totalPrice += (qtyRemaining * regularPrice)

        freebies = offer[2]
        if freebies != (): # some freebies
            if freebies[0] in itemsOrdered.keys():


    def priceCalculator(self, item, qty,itemsOrdered):
        if (qty < 1): # illegal input
            return -1

        if item not in self.specialOffers: # no special offers, sell at regular price 
            return self.prices[item] * qty
    
        return self.offerCalculator(item, qty, itemsOrdered)
    
    def checkout(self, skus): # skus = unicode string
        if skus == "": # illegal input
            return 0
        
        allItems = self.prices.keys()
        items = list(skus)  # parse input to get items and quantities
        itemsOrdered = {}

        for item in items:
            if item not in allItems:
                return -1
            if item in itemsOrdered:
                itemsOrdered[item] += 1
            else:
                itemsOrdered[item] = 1    

        totalCheckoutVal = 0
        for item, qty in itemsOrdered.items():
            val = self.priceCalculator(item,qty,itemsOrdered)
            if val != -1:
                totalCheckoutVal += val 
            else:
                return -1

        return int(totalCheckoutVal)

supermarket = CheckoutSolution()
print(supermarket.checkout(""))

