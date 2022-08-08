# PobreLang
## Overview
**PobreLang** is a programming language that lets you work
more slowly and inefficiently.

Have you ever thought while programming
> "Man, I wish this were slower,
its too much for me!"

? Then PobreLang is the language for you.
PobreLang gives you all the slowness you want!

In PobreLang, you **can't** just create variables.
You must **pay** for them!
In order to pay for them, you must **work**, which **takes time**.
If you work too much, your program will be **very slow**.
On the other hand, if you work too little,
you won't be able to afford all the variables you need.
Your payment is not very high and
there's nothing you can do to increase it.
Therefore, you must be smart and learn to **manage your money**.

## Hello world!
```
scream Hello world!
```

## Complete guide
This is a full guide for PobreLang.
It will teach you how to completely master it.
There are also some interesting tips in the end.

### Variables
Variables store values in them.
They can have two types: `item` and `tag`.
Items store numbers in them (both integer and floating point numbers),
while tags store strings of characters.

To create a variable, use the chosen type-keyword
followed by the name and the value.
**Note:** variable names and values should not have spaces in them!
If you want to store a string with spaces, you need more variables.
```
item myitem 3.5
tag mytag hello
```

The code shown above will throw an error.
This happens because all the variable names must start with `PobreLang/`.
Let's refactor the code to include them.
```
item PobreLang/myitem 3.5
tag PobreLang/mytag hello
```

It gives us two variables storing 3.5 and "hello", respectively.
Except that is still has an error.
In PobreLang, we start with no money, so we can't afford these variables.
We must work before creating them to get some money.
I'll show you how in the next section.

### Working
In order to work in PobreLang, the keyword `work` is used,
followed by the amount of working hours.
```
work 10
```

Usually, you don't want your program to stop its execution for hours.
Luckily, we can pass floating point numbers to this keyword.
Let's try working for a few seconds...
We can divide the number of seconds by 60 twice, to convert it to hours.
```
work 10/60/60
```

The code above will pause the execution for ten seconds and
give us some money.

**Note:** when using these expressions,
don't put spaces between the operations.
PobreLang uses spaces to tell expressions apart.

### Screaming
After a lot of work, you might want to scream a bit.
The `scream` keyword is used to print messages in PobreLang.

It can take an indefinite number of arguments,
so you can pass multiple strings or variables at once.

The scream keyword is used for the iconic Hello World program!
```
scream Hello world!
```

You can also pass variables to it.
```
work 10/60/60

tag PobreLang/hello Hello
tag PobreLang/world world!

scream PobreLang/hello PobreLang/world
```

The program above also outputs a Hello World message.

Mathematical expressions can be passed,
though they will not be evaluated, as `scream` treats them as tags.
```
scream 1+1
```

The program above will not print `2`, but `1+1` instead.

### User input
To read user input, two keywords exist.
One of them, `listen` is used to read tags (strings).
The other, `antidisestablishmentarianism`,
is used to read items (numbers).

A variable must be passed as a parameter to store the values in.
```
work 10/60/60

item PobreLang/number_input 0
tag PobreLang/string_input abc

antidisestablishmentarianism PobreLang/number_input
listen PobreLang/string_input
```

### Burning
Burning a variable is the same as deleting it.
You can delete a variable when you don't need it,
but you won't get your money back.

In order to burn a variable you don't need anymore,
use the `burn` keyword.

```
work 10/60/60

item PobreLang/useless

burn PobreLang/useless
```

### Notes
Notes allow you no take notes of things.
They are not executed and serve just for the purpose of taking notes.
To take a note, use the `note` keyword.
```
note that this will not be executed
```

### Stamps and sprinting
Stamps are like checkpoints you can put
in your code to return to there later.
To create a stamp, use the `stamp` keyword followed by its name.
```
note that this is a stamp
stamp PobreLang/main
	scream Hello world!
```

Stamps are not useful by themselves.
We need a way to return to them.
To return to a stamp, use the `sprint` keyword.
```
note that this is a stamp
stamp PobreLang/main
	scream Hello world!

	note that this will make us return to the stamp
	sprint PobreLang/main
```

The code above will create an endless loop.
This happens because we are constantly going back to
the start of the stamp.

### If-statements
If-statements evaluate conditions.
They are useful to get us back from infinite loops, for example.

For an if-statement to work, we must give it an expression to evaluate
and a stamp to sprint to in case the condition evaluates as true.
```
note that this is a stamp
stamp PobreLang/main
	scream Hello world!

	note that this condition is false, so we won't return
	if 1>3 PobreLang/main
```

What makes them really useful is
when you use variables in the expressions.
```
note that this is a stamp
stamp PobreLang/main
	scream Hello world!

	work 10/60/60

	item PobreLang/continue 0

	note let the user choose if we continue in the loop
	antidisestablishmentarianism PobreLang/continue

	note that this condition is false, so we won't return
	if PobreLang/continue!=0 PobreLang/main
```

### Tips & tricks
#### Saving on the working hours
If you want to save some working time, try *reassigning* your variables,
instead of creating new ones.
This way, you won't be charged extra.
```
work 10/60/60

item PobreLang/var 7

note that I don't want to work anymore

note recreating the variable as a tag
tag PobreLang/var hello
```
