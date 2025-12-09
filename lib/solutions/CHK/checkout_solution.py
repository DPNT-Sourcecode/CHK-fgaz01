
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

    def offerCalculator(self, item, qty):
        regularPrice = self.prices[item]
        offers = self.specialOffers[item]

        # 1) evaluate the quantity against each offer to calculate best possible deal
        # 2) deduct the price of any freebies (if in the basket)
        totalPrice = 0
        for offer in offers:
            if qty < offer[0]: # not enough bought to claim the offer
                totalPrice += (regularPrice * qty)
            elif qty == offer[0]: # quantity matches offer perfectly
                totalPrice += offer[1]
          
            else: # can claim at least one offer
                numOffer = qty // offer[0]
                remaining = qty - (numOffer*offer[0])
                price = (offer[1] * numOffer) + (remaining * regularPrice)
                return price

    def priceCalculator(self, item, qty):
        if (qty < 1): # illegal input
            return -1

        if item not in self.specialOffers: # no special offers, sell at regular price 
            return self.prices[item] * qty
    
        return self.offerCalculator(item, qty)
    
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
            val = self.priceCalculator(item,qty)
            if val != -1:
                totalCheckoutVal += val 
            else:
                return -1

        return int(totalCheckoutVal)

supermarket = CheckoutSolution()
print(supermarket.checkout(""))
