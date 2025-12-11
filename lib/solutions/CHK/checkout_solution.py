from solutions.CHK.catalogue import SupermarketCatalogue


class CheckoutSolution: 
    catalogue = SupermarketCatalogue()
    prices = catalogue.getPrices()
    specialOffers = catalogue.getSpecialOffers()
    groupDiscounts = catalogue.getGroupDiscounts()

    # TODO - could replace itemsOrdered with allBuys (sum(allBuys) == itemsOrdered)
    def groupDiscountCalculator(self, itemsOrdered):
        bundleOptions = self.groupDiscounts["options"] # get eligible bundle items and number
        bundleNum = bundleOptions[0] 
        bundlePrice = self.groupDiscounts["price"]

        totalBundleValue = 0
        potentialBundle = []
        
        for item, qty in itemsOrdered.items():
            if item in bundleOptions:
                potentialBundle.extend(([item,self.prices[item]] for _ in range(qty))) # extract the bundle items and prices
        
        if len(potentialBundle) >= bundleNum:
            bundlesToClaim = len(potentialBundle) // bundleNum
            totalBundleValue += bundlePrice * bundlesToClaim # claim bundles

            # favour the customer by selling the remaining cheapest items at regular price
            potentialBundle.sort(key = lambda x:x[1], reverse=True) # sort by price descending
            itemsInBundle = bundlesToClaim * bundleNum
            for item, price in potentialBundle[itemsInBundle:]:
                totalBundleValue += price 
        else:
            for item,price in potentialBundle:
                totalBundleValue += price # sell at regular price

        return totalBundleValue
    


    def offerCalculator(self, item, qty, itemsOrdered):
        regularPrice = self.prices[item]
        offers = self.specialOffers[item]

        totalPrice = 0
        qtyRemaining = qty # claim offers greedily

        bought = [0,0] # record numbers bought at regular and special price (for freebies)

        for offer in offers:
            numOffer = 0
            if qty < offer[0]: # not enough bought to claim the offer # TODO - remove this
                continue
            elif qty == offer[0]: # quantity matches offer perfectly
                numOffer = 1
                totalPrice += offer[1] 
                qtyRemaining -= qty
                bought[0] = qty
            else: 
                if qtyRemaining > 0: # can claim at least one offer
                    numOffer = qtyRemaining // offer[0]
                    qtyRemaining -= (numOffer*offer[0]) 
                    totalPrice += (offer[1] * numOffer)
                    bought[0] += (offer[1] * numOffer)

        if qtyRemaining > 0: # include any remaining items
            totalPrice += (qtyRemaining * regularPrice)
            bought[1] = qtyRemaining    

        return totalPrice, bought
    
    def freebieCalculator(self, itemsOrdered, allBuys):
        freebieValue = 0 # value to DECUCT from the total price
        for item in itemsOrdered:
            for (qtyToClaim, price, freebies) in self.specialOffers.get(item,[]):
                if freebies != (): # check if any freebies
                    freeItem, freeQty = freebies

                    offersToClaim = itemsOrdered[item] // qtyToClaim 
                    freebiesAvailable = offersToClaim * freeQty # calculate max number of individual free items to claim

                    numsSpecial, numsRegular = allBuys.get(freeItem, (0,0))
                    freebiesApplied = 0
                    if numsSpecial == numsRegular == 0: # didn't order previously so no price change  # TODO - also remove this
                        # freebiesApplied = 0
                        continue
                    elif freebiesAvailable <= numsRegular: # purchased at regular price so just a simple deduction
                        freebiesApplied = min(numsRegular, freebiesAvailable)
                    else: # some deal claimed in previous purchase
                        numOrdered = itemsOrdered[freeItem]

                        spent, _ = self.offerCalculator(freeItem, numOrdered, itemsOrdered)
                        freebieValue += spent 
                        freebieValue -= self.prices[freeItem] * numOrdered # effectively reset price and recharge at regular price

                        freebiesApplied = min(numsRegular+numsSpecial, freebiesAvailable) # set number of freebies to claim freebies
                    
                    freebieValue += freebiesApplied * self.prices[freeItem] 

        return freebieValue
    
    def priceCalculator(self, item, qty, itemsOrdered):
        groupDiscountOptions = self.groupDiscounts["options"]
        price = 0
        numsBought = 0
        if (qty < 1): # illegal input
            return -1

        if (item not in self.specialOffers) and (item not in groupDiscountOptions): # no special offers, sell at regular price 
            return self.prices[item] * qty, [0, qty]
        elif (item in self.specialOffers): 
            price, numsBought = self.offerCalculator(item,qty,itemsOrdered)
    
        return price, numsBought
    
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

        groupDiscount = self.groupDiscountCalculator(itemsOrdered) # apply group discounts separately

        return int(totalCheckoutVal - freeVal + groupDiscount) # final cehcout value

