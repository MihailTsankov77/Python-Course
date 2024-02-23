def no_it_isnt(arr):
    if type(arr) == list:
        no_list = list(map(lambda x: no_it_isnt(x), arr))
        no_list.reverse()
        return no_list
    
    if type(arr) in (int, float):
        return -arr
    
    if type(arr) == bool:
        return not arr
    
    if type(arr) == str:
        return arr[::-1]
