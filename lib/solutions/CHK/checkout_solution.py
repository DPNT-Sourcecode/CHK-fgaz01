
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
        "E" : [(2,80, ("B",1))]
    }

    def offerCalculator(self, item, qty, itemsOrdered):
        regularPrice = self.prices[item]
        offers = self.specialOffers[item]

        totalPrice = 0
        qtyRemaining = qty # claim offers greedily
        freebiesToClaim = 0
        for offer in offers:
            numOffer = 0
            if qty < offer[0]: # not enough bought to claim the offer
                continue
            elif qty == offer[0]: # quantity matches offer perfectly
                numOffer = 1
                totalPrice += offer[1] 
                qtyRemaining -= qty
                # break   
            else: 
                if qtyRemaining > 0: # can claim at least one offer
                    numOffer = qtyRemaining // offer[0]
                    qtyRemaining -= (numOffer*offer[0]) 
                    # price = (offer[1] * numOffer) + (remaining * regularPrice)
                    totalPrice += (offer[1] * numOffer)
            # print(f"Potential freebies = {offer[2]}")
            if offer[2] != ():
                # print("Adding val for freebie")
                freebiesToClaim += (numOffer*offer[2][1]) # make proportional to  offers claimed
        
        if qtyRemaining > 0: # include any remaining items
            totalPrice += (qtyRemaining * regularPrice)

        # if offer[2] != ():
        #     freebieItem, freeQtyPerOffer = offer[2]
        #     totalFreebies = freebiesToClaim

        #     if freebieItem in itemsOrdered:
        #         qtyInBasket = itemsOrdered[freebieItem]
        #         originalCost = self.priceCalculator(freebieItem, qtyInBasket, itemsOrdered)
        #         regularCost = qtyInBasket * self.prices[freebieItem]
        #         freebiesClaimed = min(qtyInBasket, totalFreebies)

        #         totalPrice -= originalCost
        #         totalPrice += regularCost
        #         totalPrice -= freebiesClaimed * self.prices[freebieItem]
        
        return totalPrice
    
    def freebieCalculator(self, itemsOrdered):
        freebieValue = 0 # value to deduct from the total price!

    def priceCalculator(self, item, qty,itemsOrdered):
        if (qty < 1): # illegal input
            return -1

        if item not in self.specialOffers: # no special offers, sell at regular price 
            # print(f"Total for {item} = {self.prices[item] * qty}\n")
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
        allBuys = {} # record quantities of items bought at special and regular price
        for item, qty in itemsOrdered.items():
            val, bought = self.priceCalculator(item,qty,itemsOrdered)
            allBuys[item] = bought
            if val != -1:
                totalCheckoutVal += val 
            else:
                return -1
            
        freeVal = self.freebieCalculator(itemsOrdered, allBuys) # calculate freebies separately

        return int(totalCheckoutVal - freeVal)

supermarket = CheckoutSolution()
# print(supermarket.checkout("ABCDEABCDE")) # expected 280
# print(supermarket.checkout("CCADDEEBBA")) # expected 280
# print(supermarket.checkout("AAAAAEEBAAABB")) # expected 455
print(supermarket.checkout("ABCDECBAABCABBAAAEEAA")) # expected = 665
