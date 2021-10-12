import os
import sys

def single_file():
    print("...")

def multiple_files():
    count = 0
    files = os.listdir(sys.argv[2])
    for f in files:
        if f.endswith(".tsa"):
            count += 1
            with open(f, "r") as file_:
                compile(file_, open( "output/" + f + ".ts", "x"))
        else:
            continue
    assert count != 0, "ERROR: no .tsa file found"

def compile(file_, output):
    for line in file_:
        line = line.lstrip()

        if line.endswith("=>\n"):
            line = line[:-1] + " {\n"             # arrow func

        if line.startswith("if "):
            line = "if(" + line[3:]             # replace 'if ' with 'if('
            line = line[:-2] + ") {\n"          # replace ':' with ') {'
        elif line.startswith("func "):
            line = "const" + line[4:] 
        elif line.startswith("end"):
            line = "}" + line[3:]               # replace 'end' with '}'
        elif line.startswith("string"):
            line = "let" + line[6:]
            if " =" in line:
                line = line.replace("=", ":string =")
            else:
                line = line[:-1]
                line += ":string\n"               # String
        elif line.startswith("int"):
                line = "let" + line[3:]
                if " =" in line:
                    line = line.replace("=", ":number =")
                else:
                    line = line[:-1]
                    line += ":number\n"

        if "printf(" in line:
            line = line.replace("printf(", "console.log(") # replace printf()

        output.write(line)          # push line

def remove_files(dir_):
    for filename in os.listdir(dir_):
        os.remove(dir_ + "/" + filename)

def main():
    if sys.argv[1] == "-f":
        if len(sys.argv) > 2:
            single_file()
        else:
            assert False, "ERROR: please provide a file"

    elif sys.argv[1] == "-d":
        if len(sys.argv) > 2:
            remove_files("./output")
            multiple_files()
        else:
            assert False, "ERROR: please provide a directory"

if __name__ == "__main__":
    main()
