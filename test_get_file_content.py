from functions.get_files_content import get_files_content

result = get_files_content("calculator", "lorem.txt")
print(result)
print(get_files_content("calculator", "main.py"))
print(get_files_content("calculator", "pkg/calculator.py"))
print(get_files_content("calculator", "/bin/cat"))
print(get_files_content("calculator", "pkg/does_not_exist.py"))
