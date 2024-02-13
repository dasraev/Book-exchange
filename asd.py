# def x():
#     def wrapper():
#         print('before print dilshod')
#         f()
#     return wrapper
#
# @x
# def f():
#     print('dilshod')
#
# print(f())
#


# def deco(f):
#     def wrapper(name):
#         print('before')
#         f(name)
#         print("after")
#     return wrapper

def f(*args):
    print(args,'Dilshod')

f('asd','wer')