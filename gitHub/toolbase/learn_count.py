import collections
duplicates = [(f.split("|")[-1]) for f in mc.ls(dag=1) ]
collect_dups = [(item, count) for item, count in collections.Counter(duplicates).items() if count >1]
if len(collect_dups)>0:
    for each in collect_dups:
        print each
else:
    print "no duplicate named objects present"

    

import collections
duplicates = [(f.split("|")[-1]) for f in mc.ls(dag=1) ]
collect_dups = [(item, count) for item, count in collections.Counter(duplicates).items() if count >1]
for index, each in enumerate(collect_dups):
    for item in range(1, each[-1]):
        try:
            mc.rename(mc.ls(each[0])[0], each[0]+'_'+str(index)+'_'+str(item))
        except:
            pass

import look_variator;look_variator.start()
