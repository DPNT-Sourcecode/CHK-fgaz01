# from solutions.CHK.catalogue import SupermarketCatalogue
from catalogue import SupermarketCatalogue

class CheckoutSolution: 
    def __init__(self):
        self.catalogue = SupermarketCatalogue()
        self.prices = self.catalogue.getPrices()
        self.specialOffers = self.catalogue.getSpecialOffers()
        self.groupDiscounts = self.catalogue.getGroupDiscounts()

    def groupDiscountCalculator(self, itemsOrdered):
        bundleOptions = self.groupDiscounts["options"] # get eligible bundle items and number
        bundleSize = self.groupDiscounts["size"]
        bundlePrice = self.groupDiscounts["price"]

        totalBundleValue = 0
        bundleItems = []

        for item, qty in itemsOrdered.items():
            if item in bundleOptions:
                bundleItems += [(item, self.prices[item])] * qty # extract the bundle items and prices

        # if len(bundleItems) >= bundleSize:
        #     numBundles = len(bundleItems) // bundleSize
        #     totalBundleValue += bundlePrice * numBundles # claim bundles

        #     # customer-friendly rule: leftover items at normal price
        #     bundleItems.sort(key=lambda x: x[1], reverse=True)
        #     itemsInBundle = numBundles * bundleSize
        #     for item, price in bundleItems[itemsInBundle:]:
        #         totalBundleValue += price

        #     return totalBundleValue

        if len(bundleItems) >= bundleSize:
            numBundles = len(bundleItems) // bundleSize
            # FIX: We want discount, not total value
            totalBundleValue = 0

            # Sort high → low so most expensive go into the bundle
            bundleItems.sort(key=lambda x: x[1], reverse=True)

            # Compute how much we OVERPAID in subtotal
            normal_price_of_bundles = sum(price for _, price in bundleItems[:numBundles * bundleSize])

            # Correct discount = normal prices removed + bundlePrice added per bundle
            return bundlePrice * numBundles - normal_price_of_bundles

        return 0 # not enough items to form a bundle so no group discount applied
    

    def offerCalculator(self, item, qty, itemsOrdered):
        regularPrice = self.prices[item]
        offers = self.specialOffers.get(item,[])

        totalPrice = 0
        qtyRemaining = qty # claim offers greedily

        bought = [0,0] # [special,regular] record numbers bought at regular and special price (for freebies)

        for offer in offers:
            while qtyRemaining >= offer[0]: # claim offers while available
                totalPrice += offer[1]
                qtyRemaining -= offer[0]
                bought[0] += offer[0]

        if qtyRemaining > 0: # include any remaining items
            totalPrice += (qtyRemaining * regularPrice)
            bought[1] += qtyRemaining    

        return totalPrice, bought
    
    def freebieCalculator(self, itemsOrdered, allBuys):
        freebieValue = 0 # value to DEDUCT from the total price
        for item in itemsOrdered:
            for (qtyToClaim, price, freebies) in self.specialOffers.get(item,[]):
                if freebies != (): # check if any freebies
                    freeItem, freeQty = freebies

                    offersToClaim = itemsOrdered[item] // qtyToClaim 
                    freebiesAvailable = offersToClaim * freeQty # calculate max number of individual free items to claim
                    numsSpecial, numsRegular = allBuys.get(freeItem, (0,0))

                    # Freebies apply to regular-price first
                    freebiesApplied = min(numsRegular, freebiesAvailable)

                    remainingFreebies = freebiesAvailable - freebiesApplied

                    # THEN allow special-priced items, but special offers consume qtyToClaim items at discounted rate
                    if remainingFreebies > 0:
                        freebiesApplied += min(numsSpecial, remainingFreebies)

                    freebieValue += freebiesApplied * self.prices[freeItem]

                    # numsSpecial, numsRegular = allBuys.get(freeItem, (0,0))
                    # eligible_freebies = numsRegular
                    # freebiesApplied = 0

                    # if freebiesAvailable <= numsRegular: # purchased at regular price so just a simple deduction
                    #     freebiesApplied = min(eligible_freebies, freebiesAvailable)
                    # # elif (numsRegular > 0 or numsSpecial > 0): # some deal claimed in previous purchase
                    # #     freebiesApplied = min(numsRegular + numsSpecial, freebiesAvailable) # claim freebies

                    # freebieValue += freebiesApplied * self.prices[freeItem] 

        return freebieValue
    
    def priceCalculator(self, item, qty, itemsOrdered):
        groupDiscountOptions = self.groupDiscounts["options"]
        price = 0
        numsBought = 0
        if (qty < 1): # illegal input
            return -1

        if (item not in self.specialOffers): # no special offers, sell at regular price 
            return self.prices[item] * qty, [0, qty]
        elif (item in self.specialOffers): 
            price, numsBought = self.offerCalculator(item,qty,itemsOrdered)
    
        return price, numsBought
    
    def checkout(self, skus): # skus = unicode string
        if skus == "": # illegal input
            return 0
        itemsOrdered = {}
        for item in skus:
            if item not in self.prices:
                return -1
            itemsOrdered[item] = itemsOrdered.get(item, 0) + 1

        subTotal = 0
        allBuys = {} # record quantities of items bought at special and regular price
        for item, qty in itemsOrdered.items():
            val, bought = self.priceCalculator(item,qty,itemsOrdered)
            allBuys[item] = bought
            if val != -1:
                subTotal += val 
            else:
                return -1
            
        freeVal = self.freebieCalculator(itemsOrdered, allBuys) # calculate freebies separately
        groupDiscount = self.groupDiscountCalculator(itemsOrdered) # apply group discounts separately

        return subTotal - freeVal + groupDiscount # final checkout value

