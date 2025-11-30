1. (01.03, Understand)  
What does the following code print?

```python
print("Hello", "World!")
```

a. HelloWorld!
*b. Hello World!
c. ("Hello", "World!")
d. Hello, World!


2. (01.03, Apply)  
Consider the following string containing an escape sequence. What is the exact output when the code runs?

```python
print("Line1\nLine2")
```

a. 
```plaintext
Line1 Line2
```
b. 
```plaintext
Line1\nLine2
```
c. 
```plaintext
Line1\n Line2
```
*d.
```plaintext
Line1
Line2
```


3. (01.03, Remember)  
Which of the following correctly converts the string variable `age_str` into an integer value?

*a.
```python
age = int(age_str)
```
b. 
```python
age = integer(age_str)
```
c. 
```python
age = age_str.toInt()
```
d. 
```python
age = parseInt(age_str)
```


4. (02.01, Apply)  
Examine the following code fragment, which updates the value stored in `x`:

```python
x = 4
x *= 3
x -= 5
```

After this code executes, what is the final value of `x`?

*a. 7
b. 12
c. -1
d. 5


5. (02.02, Understand)  
Which of the following is a valid Python variable name according to standard naming rules?

*a. `first_value`
b. `2ndValue`
c. `total-cost`
d. `class`


6. (02.03, Apply)  
Consider the following code that assigns and modifies two variables:

```python
a = b = 0
b += 1
```

What is the output of the following lines?

```python
print(id(a) == id(b))
print(f"a={a} b={b}")
```

a. 
```python
True
a=0 b=1
```
*b.
```python
False
a=0 b=1
```
c. 
```python
True
a=1 b=1
```
d. 
```python
False
a=1 b=1
```


7. (02.04, Apply) 
What is the output of the following code?

```python
x = 2/3
print(f"{x:.2f}")
```

a. 0.66
*b. 0.67
c. 0.66666667
d. 0.65


8. (02.05, Understand) 
What is the value of `2 + 3 * 2 ** 2`?

a. 20
b. 16
*c. 14
d. 10


9. (02.06, Apply) 
What is the result of

```python
n = 5
n *= 2
n /= 4
```

n = ?

*a. 2.5
b. 2
c. 10
d. 3


10. (02.07, Apply) 

For `minutes = 134`, what is the output of

```python
hours = minutes // 60
mins = minutes % 60
print(hours, mins)
```

*a. 2 14
b. 2 74
c. 14 2
d. 14 74


11. (02.07, Analyze) 
For `num = 987`, what is `(num // 10) % 10`?

a. 9
*b. 8
c. 7
d. 98


12. (02.08, Remember) 

How do you access `sqrt` after `import math`:

a. `sqrt(9)`
*b. `math.sqrt(9)`
c. `import sqrt`
d. `from sqrt import math`


13. (02.09, Apply) 
What is the output of the following code?

```python
import math
print(math.ceil(3.14))
```

a. 3
*b. 4
c. 3.1
d. 3.14


14. (02.10, Apply) 

Which gives a valid 1–6 die roll (inclusive)?

a. `random.randrange(1,6)`
*b. `random.randint(1,6)`
c. `random.random(6)`
d. `random.choice(1,6)`


15. (02.11, Understand) 
What does `print("C:\\Temp\\file.txt")` display?

*a. `C:\\Temp\\file.txt`
b. `C:\Temp\file.txt`
c. `C:Tempfile.txt`
d. Syntax error


16. (02.12, Analyze) 

Which violates PEP 8 naming conventions?

a. `total_cost = price * qty`
b. `def compute_total():`
*c. `Result = 0`
d. `return total_cost`


17. (03.01, Apply) 

If `s = "Aloha"`, `s[-2]` is?

a. `A`
b. `o`
*c. `h`
d. `a`


18. (03.02, Apply) 
What is the output of `f"{1234567:,}"`?

*a. `1,234,567`
b. `1234,567`
c. `1.234.567`
d. `1234567.0`


19. (03.03, Analyze) 

What are the final values of `nums` and `x`?

```python
nums = [1, 2, 3]
nums.remove(2)
x = nums.pop()
```

*a. `[1, 3]`, `3`
b. `[1, 2]`, `3`
c. `[1, 3]`, `2`
d. `[2, 3]`, `3`


20. (03.04, Understand) 
For `t = (1, 2, 3)`, which is true?

a. `t[1] = 5` works
b. `len(t)` is 2
*c. `t[0]` is 1
d. Tuples are mutable


21. (03.05, Apply) 
If `a = {1,2,3}` and `b = {3,4}`, what is `a.intersection(b)`?

a. `{1,2,3,4}`
b. `{1,2}`
*c. `{3}`
d. `{4}`


22. (03.06, Apply) 

What is the final value of `d`?

```python
d = {"a": 1}
d["b"] = 2
d["a"] = 5
```

a. `{"a": 1, "b": 2}`
*b. `{"a": 5, "b": 2}`
c. `{"b": 2}`
d. `{"a": 5}`


23. (03.09, Analyze) 
What is the output of

```python
pi = 3.9
print(int(pi), float(int(pi)))
```

*a. `3 3.0`
b. `4 4.0`
c. `3 3.9`
d. `3.9 3.9`


24. (04.02, Apply) 
For `x = 10`, which prints `not five`?

a. 
```python
if x == 5:
    print("not five")
```

*b.
```python
if x != 5: 
    print("not five")
```

c. 
```python
if x = 5:
    print("not five")
```

d. 
```python
if x <> 5:
    print("not five")
```


25. (04.04, Apply) 

With `t = 68`, what does the following code print?

```python
if t < 32:
  print("freezing")
elif t < 72:
  print("cool")
else:
  print("warm")
```

a. `freezing`
*b. `cool`
c. `warm`
d. nothing


26. (04.05, Analyze) 

What is the result of the following code?

```python
x, y = 5, 10
if x < 10 and y > 20:
  print("yes")
else:
  print("no")
```

a. `yes`
*b. `no`
c. Error
d. Nothing


27. (04.06, Analyze) 

For `rating = 3.7`, what is the output of the following code?

```python
if (0 <= rating < 2) or (3.5 <= rating <= 5):
  print("valid band")
else:
  print("invalid")
```

*a. `valid band`
b. `invalid`
c. Error
d. Nothing


28. (04.07, Apply) 
With `num = -3` in following standard nested-if sign test, what prints?

```python
if num > 0:
  print("positive")
else:
  if num < 0:
    print("negative")
  else:
    print("zero")
```

a. `positive`
*b. `negative`
c. `zero`
d. `none`


29. (04.09, Apply) 

Let `name = "kai"`. Which is `True`?

a. `"z" in name`
b. `"ai" not in name`
*c. `"k" in name`
d. `"K" in name`


30. (04.10, Analyze) 
What is the value of `3 + 4 * 2 ** 2`?

a. 11
*b. 19
c. 35
d. 28


31. (04.12, Apply) 

For `age = 17`, what is the value of `status`?

```python
status = "adult" if age >= 18 else "minor"
```

a. `adult`
*b. `minor`
c. `True`
d. Error


32. (05.02, Apply) 
How many times does `print(i)` execute?

```python
i = 0
while i < 3:
  print(i)
  i += 1
```

a. 2
*b. 3
c. 4
d. Infinite


33. (05.04, Apply) 
What is the last value printed?

```python
n = 3
while n > 0:
  print(n)
  n -= 1
```

a. 3
b. 2
*c. 1
d. 0


34. (05.05, Understand) 
What does this print?

```python
for k in {"a": 1, "b": 2}:
  print(k)
```

*a. `a` then `b`
b. `1` then `2`
c. `("a", 1)` then `("b", 2)`
d. Random numbers


35. (05.06, Apply) 
What is `list(range(5, 0, -2))`?

a. `[5, 4, 3, 2, 1, 0]`
*b. `[5, 3, 1]`
c. `[5, 2]`
d. `[]`


36. (05.08, Analyze) 
How many times does `count += 1` execute?

```python
count = 0
for i in range(2):
  for j in range(3):
    count += 1
```

a. 3
b. 5
*c. 6
d. 2


37. (05.10, Apply) 

What prints?

```python
for n in range(5):
  if n == 3:
    break
  if n % 2 == 0:
    continue
  print(n)
```

a. `0 1 2`
b. `1 3`
*c. `1`
d. `1 2`


38. (05.11, Analyze) 

What is the output?

```python
for n in [1, 2]:
  if n == 3:
    break
  print(n)
else:
  print("done")
```

a. `1 2`
*b. `1 2 done`
c. `done`
d. `1 done`


39. (05.12, Apply) 
What prints?

```python
items = ["a", "b"]
for i, v in enumerate(items):
  print(i, v)
```

a. `1 a` / `2 b`
*b. `0 a` / `1 b`
c. `a b`
d. Error


40. (05.08, Integrate) 
What is the final value of `total`?

```python
total = 0
for i in range(1, 3):
  for j in range(2):
    total += i + j
```

a. 6
*b. 8
c. 10
d. 12


41. (06.01, Apply) 
What prints?

```python
def add(x, y):
  return x + y

print(add(2, 3) * 2)
```

*a. 10
b. 7
c. 5
d. `add(2,3) * 2`


42. (06.05, Apply) 
What is the output?

```python
def triple(n):
  return n * 3

print(triple(4) + triple(2))
```

a. 12
*b. 18
c. 24
d. 30


43. (06.06, Understand) 
The `pass` statement in a function does what?

a. Exits the function
b. Throws an error
*c. Acts as a placeholder that does nothing
d. Returns `None` immediately


44. (06.12, Analyze) 

Given the following code, what is the final value of `orig` and `new`?

```python
def safe_append(xs, val):
  ys = xs[:]
  ys.append(val)
  return ys

orig = [1, 2]
new = safe_append(orig, 3)
```

a. `[1, 2, 3]` / `[1, 2, 3]`
*b. `[1, 2]` / `[1, 2, 3]`
c. `[1, 2, 3]` / `[1, 2]`
d. `[1, 2]` / `[1, 2]`


45. (06.13, Apply) 
What is the output of the following code?

```python
def power(x, y=2):
  return x ** y

print(power(3), power(2, 3))
```

a. `6 8`
*b. `9 8`
c. `9 6`
d. `8 9`


46. (06.14, Apply) 

What is `add_all(1, 2, 3)` given

```python
def add_all(*args):
  return sum(args)
```

a. `(1, 2, 3)`
*b. `6`
c. Error
d. `1`


47. (06.15, Apply) 

What prints?

```python
def stats(xs):
  return (min(xs), max(xs))

low, high = stats([3, 1, 4])
print(low, high)
```

a. `3 4`
*b. `1 4`
c. `(1, 4)`
d. `1`


48. (06.16, Analyze) 
What does `help(greet)` show?

```python
def greet(name):
  """Print a friendly greeting."""
  print(f"Hello, {name}")
```

a. Only the source code
*b. The function signature and the docstring
c. Nothing
d. An error


49. (06.01, Integrate) 
What prints?

```python
def square(n):
  return n * n

def hyp(a, b):
  return (square(a) + square(b)) ** 0.5

print(round(hyp(3, 4)))
```

*a. 5
b. 25
c. 7
d. 4


50. (07.01, Apply) 
What is the result of `"abcdef"[1:5:2]`?

a. `ace`
*b. `bd`
c. `bdf`
d. `bde`


51. (07.02, Apply) 
What is the output of `f"{'hi':*<6}"`?

*a. `hi****`
b. `**hi**`
c. `hi****` (with space)
d. `*hi***`


52. (07.03, Analyze) 
What prints?

```python
print("banana".replace("a", "o", 2))
```

*a. `bonona`
b. `boonoo`
c. `bononaa`
d. `banana`


53. (07.04, Apply) 
What is the result of

```python
",".join("ab c".split())
```

*a. `ab,c`
b. `a,b,c`
c. `ab c`
d. `ab c` (unchanged)


54. (07.03, Analyze) 
Which is `True`?

a. `"abc" == "ABC"`
*b. `"abc" < "abd"`
c. `"a" not in "banana"`
d. `"ABC".islower()`


55. (08.01, Apply) 
What is the final value of `a` after the following code is executed? 
```python
a = [1, 2, 3]
b = a
b[0] = 99
```

a. `[1, 2, 3]`
*b. `[99, 2, 3]`
c. `[1, 99, 3]`
d. Error


56. (08.06, Apply) 
What is the output of

```python
xs = [0, 1, 2, 3, 4]
print(xs[0:5:2])
```

*a. `[0, 2, 4]`
b. `[1, 3]`
c. `[0, 1, 2, 3, 4]`
d. `[2, 4]`


57. (08.08, Analyze) 
`evens_sq` equals what?

```python
xs = [1, 2, 3, 4]
evens_sq = [x * x for x in xs if x % 2 == 0]
```

a. `[1, 4, 9, 16]`
b. `[1, 9]`
*c. `[4, 16]`
d. `[2, 4]`


58. (08.09, Analyze) 
What prints?

```python
words = ["Banana", "apple"]
print(sorted(words, key=str.lower))
print(words)
```

a. 
```python
['apple', 'Banana']
['apple', 'Banana']
```

*b.
```python 
['apple', 'Banana']
['Banana', 'apple']
```

c. 
```python
['Banana', 'apple']
['Banana', 'apple']
```
d. Error


59. (08.14, Apply) 
What is the output?

```python
d = {"a": 1, "b": 2}
for k, v in d.items():
  print(k, v)
```

*a.
```python
a 1
b 2
```

b. 
```python
1 a
2 b
```

c. 
```python
("a", 1, "b", 2)
```
d. Error


60. (12.01, Analyze) What is the best way to read all lines from a text file safely?

a. 
```python
f = open("data.txt")
lines = f.readlines()
```

*b.
```python
with open("data.txt", "r", encoding="utf-8") as f:
  lines = f.readlines()
```

c. 
```python
open("data.txt", "r").close()
```

d. 
```python
lines = open("data.txt", "w").readlines()
``` 


61. (12.02, Apply) 
How do you open a file to append text?

a. `open("log.txt", "w")`
b. `open("log.txt", "r")`
*c. `open("log.txt", "a")`
d. `open("log.txt")`


---

End of exam.
