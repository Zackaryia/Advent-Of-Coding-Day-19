"""
What I want my code to do:

Step one: Evaluate the steps and in reverse order (starting from the last rule to the 0th) 

Step two: generate a list of possible awnsers for each rule

Step three: Compare the list to the input given and check if message has been courupted.

Example of step one + step two

--Example rules--
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"
--End Example rules--

Reverse loop through rules and generate list of possible awnsers.

5: ["b"]
4: ["a"]
3: ["ab", "ba"]
2: ["aa", "ba"]
1: ["aaab", "aaba", "baab", "baba"]
0: ["aaaabb", "aaabab", "abaabb", "ababab"]

"""

debug_puzzle_input = False

if debug_puzzle_input:
	puzzle_input_text_file_name = "debugging_puzzle_input.txt"
else:
	puzzle_input_text_file_name = "puzzle_input.txt"
with open(puzzle_input_text_file_name, 'r') as puzzle_input:
	rules, test_cases = puzzle_input.read().split('\n\n')
	rules = rules.split('\n')
	test_cases = test_cases.split('\n')

print(reversed(rules))

def generate_constant_possible(rule):
	_, rule = rule.split(": ")
	rule = rule.replace('\"', "")
	return [rule]

def generate_list_if_combination(rule, dict_rules):
	rule = rule.strip()

	if ': ' in rule:
		_, rule = rule.split(': ')
	rule = rule.split(' ')

	current_list_of_outputs = ['']

	def additioner(current_list_of_outputs, rule_outputs): # Takes the list of outputs and expands it by the next constant in the list example if the current list of outputs is ["a", "babb"] and this rule can have the outputs of ['bb', 'bab'] then the ending list of outputs will become ['abb', 'babbbb', 'bab', 'babbbab'] so it just combines the output and rule to make a new output
		new_outputs = []

		if current_list_of_outputs == []:
			current_list_of_outputs = [''] #if there are no current outputs set rule outputs to [''] so it dosent skip next for loop

		for pre_output in current_list_of_outputs:
			for rule_output in rule_outputs:
				new_outputs.append(pre_output+rule_output)
		
		return new_outputs
	
	for sub_rule in rule:
		current_list_of_outputs = additioner(current_list_of_outputs, dict_rules[sub_rule])

	return current_list_of_outputs

def generate_list_if_or_used(rule, dict_rules):
	_, rule = rule.split(': ')
	rule = rule.split('|')

	current_list_of_outputs = []


	for sub_rule in rule:
		sub_rule.strip() #removes any trailing or starting white space

		current_list_of_outputs += generate_list_if_combination(sub_rule, dict_rules)

	return current_list_of_outputs


# MAIN LOOP FUNCTION TO GENERATE POSSIBLE MESSAGES
rule_dict = {}

new_rules_list = ['']*len(rules)
order_of_rules = []

while len(order_of_rules) < len(rules):
	for rule in rules:
		if rule.split(':')[0] in order_of_rules:
			pass
		elif '"' in rule:
			order_of_rules.append(rule.split(':')[0])
		else:
			a = rule.split(':')
			b = a[1]
			c = b.split(' ')
			y = [i for i in c if i.isdigit()]
			print(y)
			if set(y).issubset(set(order_of_rules)):
				order_of_rules.append(rule.split(':')[0])


for rule in rules:
	new_rules_list[order_of_rules.index(rule.split(':')[0])] = rule


for rule in new_rules_list:
	rule_number, _ = rule.split(": ")
	if rule.split(':')[0] == "0":
		print('ok')
	if '"' in rule:
		rule_dict[rule_number] = generate_constant_possible(rule)
	elif "|" in rule:
		rule_dict[rule_number] = generate_list_if_or_used(rule, rule_dict)
	else:
		rule_dict[rule_number] = generate_list_if_combination(rule, rule_dict)

awnser = 0
for test in test_cases:
	if test in rule_dict['0']:
		awnser += 1
	
print(awnser)

# Test cases for debugging

print(generate_constant_possible('492: "a"""'))
print(generate_list_if_combination('3: 4 5 6 7', {'4': ['b'], '5': ['ab', 'ba'], '6': ['bbaa', 'b'], '7': ['b']}))
print(generate_list_if_or_used('599: 1 2 3 | 2 3', {'1': ['b'], '2': ['ba', 'b'], '3': ['bbb', 'baaa', 'aba']}))

