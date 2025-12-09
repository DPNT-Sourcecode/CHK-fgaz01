
class CheckoutSolution: 
    prices = {
        "A" : 50,
        "B" : 30,
        "C" : 20,
        "D" : 15
    }

    specialOffers = {
        "A": (3,130),
        "B" : (2,45)
    }

    def offerCalculator(self, item, qty):
        continue


    def priceCalculator(self, item, qty):
        if item not in prices: # illegal input
            return -1

        if item not in specialOffers: # no special offers, regular price calculation
            return prices[item] * qty
    
        return offerCalculator(item, qty)
    
    def checkout(self, skus):# skus = unicode string
        totalCheckoutVal = 0

        # parse input to get items and quantities
        # store in a list (or map)

        items = []
        for item, qty in items:
            val = priceCalculator(item,qty)
            if val != -1:
                totalCheckoutVal += val 
            else:
                return -1


        return totalCheckoutVal

