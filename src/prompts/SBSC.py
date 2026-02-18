SBSC_SYSTEM_PROMPT = """You are a math problem solver. Solve problems step-by-step, writing a small Python code snippet for each step.

Format for each step:
Step N: [Brief description of what this step does]
```python
[code for this step only]
```

After I execute your code, I'll provide the output. Then continue to the next step.

When you reach the final answer, write:
Step N: Final Answer
```python
print(f"The answer is {result}")
```
###END OF CODE

Important rules:
- Each step should do ONE thing (extract a value, perform one calculation, etc.)
- Use results from previous steps
- If the executed code snippet returns an error, use it to correct the current step's code snippet. DO NOT restart solving from Step 1.
- Use meaningful variable names and include comments."""


SBSC_FEW_SHOT = """Example 1:
Q: There are 15 trees in the grove. Grove workers will plant trees in the grove today. After they are done, there will be 21 trees. How many trees did the grove workers plant today?

Step 1: Identify the initial number of trees
```python
trees_initial = 15
print(f"Initial trees: {trees_initial}")
```
```output
Initial trees: 15
```

Step 2: Identify the final number of trees
```python
trees_after = 21
print(f"Trees after planting: {trees_after}")
```
```output
Trees after planting: 21
```

Step 3: Calculate how many trees were planted
```python
trees_initial = 15
trees_after = 21
trees_planted = trees_after - trees_initial
print(f"Trees planted: {trees_planted}")
```
```output
Trees planted: 6
```

Step 4: Final Answer
```python
print(f"The answer is 6")
```
###END OF CODE

Example 2:
Q: If there are 3 cars in the parking lot and 2 more cars arrive, how many cars are in the parking lot?

Step 1: Identify initial cars and arriving cars
```python
cars_initial = 3
cars_arrived = 2
print(f"Initial: {cars_initial}, Arrived: {cars_arrived}")
```
```output
Initial: 3, Arrived: 2
```

Step 2: Calculate total cars
```python
cars_initial = 3
cars_arrived = 2
total_cars = cars_initial + cars_arrived
print(f"Total cars: {total_cars}")
```
```output
Total cars: 5
```

Step 3: Final Answer
```python
print(f"The answer is 5")
```
###END OF CODE

Example 3:
Q: Leah had 32 chocolates and her sister had 42. If they ate 35, how many pieces do they have left in total?

Step 1: Calculate total chocolates they had together
```python
leah_chocolates = 32
sister_chocolates = 42
total_chocolates = leah_chocolates + sister_chocolates
print(f"Total chocolates: {total_chocolates}")
```
```output
Total chocolates: 74
```

Step 2: Calculate chocolates left after eating
```python
total_chocolates = 74
chocolates_eaten = 35
chocolates_left = total_chocolates - chocolates_eaten
print(f"Chocolates left: {chocolates_left}")
```
```output
Chocolates left: 39
```

Step 3: Final Answer
```python
print(f"The answer is 39")
```
###END OF CODE

Example 4:
Q: Jason had 20 lollipops. He gave Denny some lollipops. Now Jason has 12 lollipops. How many lollipops did Jason give to Denny?

Step 1: Identify Jason's initial and final lollipop counts
```python
jason_initial = 20
jason_after = 12
print(f"Initial: {jason_initial}, After: {jason_after}")
```
```output
Initial: 20, After: 12
```

Step 2: Calculate lollipops given to Denny
```python
jason_initial = 20
jason_after = 12
given_to_denny = jason_initial - jason_after
print(f"Given to Denny: {given_to_denny}")
```
```output
Given to Denny: 8
```

Step 3: Final Answer
```python
print(f"The answer is 8")
```
###END OF CODE

Example 5:
Q: Shawn has five toys. For Christmas, he got two toys each from his mom and dad. How many toys does he have now?

Step 1: Identify initial toys
```python
toys_initial = 5
print(f"Initial toys: {toys_initial}")
```
```output
Initial toys: 5
```

Step 2: Calculate toys received from mom and dad
```python
toys_from_mom = 2
toys_from_dad = 2
total_received = toys_from_mom + toys_from_dad
print(f"Total received: {total_received}")
```
```output
Total received: 4
```

Step 3: Calculate total toys now
```python
toys_initial = 5
total_received = 4
total_toys = toys_initial + total_received
print(f"Total toys: {total_toys}")
```
```output
Total toys: 9
```

Step 4: Final Answer
```python
print(f"The answer is 9")
```
###END OF CODE

Example 6:
Q: There were nine computers in the server room. Five more computers were installed each day, from monday to thursday. How many computers are now in the server room?

Step 1: Identify initial computers and daily installation rate
```python
computers_initial = 9
computers_per_day = 5
print(f"Initial: {computers_initial}, Per day: {computers_per_day}")
```
```output
Initial: 9, Per day: 5
```

Step 2: Calculate number of days (Monday to Thursday)
```python
# Monday, Tuesday, Wednesday, Thursday = 4 days
num_days = 4
print(f"Number of days: {num_days}")
```
```output
Number of days: 4
```

Step 3: Calculate total computers added
```python
computers_per_day = 5
num_days = 4
computers_added = computers_per_day * num_days
print(f"Computers added: {computers_added}")
```
```output
Computers added: 20
```

Step 4: Calculate total computers now
```python
computers_initial = 9
computers_added = 20
computers_total = computers_initial + computers_added
print(f"Total computers: {computers_total}")
```
```output
Total computers: 29
```

Step 5: Final Answer
```python
print(f"The answer is 29")
```
###END OF CODE

Example 7:
Q: Michael had 58 golf balls. On tuesday, he lost 23 golf balls. On wednesday, he lost 2 more. How many golf balls did he have at the end of wednesday?

Step 1: Identify initial golf balls
```python
golf_balls_initial = 58
print(f"Initial golf balls: {golf_balls_initial}")
```
```output
Initial golf balls: 58
```

Step 2: Calculate golf balls after Tuesday's loss
```python
golf_balls_initial = 58
lost_tuesday = 23
after_tuesday = golf_balls_initial - lost_tuesday
print(f"After Tuesday: {after_tuesday}")
```
```output
After Tuesday: 35
```

Step 3: Calculate golf balls after Wednesday's loss
```python
after_tuesday = 35
lost_wednesday = 2
after_wednesday = after_tuesday - lost_wednesday
print(f"After Wednesday: {after_wednesday}")
```
```output
After Wednesday: 33
```

Step 4: Final Answer
```python
print(f"The answer is 33")
```
###END OF CODE

Example 8:
Q: Olivia has $23. She bought five bagels for $3 each. How much money does she have left?

Step 1: Identify initial money and bagel details
```python
money_initial = 23
num_bagels = 5
price_per_bagel = 3
print(f"Initial: ${money_initial}, Bagels: {num_bagels}, Price: ${price_per_bagel}")
```
```output
Initial: $23, Bagels: 5, Price: $3
```

Step 2: Calculate total spent on bagels
```python
num_bagels = 5
price_per_bagel = 3
money_spent = num_bagels * price_per_bagel
print(f"Money spent: ${money_spent}")
```
```output
Money spent: $15
```

Step 3: Calculate money left
```python
money_initial = 23
money_spent = 15
money_left = money_initial - money_spent
print(f"Money left: ${money_left}")
```
```output
Money left: $8
```

Step 4: Final Answer
```python
print(f"The answer is 8")
```
###END OF CODE

Now solve this problem step-by-step:
Q: """


def build_sbsc_prompt(question: str) -> tuple[str, str]:
    """Returns (system_prompt, user_prompt) for SBSC."""
    user_prompt = SBSC_FEW_SHOT + question
    return SBSC_SYSTEM_PROMPT, user_prompt