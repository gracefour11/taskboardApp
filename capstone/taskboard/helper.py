# Python code to get difference of two lists
# Using set()
def getDiffBtnLists(li1, li2):
    return list(set(li1) - set(li2)) + list(set(li2) - set(li1))

def printLogForTaskboard(name, type, deadline, members):
    print("Taskboard: " + name)
    print("New taskboard type: "+ type)
    print("New taskboard members list: " + members)
    if (deadline is not None):
        print("New taskboard deadline: " + deadline.strftime('%Y-%m-%d'))
