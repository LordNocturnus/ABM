## ------------------------------------------------------------------------------------- ##
## File created to automatically generate the test cases for all maps, using all solvers ##
## ------------------------------------------------------------------------------------- ##
## Run with precaution !!! ##
## ----------------------- ##

imports = 'tests/test_map/setup.config'
test_class = 'tests/test_map/class.config'

with open(imports, 'r') as reader:
    imports_content = reader.read()

with open(test_class, 'r') as reader:
    test_class_content = reader.read()

with open('tests/test_map/test_single.py', 'w') as file:

    file.write(imports_content)

    for i in range(1, 51):
        file.write(test_class_content % (i, i, i, i))
    
    file.write("\n\n#### ---- End of tests ---- ####")