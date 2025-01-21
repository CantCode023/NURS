from nurs import summarize, parse_text

text = parse_text('https://freedium.cfd/https://medium.com/pythoneers/18-insanely-useful-python-automation-scripts-i-use-everyday-b3aeb7671ce9')
print(summarize(text))