# # from solutions.CHK.catalogue import SupermarketCatalogue
# from catalogue import SupermarketCatalogue

# class CheckoutSolution: 
#     def __init__(self):
#         self.catalogue = SupermarketCatalogue()
#         self.prices = self.catalogue.getPrices()
#         self.specialOffers = self.catalogue.getSpecialOffers()
#         self.groupDiscounts = self.catalogue.getGroupDiscounts()

#     def groupDiscountCalculator(self, itemsOrdered):
#         bundleOptions = self.groupDiscounts["options"] # get eligible bundle items and number
#         bundleSize = self.groupDiscounts["size"]
#         bundlePrice = self.groupDiscounts["price"]

#         totalBundleValue = 0
#         bundleItems = []

#         for item, qty in itemsOrdered.items():
#             if item in bundleOptions:
#                 bundleItems += [(item, self.prices[item])] * qty # extract the bundle items and prices

#         if len(bundleItems) >= bundleSize:
#             numBundles = len(bundleItems) // bundleSize
#             totalBundleValue += bundlePrice * numBundles # claim bundles

#             # customer-friendly rule: leftover items at normal price
#             bundleItems.sort(key=lambda x: x[1], reverse=True)
#             itemsInBundle = numBundles * bundleSize
#             for item, price in bundleItems[itemsInBundle:]:
#                 totalBundleValue += price

#             return totalBundleValue

       
#         return 0 # not enough items to form a bundle so no group discount applied


#     # def groupDiscountCalculator(self, itemsOrdered):
#     #     bundleOptions = self.groupDiscounts["options"] # get eligible bundle items and number
#     #     bundleSize = self.groupDiscounts["size"]
#     #     bundlePrice = self.groupDiscounts["price"]

#     #     totalBundleValue = 0
#     #     bundleItems = []
        
#     #     for item, qty in itemsOrdered.items():
#     #         if item in bundleOptions:
#     #             bundleItems += [(item, self.prices[item])] * qty # extract the bundle items and prices
        
#     #     if len(bundleItems) >= bundleSize:
#     #         numBundles = len(bundleItems) // bundleSize
#     #         totalBundleValue += bundlePrice * numBundles # claim bundles

#     #         # favour the customer by selling the remaining cheapest items at regular price
#     #         bundleItems.sort(key = lambda x:x[1], reverse=True) # sort by price descending
#     #         itemsInBundle = numBundles * bundleSize
#     #         for item, price in bundleItems[itemsInBundle:]:
#     #             totalBundleValue += price 
#     #     else:
#     #         return 0
#     #         # for item,price in bundleItems:
#     #         #     totalBundleValue += price # sell at regular price

#     #     return totalBundleValue
    

#     def offerCalculator(self, item, qty, itemsOrdered):
#         regularPrice = self.prices[item]
#         offers = self.specialOffers.get(item,[])

#         totalPrice = 0
#         qtyRemaining = qty # claim offers greedily

#         bought = [0,0] # [special,regular] record numbers bought at regular and special price (for freebies)

#         for offer in offers:
#             while qtyRemaining >= offer[0]: # claim offers while available
#                 totalPrice += offer[1]
#                 qtyRemaining -= offer[0]
#                 bought[0] += offer[0]

#         if qtyRemaining > 0: # include any remaining items
#             totalPrice += (qtyRemaining * regularPrice)
#             bought[1] += qtyRemaining    

#         return totalPrice, bought
    
#     def freebieCalculator(self, itemsOrdered, allBuys):
#         freebieValue = 0 # value to DEDUCT from the total price
#         for item, offers in self.specialOffers.items():
#             for (qtyToClaim, price, freebies) in offers:
#                 if freebies != (): # check if any freebies
#                     freeItem, freeQty = freebies

#                     offersToClaim = itemsOrdered[item] // qtyToClaim 
#                     freebiesAvailable = offersToClaim * freeQty # calculate max number of individual free items to claim

#                     numsSpecial, numsRegular = allBuys.get(freeItem, (0,0))
#                     freebiesApplied = 0

#                     if freebiesAvailable <= numsRegular: # purchased at regular price so just a simple deduction
#                         freebiesApplied = min(numsRegular, freebiesAvailable)
#                     elif (numsRegular > 0 or numsSpecial > 0): # some deal claimed in previous purchase
#                         freebiesApplied = min(numsRegular + numsSpecial, freebiesAvailable) # claim freebies

#                     freebieValue += freebiesApplied * self.prices[freeItem] 

#         return freebieValue
    
#     def priceCalculator(self, item, qty, itemsOrdered):
#         groupDiscountOptions = self.groupDiscounts["options"]
#         price = 0
#         numsBought = 0
#         if (qty < 1): # illegal input
#             return -1
        
#         if item in groupDiscountOptions: # ignore group bundle items
#             return 0, [0, qty]

#         if item in self.specialOffers:
#             return self.offerCalculator(item, qty, itemsOrdered)

#         return self.prices[item] * qty, [0, qty]


#         # if (item not in self.specialOffers) and (item not in groupDiscountOptions): # no special offers, sell at regular price 
#         #     return self.prices[item] * qty, [0, qty]
#         # elif (item in self.specialOffers): 
#         #     price, numsBought = self.offerCalculator(item,qty,itemsOrdered)
    
#         # return price, numsBought
    
#     def checkout(self, skus): # skus = unicode string
#         if skus == "": # illegal input
#             return 0
#         itemsOrdered = {}
#         for item in skus:
#             if item not in self.prices:
#                 return -1
#             itemsOrdered[item] = itemsOrdered.get(item, 0) + 1

#         subTotal = 0
#         allBuys = {} # record quantities of items bought at special and regular price
#         for item, qty in itemsOrdered.items():
#             val, bought = self.priceCalculator(item,qty,itemsOrdered)
#             allBuys[item] = bought
#             if val != -1:
#                 subTotal += val 
#             else:
#                 return -1
            
#         freeVal = self.freebieCalculator(itemsOrdered, allBuys) # calculate freebies separately
#         groupDiscount = self.groupDiscountCalculator(itemsOrdered) # apply group discounts separately

#         return subTotal - freeVal + groupDiscount # final checkout value
from catalogue import SupermarketCatalogue

class CheckoutSolution: 
    def __init__(self):
        self.catalogue = SupermarketCatalogue()
        self.prices = self.catalogue.getPrices()
        self.specialOffers = self.catalogue.getSpecialOffers()
        self.groupDiscounts = self.catalogue.getGroupDiscounts()

    # -----------------------------------------------------------
    # GROUP DISCOUNT (STXYZ mix-and-match bundles)
    # -----------------------------------------------------------

    def groupDiscountCalculator(self, itemsOrdered):
        bundleItems = []
        bundleOptions = self.groupDiscounts["options"]   # eligible items for bundle
        bundleSize   = self.groupDiscounts["size"]       # number of items per bundle
        bundlePrice  = self.groupDiscounts["price"]      # bundle price

        # Extract all bundle-eligible items
        for item, qty in itemsOrdered.items():
            if item in bundleOptions:
                bundleItems += [(item, self.prices[item])] * qty

        if not bundleItems:
            return 0

        # Sort so that bundles consume the *most expensive* items first
        bundleItems.sort(key=lambda x: x[1], reverse=True)

        numBundles = len(bundleItems) // bundleSize
        leftover   = len(bundleItems) % bundleSize

        # Price the bundles
        total = numBundles * bundlePrice

        # Price leftover bundle items at REGULAR PRICE
        for item, price in bundleItems[numBundles * bundleSize:]:
            total += price

        return total

    # -----------------------------------------------------------
    # REGULAR SPECIAL OFFERS (e.g., A: 3 for 130)
    # -----------------------------------------------------------

    def offerCalculator(self, item, qty, itemsOrdered):
        regularPrice = self.prices[item]
        offers = self.specialOffers.get(item, [])

        totalPrice = 0
        qtyRemaining = qty
        bought = [0, 0]  # [special, regular]

        # claim offers greedily (highest-value offers first)
        for offerQty, offerPrice, freebies in offers:
            while qtyRemaining >= offerQty:
                totalPrice += offerPrice
                qtyRemaining -= offerQty
                bought[0] += offerQty   # bought under special price

        # leftover units at regular price
        if qtyRemaining > 0:
            totalPrice += qtyRemaining * regularPrice
            bought[1] += qtyRemaining

        return totalPrice, bought

    # -----------------------------------------------------------
    # FREEBIES (e.g., E gives free B)
    # -----------------------------------------------------------

    def freebieCalculator(self, itemsOrdered, allBuys):
        freebieValue = 0  # value to DEDUCT from total

        for item, offers in self.specialOffers.items():
            for (qtyToClaim, _, freebies) in offers:

                if freebies == ():  
                    continue         # this offer does NOT produce freebies

                freeItem, freeQty = freebies

                # How many times the offer is applied for this item
                offerApplications = itemsOrdered.get(item, 0) // qtyToClaim
                freebiesAvailable = offerApplications * freeQty

                # How many freeItems were bought at regular/special price
                specialCount, regularCount = allBuys.get(freeItem, (0, 0))

                if freebiesAvailable == 0:
                    continue

                # Freebies can apply to any purchased units of the free item
                totalPurchased = specialCount + regularCount
                freebiesApplied = min(freebiesAvailable, totalPurchased)

                # Deduct the value of freebies applied
                freebieValue += freebiesApplied * self.prices[freeItem]

        return freebieValue

    # -----------------------------------------------------------
    # PRICE CALCULATOR (per item before freebies)
    # -----------------------------------------------------------

    def priceCalculator(self, item, qty, itemsOrdered):
        groupOptions = self.groupDiscounts["options"]

        if qty < 1:
            return -1

        # Group bundle items are not individually priced here
        if item in groupOptions:
            return 0, [0, qty]

        # Items with special offers
        if item in self.specialOffers:
            return self.offerCalculator(item, qty, itemsOrdered)

        # Regular pricing
        return self.prices[item] * qty, [0, qty]

    # -----------------------------------------------------------
    # MAIN CHECKOUT
    # -----------------------------------------------------------

    def checkout(self, skus):
        if skus == "":
            return 0

        # Parse SKUs
        itemsOrdered = {}
        for item in skus:
            if item not in self.prices:
                return -1
            itemsOrdered[item] = itemsOrdered.get(item, 0) + 1

        subTotal = 0
        allBuys = {}  # record {item: [specialQty, regularQty]}

        # Price all items individually (except bundle items)
        for item, qty in itemsOrdered.items():
            price, bought = self.priceCalculator(item, qty, itemsOrdered)
            if price == -1:
                return -1
            allBuys[item] = bought
            subTotal += price

        # Apply freebies
        freeValue = self.freebieCalculator(itemsOrdered, allBuys)

        # Apply group bundles
        groupValue = self.groupDiscountCalculator(itemsOrdered)

        # Final price
        return subTotal - freeValue + groupValue








