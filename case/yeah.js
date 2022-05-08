"yield&gt;&gt;&gt; mylist = [1, 2, 3]
&gt;&gt;&gt; for i in mylist:
...    print(i)
1
2
3
mylist&gt;&gt;&gt; mylist = [x*x for x in range(3)]
&gt;&gt;&gt; for i in mylist:
...    print(i)
0
1
4
for... in...listsstrings&gt;&gt;&gt; mygenerator = (x*x for x in range(3))
&gt;&gt;&gt; for i in mygenerator:
...    print(i)
0
1
4
()[]for i in mygeneratoryieldreturn&gt;&gt;&gt; def create_generator():
...    mylist = range(3)
...    for i in mylist:
...        yield i*i
...
&gt;&gt;&gt; mygenerator = create_generator() # create a generator
&gt;&gt;&gt; print(mygenerator) # mygenerator is an object!
&lt;generator object create_generator at 0xb7555c34&gt;
&gt;&gt;&gt; for i in mygenerator:
...     print(i)
0
1
4
yieldforforyieldyield""if/else""# Here you create the method of the node object that will return the generator
def _get_child_candidates(self, distance, min_dist, max_dist):

    # Here is the code that will be called each time you use the generator object:

    # If there is still a child of the node object on its left
    # AND if the distance is ok, return the next child
    if self._leftchild and distance - max_dist &lt; self._median:
        yield self._leftchild

    # If there is still a child of the node object on its right
    # AND if the distance is ok, return the next child
    if self._rightchild and distance + max_dist &gt;= self._median:
        yield self._rightchild

    # If the function arrives here, the generator will be considered empty
    # there is no more than two values: the left and the right children
# Create an empty list and a list with the current object reference
result, candidates = list(), [self]

# Loop on candidates (they contain only one element at the beginning)
while candidates:

    # Get the last candidate and remove it from the list
    node = candidates.pop()

    # Get the distance between obj and the candidate
    distance = node._get_dist(obj)

    # If distance is ok, then you can fill the result
    if distance &lt;= max_dist and distance &gt;= min_dist:
        result.extend(node._values)

    # Add the children of the candidate in the candidate's list
    # so the loop will keep running until it will have looked
    # at all the children of the children of the children, etc. of the candidate
    candidates.extend(node._get_child_candidates(distance, min_dist, max_dist))

return result
candidates.extend(node._get_child_candidates(distance, min_dist, max_dist))whileextend()&gt;&gt;&gt; a = [1, 2]
&gt;&gt;&gt; b = [3, 4]
&gt;&gt;&gt; a.extend(b)
&gt;&gt;&gt; print(a)
[1, 2, 3, 4]
&gt;&gt;&gt; class Bank(): # Let's create a bank, building ATMs
...    crisis = False
...    def create_atm(self):
...        while not self.crisis:
...            yield ""$100""
&gt;&gt;&gt; hsbc = Bank() # When everything's ok the ATM gives you as much as you want
&gt;&gt;&gt; corner_street_atm = hsbc.create_atm()
&gt;&gt;&gt; print(corner_street_atm.next())
$100
&gt;&gt;&gt; print(corner_street_atm.next())
$100
&gt;&gt;&gt; print([corner_street_atm.next() for cash in range(5)])
['$100', '$100', '$100', '$100', '$100']
&gt;&gt;&gt; hsbc.crisis = True # Crisis is coming, no more money!
&gt;&gt;&gt; print(corner_street_atm.next())
&lt;type 'exceptions.StopIteration'&gt;
&gt;&gt;&gt; wall_street_atm = hsbc.create_atm() # It's even true for new ATMs
&gt;&gt;&gt; print(wall_street_atm.next())
&lt;type 'exceptions.StopIteration'&gt;
&gt;&gt;&gt; hsbc.crisis = False # The trouble is, even post-crisis the ATM remains empty
&gt;&gt;&gt; print(corner_street_atm.next())
&lt;type 'exceptions.StopIteration'&gt;
&gt;&gt;&gt; brand_new_atm = hsbc.create_atm() # Build a new one to get back in business
&gt;&gt;&gt; for cash in brand_new_atm:
...    print cash
$100
$100
$100
$100
$100
$100
$100
$100
$100
...
print(corner_street_atm.__next__())print(next(corner_street_atm))Map / Zipimport itertools&gt;&gt;&gt; horses = [1, 2, 3, 4]
&gt;&gt;&gt; races = itertools.permutations(horses)
&gt;&gt;&gt; print(races)
&lt;itertools.permutations object at 0xb754f1dc&gt;
&gt;&gt;&gt; print(list(itertools.permutations(horses)))
[(1, 2, 3, 4),
 (1, 2, 4, 3),
 (1, 3, 2, 4),
 (1, 3, 4, 2),
 (1, 4, 2, 3),
 (1, 4, 3, 2),
 (2, 1, 3, 4),
 (2, 1, 4, 3),
 (2, 3, 1, 4),
 (2, 3, 4, 1),
 (2, 4, 1, 3),
 (2, 4, 3, 1),
 (3, 1, 2, 4),
 (3, 1, 4, 2),
 (3, 2, 1, 4),
 (3, 2, 4, 1),
 (3, 4, 1, 2),
 (3, 4, 2, 1),
 (4, 1, 2, 3),
 (4, 1, 3, 2),
 (4, 2, 1, 3),
 (4, 2, 3, 1),
 (4, 3, 1, 2),
 (4, 3, 2, 1)]
__iter__()__next__()foryieldyieldyieldyieldyield()[]()returnreturnyield"