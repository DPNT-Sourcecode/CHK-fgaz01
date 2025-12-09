
class CheckoutSolution: 
    prices = {
        "A" : 50,
        "B" : 30,
        "C" : 20,
        "D" : 15
    }

    specialOffers = {
        "A": (3,130), # (qty,price)
        "B" : (2,45)
    }

    def offerCalculator(self, item, qty):
        regularPrice = self.prices[item]
        offer = self.specialOffers[item]

        if qty == offer[0]: # quantity matches offer perfectly
            return offer[1]
        elif qty < offer: # not enough bought to claim the offer
            return regularPrice * qty
        else: # can claim at least one offer
            numOffer = qty // offer[0]
            remaining = qty - (numOffer*offer[0])
            price = (offer[1] * numOffer) + (remaining * regularPrice)
            return price

    def priceCalculator(self, item, qty):
        if (item not in self.prices) or (qty < 1): # illegal input
            return -1

        if item not in self.specialOffers: # no special offers, sell at regular price 
            return self.prices[item] * qty
    
        return self.offerCalculator(item, qty)
    
    def checkout(self, skus): # skus = unicode string
        items = skus.split()  # parse input to get items and quantities
        itemsOrdered = {}
        for item in items:
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


