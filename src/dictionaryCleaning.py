def extract_word_from_entry(entry):
    """
    Given a dictionary entry (a block of text), extract the word.
    Assumes that the first nonempty line contains the word.
    Returns None if the word:
    - contains any non-alphabetic characters
    """
    lines = [line.strip() for line in entry.splitlines() if line.strip()]
    if lines:
        tokens = lines[0].split()
        if tokens:
            word = tokens[0]
            
            # Only keep words that contain ONLY alphabetic characters
            if not word.isalpha():
                return None
                
            return word
    return None

def main():
    input_filename = "data/Oxford English Dictionary.txt"  # Your original dictionary file
    output_filename = "data/oxford_words.txt"                   # Output file with one word per line

    # Read the entire file content
    with open(input_filename, "r", encoding="utf-8") as infile:
        content = infile.read()

    # Split entries by double newline (adjust if your entries are separated differently)
    entries = content.split("\n\n")

    # Use a set to avoid duplicate words
    words = set()
    for entry in entries:
        word = extract_word_from_entry(entry)
        if word:
            words.add(word)

    # Write the unique words into the output file, sorted alphabetically
    with open(output_filename, "w", encoding="utf-8") as outfile:
        for word in sorted(words, key=str.lower):
            outfile.write(word + "\n")

if __name__ == "__main__":
    main()