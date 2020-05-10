# lambda-calculus-Interpreter
Interpreter for lambda calculus as described in https://en.wikipedia.org/wiki/Lambda_calculus

## Grammar :
<pre>
  <λexp>::= <var>
          |(λ <var> <λexp>)
          |(<λexp> <λexp>) 
</pre>

## Example:
<pre>
  >> (lambda x x)
      λx. x
  >> (lambda x y)
      λx. y
  >> x
     x
  >> 5
     5
  >> ((lambda x 5) 3)
     5
  >> (((lambda x (lambda y x)) 3) 5)
     3
</pre>
