# ------------------------------------------------------------------------- 
# * This program - an extension of program sis1.c - simulates a simple (s,S) 
# * inventory system using Equilikely distributed demands. 
# * 
# * Name              : sis2.c  (Simple Inventory System, version 2)
# * Authors           : Steve Park & Dave Geyer 
# * Language          : ANSI C 
# * Latest Revision   : 8-28-97 
#   Translated by     : Philip Steele 
#   Language          : Python 3.3
#   Latest Revision   : 3/26/14
# * ------------------------------------------------------------------------- 
# */

#include <stdio.h>
#include "rng.h"
from rng import random, putSeed

MINIMUM = 20                        # 's' inventory policy parameter */
MAXIMUM = 80                        # 'S' inventory policy parameter */
STOP = 100                       # number of time intervals       */


class sumOf:
  setup = 0.0     #setup instances
  holding = 0.0   #inventory held (+)
  shortage = 0.0  #inventory held (-)
  order = 0.0     #orders
  demand = 0.0    #demands

def sqr(x):
  return((x)*(x))

def Equilikely(a,b):
  #===================================================================
  #Returns an equilikely distributed integer between a and b inclusive. 
  #NOTE: use a < b
  #===================================================================
  return (a + int((b - a + 1) * random()))


def GetDemand():              
#  ------------------------
#  * generate the next demand
#  * ------------------------
#  */                                           
  return (Equilikely(10, 50)) 


###########################Main Program###############################


index     = 0                      # time interval index     */
inventory = MAXIMUM                # current inventory level */
demand = -1                            # amount of demand        */
order = -1                             # amount of order         */
sum = sumOf()

putSeed(123456789)

while (index < STOP):
  index += 1
  if (inventory < MINIMUM):             # place an order */
    order         = MAXIMUM - inventory
    sum.setup += 1
    sum.order    += order
  else:                                   # no order       */
    order         = 0

  inventory      += order               # there is no delivery lag */
  demand          = GetDemand()
  sum.demand     += demand

  if (inventory > demand):
    sum.holding  += (inventory - 0.5 * demand)
  else:
    sum.holding  += sqr(inventory) / (2.0 * demand)
    sum.shortage += sqr(demand - inventory) / (2.0 * demand)
  
  inventory     -= demand
#EndWhile

if (inventory < MAXIMUM):               # force the final inventory to */
  order      = MAXIMUM - inventory      # match the initial inventory  */
  sum.setup += 1
  sum.order += order
  inventory += order

print("\nfor {0:1d} time intervals with an average demand of {1:6.2f}".format(index, (sum.demand/index)))
print("and policy parameters (s, S) = ({0}, {1})\n".format(MINIMUM, MAXIMUM))
print("   average order ............ = {0:6.2f}".format(sum.order / index))
print("   setup frequency .......... = {0:6.2f}".format(sum.setup / index))
print("   average holding level .... = {0:6.2f}".format(sum.holding / index))
print("   average shortage level ... = {0:6.2f}".format(sum.shortage / index))

#C output:
# for 100 time intervals with an average demand of  27.68
# and policy parameters (s, S) = (20, 80)

#    average order ............ =  27.68
#    setup frequency .......... =   0.36
#    average holding level .... =  44.81
#    average shortage level ... =   0.14