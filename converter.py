INPUT_PATH = 'original.txt'
OUTPUT_PATH = 'Makefile'

input = open(INPUT_PATH, 'r')
output = open(OUTPUT_PATH, 'x')

assert input.mode == 'r'

input_lines = input.readlines()

# Map of parent->set of dependencies
dependency_map = dict()

# Set of all parent_features
parent_features = set()

# Set of all features
all_features = set()

current_parent = ""
for line in input_lines:
    
    # Clear any bolding
    line = line.replace('*', '')
    
    # Strip out any content after a parenthesis
    idx = line.find('(')
    if idx != -1:
        line = line[:idx]

    # If Feature Header
    if line.startswith("###"):
        feature = line[4:].lower().strip().replace(" ", "_")
        dependency_map[feature] = set()
        parent_features.add(feature)
        all_features.add(feature)
        current_parent = feature

    # If Dependency
    if line.startswith('- '):
        # If Essential
        if '[' not in line:
            dependency = line[2:].lower().strip().replace(" ", "_")
            all_features.add(dependency)
            dependency_map[current_parent].add(dependency)

# Write lines to add rules for all base features 
# for feature in all_features:
#     if feature not in parent_features:
#         print("\n\n" + feature + ':')
#         output.write("\n\n" + feature + ':')
input.close()


print("world_domination", end=": ")
output.write("world_domination: ")
for parent in parent_features:
    print(parent, end=" ")
    output.write(parent + " ")
output.write('\n')

for parent, dependencies in dependency_map.items():
    print(parent, end=": ")
    output.write(parent + ": ")
    
    for child in dependencies:
        # Omit base features
        if child in parent_features:
            print(child, end=' ')
            output.write(child + " ")
    print(" ")
    output.write('\n')

output.close()