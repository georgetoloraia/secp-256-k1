

# First, let's open the file to understand its structure and content before processing it.
file_path = 'all_updated.txt'
with open(file_path, 'r') as file:
    content = file.read()

# Displaying the first 500 characters to understand the file content and structure
print(content[:500])



# Splitting the content into lines and adding 1 to each number
lines = content.strip().split('\n')
updated_lines = [str(int(line) + 1) for line in lines]

# Joining the updated lines back into a single string
updated_content = '\n'.join(updated_lines)

# Saving the updated content to a new file
updated_file_path = 'all_updated.txt'
with open(updated_file_path, 'w') as file:
    file.write(updated_content)

updated_file_path
