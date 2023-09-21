import argparse
from scanner import Scanner

def compile(file):
  with open(file, "r") as archivo:
    code_body = archivo.read()

  scanner = Scanner(code_body)
  print("INFO SCAN - Start scanning...")
  tokens, errors = scanner.scan()
  for token in tokens:
    print(f'DEBUG SCAN - {token[1]} [ {repr(token[0])} ] found at {token[2]}.')
  if len(errors) > 0:
    print("INFO SCAN - Compilation failure, errors found.")
    for error in errors:
      print(f'\tERROR [ {repr(error[0])} ] at {error[1]}.')
  else:
    print("INFO SCAN - Finished without errors.")

def main():
  parser = argparse.ArgumentParser(description='Compile a file.')
  parser.add_argument('file', type=str, help='Path of the file you want to compile.')

  args = parser.parse_args()
  file = args.file

  compile(file)

if __name__ == "__main__":
  main()